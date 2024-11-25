import sys
from ftp_bruteforce import ftp_bruteforce_main
from ssh_bruteforce import ssh_bruteforce_main
from mysql_bruteforce import mysql_bruteforce_main
from hash_cracker import hash_cracker_main


def print_help():
    print("Available services and their usage:\n")

    print("1. FTP Bruteforce:")
    print("   python main.py ftp -h\n")

    print("2. SSH Bruteforce:")
    print("   python main.py ssh -h\n")

    print("3. MySQL Bruteforce:")
    print("   python main.py mysql -h\n")

    print("5. Hash Cracker:")
    print("   python main.py crack -h\n")

    print("Use '-h' with each command to view specific options.\n")


def main():
    if len(sys.argv) < 2:
        print_help()
        sys.exit(1)

    service = sys.argv[1]
    service_args = sys.argv[2:]

    if service == "ftp":
        ftp_bruteforce_main(service_args)
    elif service == "ssh":
        ssh_bruteforce_main(service_args)
    elif service == "mysql":
        mysql_bruteforce_main(service_args)
    elif service == "crack":
        hash_cracker_main(service_args)
    else:
        print(f"Error: Service '{service}' is not supported.")
        sys.exit(1)


if __name__ == "__main__":
    main()
