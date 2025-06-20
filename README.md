# FTPBrute

FTPBrute is a powerful command-line brute-forcing tool designed to brute-force FTP, SFTP, and explicit FTPS servers by performing dictionary-based attacks.  

---

## 🚀 Features

- Brute-force support for **FTP**, **SFTP**, and **explicit FTPS (AUTH TLS only)**
- Supports **single username/password** and **username/password wordlists**
- Real-time progress: tried, remaining, speed, elapsed time, ETA
- **Optional option to save valid credentials to a file**
- **Multithreaded** for speed (**maximum threads: 50 for better accuracy**)
- **Automatically handles UTF-8 encoded wordlists**, with fallback to **Latin-1** if UTF-8 fails

---

##  Supported Protocols

- ✅ FTP
- ✅ SFTP (via Paramiko)
- ✅ FTPS (explicit AUTH TLS only)

---

##  Requirements

- Python 3.x
- `paramiko` module

Install dependencies:
```bash
pip3 install paramiko
```
