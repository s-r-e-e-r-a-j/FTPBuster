# FTPBuster

FTPBuster is a powerful command-line brute-forcing tool designed to brute-force FTP, SFTP, and explicit FTPS servers by performing dictionary-based attacks.  

---

## Features

- Brute-force support for **FTP**, **SFTP**, and **explicit FTPS (AUTH TLS only)**
- Supports **single username/password** and **username/password wordlists**
- Real-time progress: tried, remaining, speed, elapsed time, ETA
- **Optional option to save valid credentials to a file**
- **Multithreaded** for speed (**maximum threads: 50 for better accuracy**)
- **Automatically handles UTF-8 encoded wordlists**, with fallback to **Latin-1** if UTF-8 fails

---

## ⚠️ Legal Disclaimer
FTPBuster is intended for educational and authorized security testing purposes only.
Unauthorized use of this tool against systems without explicit permission is illegal and strictly prohibited.
The author is not responsible for any misuse, damage, or legal consequences resulting from the use of this tool.

---

## Requirements

- Python 3.x
- `paramiko` library

Install dependencies:
```bash
pip3 install paramiko
```

---

## Compatibility
Linux (Debian, RedHat, Arch, etc.)

---

## installation

**1. Clone the Repository**
```bash
git clone https://github.com/s-r-e-e-r-a-j/FTPBuster.git
```
**2. Navigate to the FTPBuster directory**
```bash
cd FTPBuster
```
**3. Run Installer**
```bash
sudo python3 install.py
```
**then type `y` for install**

**4. Run the tool**
```bash
ftpbuster [options]
```

---

### Required Arguments

| Option               | Description                            |
|----------------------|----------------------------------------|
| `-t`, `--target`     | Target IP address or domain            |
| `-P`, `--protocol`   | Protocol to use: `FTP`, `SFTP`, `FTPS` |
| `-u`, `--user-file`  | Username wordlist                      |
| `--user`             | Single username                        |
| `-p`, `--pass-file`  | Password wordlist                      |
| `--password`         | Single password                        |

> You must provide either a wordlist or a single value for both username and password.

### Optional Arguments

| Option         | Description                                                                 |
|----------------|-----------------------------------------------------------------------------|
| `--port`       | Custom port (default: 21 for FTP/FTPS, 22 for SFTP)                         |
| `--threads`    | Number of threads (default: 10, **max: 50 enforced for better accuracy**)   |
| `--timeout`    | Timeout in seconds (default: 10)                                            |
| `--outfile`    | Optional option to save valid credentials to a file                         |

---

## Examples
**FTP with wordlists**
```bash
ftpbuster -t 192.168.1.5 -P FTP -u /home/kali/Desktop/users.txt -p /home/kali/Desktop/passwords.txt
```
**SFTP with single username**
```bash
ftpbuster -t 192.168.1.5 -P SFTP --user root -p /home/kali/Desktop/passwords.txt
```
**FTPS with output file**
```bash
ftpbuster -t ftp.example.com -P FTPS -u /home/kali/Desktop/user.txt -p /home/kali/Desktop/pass.txt --outfile /home/kali/Desktop/valid.txt
```

---

## Uninstallation
**Run the install.py script**
```bash
sudo python3 install.py
```
**Then Type `n` for uninstall**

---
## License
This project is licensed under the GNU General Public License v3.0





