# BruteForceX

**BruteForceX** is a powerful and versatile tool designed for performing brute-force attacks on network protocols like SSH, FTP, MySQL, and cracking password hashes (MD5, SHA1, SHA256, etc.). It is built for ethical hackers, penetration testers, and cybersecurity professionals to test system vulnerabilities in a controlled and legal environment.


## Features:

- Perform brute-force attacks on:
  - SSH
  - FTP
  - MySQL login protocols
- Crack password hashes:
  - BLAKE2b, BLAKE2s, MD5, SHA-1, SHA-224, SHA-256, SHA-384, SHA-512, SHA3-224, SHA3-256, SHA3-384, SHA3-512


## Table of Contents:

- [Installation](#installation)
- [Usage](#usage)
  - [General Help](#general-help)
  - [FTP Brute Force](#ftp-brute-force)
  - [SSH Brute Force](#ssh-brute-force)
  - [MySQL Brute Force](#mysql-brute-force)
  - [Hash Cracking](#hash-cracking)
- [Contributing](#contributing)
- [Disclaimer](#disclaimer)


## Installation

To get started with \*\*BruteForceX\*\*, follow these steps:

1. **Clone the repository:**

  ```bash
  git clone https://github.com/yourusername/BruteForceX.git
  ```
  ```bash
  cd BruteForceX
  ```

2. **Install the dependencies:**

```bash
pip install -r requirements.txt
```

3. **Run the tool:**

```bash
python main.py
```

## Usage

### General Help

Run the following command to display the help menu:

```bash
python main.py
```


### FTP Brute Force

1. **Display help menu for FTP brute force:**

```bash
python main.py ftp -h
```

2. **Single username with a password file:**

```bash
python main.py ftp -u <username> -P <password file> -host <IP>
```

3. **Multiple usernames with a password file:**

```bash
python main.py ftp -U <usernames file> -P <password file> -host <IP>
```

4. **Single username against all passwords in a file:**

```bash
python main.py ftp -u <username> -P <password file> -host <IP>
```

5. **Save output to a file:**

```bash
python main.py ftp -U <usernames file> -P <password file> -host <IP> -o <output file>
```


### SSH Brute Force

1. Single username with a password file:

```bash
python main.py ssh -u <username> -P <password file> -host <IP>
```

2. Multiple usernames with a password file:

```bash
python main.py ssh -U <usernames file> -P <password file> -host <IP>
```
3. **Single username against all passwords in a file:**

```bash
python main.py ssh -u <username> -P <password file> -host <IP>
```

4. **Save output to a file:**

```bash
python main.py ssh -U <usernames file> -P <password file> -host <IP> -o <output file>
```

### MySQL Brute Force

1. Single username with a password file:

```bash
python main.py mysql -u <username> -P <password file> -host <IP>
```

2. Multiple usernames with a password file:

```bash
python main.py mysql -U <usernames file> -P <password file> -host <IP>
```
3. **Single username against all passwords in a file:**

```bash
python main.py mysql -u <username> -P <password file> -host <IP>
```

4. **Save output to a file:**

```bash
python main.py mysql -U <usernames file> -P <password file> -host <IP> -o <output file>
```

### Hash Cracking

1. **Crack a hash from a wordlist**

```bash
python main.py crack -hash <hash> -t <type> -w <wordlist file>
```

2. **Crack multiple hashes from a file:**

```bash
python main.py crack -hash-file <hash file> -t <hash type> -w <wordlist file>
```

3. **Save output to a file:**

```bash
python main.py crack -hash-file <hash file> -t <hash type> -w <wordlist file> -o <output file>
```

## Disclaimer

**BruteForceX**  is  intended  for  educational  purposes  and  authorized  security  testing  only. Unauthorized use of this tool is illegal and unethical. The developers are not responsible for any misuse of this tool. Always obtain proper permissions before performing any security tests.



