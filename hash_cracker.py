import hashlib
from tqdm import tqdm
import argparse
import sys

# Supported hash algorithms
hash_names = [
    'blake2b', 'blake2s', 
    'md5', 'sha1', 
    'sha224', 'sha256', 'sha384', 'sha512',
    'sha3_224', 'sha3_256', 'sha3_384', 'sha3_512', 
]

def crack_single_hash(hash_value, wordlist, hash_type):
    hash_fn = getattr(hashlib, hash_type, None)
    if hash_fn is None or hash_type not in hash_names:
        raise ValueError(f'[!] Invalid hash type: {hash_type}. Supported types: {hash_names}')
    
    with open(wordlist, 'r', encoding='utf-8') as f:
        for line in tqdm(f, desc=f'Cracking {hash_type} hash', unit=" word"):
            if hash_fn(line.strip().encode()).hexdigest() == hash_value:
                return line.strip()
    return None

def crack_hash_file(hash_file, wordlist, hash_type, output_file=None):
    results = []
    with open(hash_file, 'r') as hashes:
        for hash_value in hashes:
            hash_value = hash_value.strip()
            password = crack_single_hash(hash_value, wordlist, hash_type)
            result = f"{hash_value}:{password if password else 'Not found'}"
            results.append(result)
            print(result)
    
    if output_file:
        with open(output_file, 'w') as f:
            f.write('\n'.join(results))
        print(f"[+] Results saved to {output_file}")

    return results

def hash_cracker_main(args=None):
    parser = argparse.ArgumentParser(description='Crack hashes using a wordlist.')
    parser.add_argument('-hash', '--hash', help='The hash to crack.')
    parser.add_argument('-hash-file', '--hash-file', help='A file containing hashes to crack.')
    parser.add_argument('-w', '--wordlist', help='Path to the wordlist.', required=True)
    parser.add_argument('-t', '--hash-type', help='Hash type to use. Choose between:- blake2b, blake2s,md5, sha1, sha224, sha256, sha384, sha512, sha3_224, sha3_256, sha3_384, sha3_512', default='md5')
    parser.add_argument('-o', '--output', help='Output file to save cracked hashes.')

    parsed_args = parser.parse_args(args)

    try:
        if parsed_args.hash:
            print(f"[+] Cracking single hash: {parsed_args.hash}")
            password = crack_single_hash(parsed_args.hash, parsed_args.wordlist, parsed_args.hash_type)
            if password:
                print(f"[+] Found password: {password}")
                if parsed_args.output:
                    with open(parsed_args.output, 'w') as f:
                        f.write(f"{parsed_args.hash}:{password}\n")
            else:
                print("[!] Password not found.")
        
        elif parsed_args.hash_file:
            print(f"[+] Cracking hashes from file: {parsed_args.hash_file}")
            crack_hash_file(parsed_args.hash_file, parsed_args.wordlist, parsed_args.hash_type, parsed_args.output)
        else:
            print("[!] Please provide either --hash or --hash-file.")
    
    except KeyboardInterrupt:
        print("\n[!] Process interrupted by user.")
    except FileNotFoundError as e:
        print(f"[!] File error: {e}")
    except Exception as e:
        print(f"[!] Error: {e}")

if __name__ == "__main__":
    hash_cracker_main()
