import os
import sys
from utils.banner import show_banner
from utils.password_analyzer import analyze_password_strength
from utils.crypto import hash_password, identify_hash_type
from attacks.dictionary import DictionaryAttack
from attacks.rainbow import RainbowAttack
from attacks.markov import MarkovAttack
from attacks.bruteforce import BruteForceAttack


def clear_screen():
    """Clear the terminal screen"""
    os.system("cls" if os.name == "nt" else "clear")


def display_main_menu():
    """Display the main menu"""
    clear_screen()
    show_banner()
    print("\n--- SEC-SUITE Main Menu ---")
    print("1. Password Cracking")
    print("2. Password Strength Analysis")
    print("3. Password Hashing")
    print("4. Keylogger")
    print("5. Network Scanner")
    print("6. Encoding/Decoding")
    print("0. Exit")

    choice = input("\nEnter your choice: ")
    return choice


def password_cracking_menu():
    """Password cracking submenu"""
    clear_screen()
    print("--- Password Cracking ---")
    print("1. Dictionary Attack")
    print("2. Rainbow Table Attack")
    print("3. Markov Chain Attack")
    print("4. Brute Force Attack")
    print("0. Back to Main Menu")

    choice = input("\nEnter your choice: ")
    return choice


def handle_dictionary_attack():
    """Handle dictionary attack"""
    clear_screen()
    print("--- Dictionary Attack ---")
    target_hash = input("Enter the target hash: ")
    hash_type = input(
        "Enter hash type (md5, sha1, sha256, sha512, bcrypt, scrypt, argon2) or press Enter to auto-detect: "
    )
    wordlist_path = (
        input("Enter wordlist path [data/rockyou.txt]: ") or "data/rockyou.txt"
    )
    threads = int(input("Enter number of threads [4]: ") or "4")

    if not hash_type:
        hash_type = identify_hash_type(target_hash)
        if not hash_type:
            print("Could not auto-detect hash type. Please specify.")
            return

    attack = DictionaryAttack(wordlist_path, hash_type, threads)
    result = attack.crack(target_hash)

    if result:
        print(f"\n[SUCCESS] Password found: {result}")
    else:
        print("\n[FAILED] Password not found")

    input("\nPress Enter to continue...")


def handle_rainbow_attack():
    """Handle rainbow table attack"""
    clear_screen()
    print("--- Rainbow Table Attack ---")
    target_hash = input("Enter the target hash: ")
    rainbow_table_path = input("Enter rainbow table path: ")

    attack = RainbowAttack(rainbow_table_path)
    result = attack.crack(target_hash)

    if result:
        print(f"\n[SUCCESS] Password found: {result}")
    else:
        print("\n[FAILED] Password not found")

    input("\nPress Enter to continue...")


def handle_markov_attack():
    """Handle Markov chain attack"""
    clear_screen()
    print("--- Markov Chain Attack ---")
    target_hash = input("Enter the target hash: ")
    hash_type = input(
        "Enter hash type (md5, sha1, sha256, sha512, bcrypt, scrypt, argon2) or press Enter to auto-detect: "
    )
    training_file = (
        input("Enter training file path [data/rockyou.txt]: ") or "data/rockyou.txt"
    )
    threads = int(input("Enter number of threads [4]: ") or "4")
    max_passwords = int(input("Enter max passwords to generate [100000]: ") or "100000")

    if not hash_type:
        hash_type = identify_hash_type(target_hash)
        if not hash_type:
            print("Could not auto-detect hash type. Please specify.")
            return

    attack = MarkovAttack(training_file, hash_type, threads, max_passwords)
    result = attack.crack(target_hash)

    if result:
        print(f"\n[SUCCESS] Password found: {result}")
    else:
        print("\n[FAILED] Password not found")

    input("\nPress Enter to continue...")


def handle_brute_force_attack():
    """Handle brute force attack"""
    clear_screen()
    print("--- Brute Force Attack ---")
    target_hash = input("Enter the target hash: ")
    hash_type = input(
        "Enter hash type (md5, sha1, sha256, sha512, bcrypt, scrypt, argon2) or press Enter to auto-detect: "
    )
    charset = (
        input("Enter character set [luds] (l=lower, u=upper, d=digit, s=special): ")
        or "luds"
    )
    min_length = int(input("Enter min length [1]: ") or "1")
    max_length = int(input("Enter max length [8]: ") or "8")
    threads = int(input("Enter number of threads [4]: ") or "4")

    if not hash_type:
        hash_type = identify_hash_type(target_hash)
        if not hash_type:
            print("Could not auto-detect hash type. Please specify.")
            return

    attack = BruteForceAttack(hash_type, charset, min_length, max_length, threads)
    result = attack.crack(target_hash)

    if result:
        print(f"\n[SUCCESS] Password found: {result}")
    else:
        print("\n[FAILED] Password not found")

    input("\nPress Enter to continue...")


def handle_password_cracking():
    """Handle password cracking menu"""
    while True:
        choice = password_cracking_menu()
        if choice == "1":
            handle_dictionary_attack()
        elif choice == "2":
            handle_rainbow_attack()
        elif choice == "3":
            handle_markov_attack()
        elif choice == "4":
            handle_brute_force_attack()
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.")
            input("Press Enter to continue...")


def handle_password_analysis():
    """Handle password strength analysis"""
    clear_screen()
    print("--- Password Strength Analysis ---")
    password = input("Enter the password to analyze: ")

    if not password:
        print("Password cannot be empty.")
    else:
        analyze_password_strength(password)

    input("\nPress Enter to continue...")


def hash_menu():
    """Handle password hashing"""
    clear_screen()
    print("--- Cryptographic Hasher ---")
    password = input("Enter the password to hash: ")

    if not password:
        print("Password cannot be empty.")
    else:
        algorithm = (
            input(
                "Enter algorithm (md5, sha1, sha256, sha512, bcrypt, scrypt, argon2) [sha256]: "
            )
            or "sha256"
        )
        hashed = hash_password(password, algorithm)
        print(f"\n{algorithm.upper()} Hash: {hashed}")

    input("\nPress Enter to return to the main menu...")


def handle_keylogger():
    """Handle keylogger menu"""
    clear_screen()
    print("--- Keylogger ---")
    print("This feature is available via the command line interface.")
    print("Please run: python main.py keylog --help")
    input("\nPress Enter to continue...")


def handle_network_scanner():
    """Handle network scanner menu"""
    clear_screen()
    print("--- Network Scanner ---")
    print("This feature is available via the command line interface.")
    print("Please run: python main.py scan --help")
    input("\nPress Enter to continue...")


def handle_encoding_decoding():
    """Handle encoding/decoding menu"""
    clear_screen()
    print("--- Encoding/Decoding ---")
    print("This feature is available via the command line interface.")
    print("Please run: python main.py encode --help")
    input("\nPress Enter to continue...")


def main():
    """Main CLI loop"""
    while True:
        choice = display_main_menu()

        if choice == "1":
            handle_password_cracking()
        elif choice == "2":
            handle_password_analysis()
        elif choice == "3":
            hash_menu()
        elif choice == "4":
            handle_keylogger()
        elif choice == "5":
            handle_network_scanner()
        elif choice == "6":
            handle_encoding_decoding()
        elif choice == "0":
            print("Exiting SEC-SUITE. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
            input("Press Enter to continue...")


if __name__ == "__main__":
    main()
