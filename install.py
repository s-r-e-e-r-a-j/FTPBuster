
import os
import sys

if os.geteuid() != 0:
    print("please run as root or with sudo")
    sys.exit(1)
choice = input('[+] to install press (Y) to uninstall press (N) >> ')
run = os.system
if str(choice) =='Y' or str(choice)=='y':

    run('chmod 755 ftpbuster.py')
    run('mkdir /usr/share/ftpbuster')
    run('cp ftpbuster.py /usr/share/ftpbuster/ftpbuster.py')

    cmnd=(' #! /bin/sh \n exec python3 /usr/share/ftpbuster/ftpbuster.py "$@"')
    with open('/usr/bin/ftpbuster','w')as file:
        file.write(cmnd)
    run('chmod +x /usr/bin/ftpbuster & chmod +x /usr/share/ftpbuster/ftpbuster.py')
    print('''\n\ncongratulation FTPBuster is installed successfully \nfrom now just type \x1b[6;30;42mftpbuster\x1b[0m in terminal ''')
if str(choice)=='N' or str(choice)=='n':
    run('rm -r /usr/share/ftpbuster ')
    run('rm /usr/bin/ftpbuster ')
    print('[!] now FTPBuster has been removed successfully')
