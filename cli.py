# cli.py
import os
from utils.banner import get_banner, clear_screen
from utils.password_analyzer import calculate_password_entropy, generate_password
from utils.crypto import hash_password
from attacks.dictionary import dictionary_attack
from attacks.rainbow import generate_table, crack_hash


def display_main_menu():
    """Displays the main menu and returns the user's choice."""
    clear_screen()
    print(get_banner())
    print("\n--- Main Menu ---\n")
    print("1. Analyze Password Entropy")
    print("2. Generate a Secure Password")
    print("3. Hash a Password")
    print("4. Dictionary Attack")
    print("5. Rainbow Table Utilities")
    print("0. Exit")
    return input("\nSelect an option: ")


def entropy_menu():
    """Handles the password entropy analysis."""
    clear_screen()
    print("--- Password Entropy Calculator ---")
    password = input("Enter the password to analyze: ")
    if not password:
        print("Password cannot be empty.")
    else:
        calculate_password_entropy(password)
    input("\nPress Enter to return to the main menu...")


def generate_menu():
    """Handles the secure password generation."""
    clear_screen()
    print("--- Secure Password Generator ---")
    try:
        length = int(input("Enter desired password length (e.g., 16): "))
        use_symbols = input("Include symbols? (y/n): ").lower() == "y"
        password = generate_password(length, use_symbols)
        print(f"\nGenerated Password: {password}")
    except ValueError:
        print("\nInvalid length. Please enter a number.")
    input("\nPress Enter to return to the main menu...")


def hash_menu():
    """Handles the password hashing."""
    clear_screen()
    print("--- Cryptographic Hasher ---")
    password = input("Enter the password to hash: ")
    if not password:
        print("Password cannot be empty.")
    else:
        hashed = hash_password(password)
        print(f"\nSHA-256 Hash: {hashed}")
    input("\nPress Enter to return to the main menu...")


def dictionary_attack_menu():
    """Handles the dictionary attack."""
    clear_screen()
    print("--- Dictionary Attack ---")
    hash_to_crack = input("Enter the hash to crack: ")
    wordlist_path = (
        input("Enter path to wordlist (default: data/rockyou.txt): ")
        or "data/rockyou.txt"
    )

    if not os.path.exists(wordlist_path):
        print(f"\nError: Wordlist file not found at '{wordlist_path}'")
    else:
        print("\nStarting dictionary attack... This may take a while.")
        cracked_password = dictionary_attack(hash_to_crack, wordlist_path)
        if cracked_password:
            print(f"\n✅ Password cracked: {cracked_password}")
        else:
            print("\n❌ Password not found in the wordlist.")
    input("\nPress Enter to return to the main menu...")


def rainbow_menu():
    """Handles the rainbow table utilities sub-menu."""
    while True:
        clear_screen()
        print("--- Rainbow Table Utilities ---\n")
        print("1. Generate a Rainbow Table")
        print("2. Crack a Hash with a Rainbow Table")
        print("B. Back to Main Menu")
        choice = input("\nSelect an option: ").lower()

        if choice == "1":
            rainbow_generate_menu()
        elif choice == "2":
            rainbow_crack_menu()
        elif choice == "b":
            break
        else:
            input("\nInvalid option. Press Enter to try again...")


def rainbow_generate_menu():
    """Handles the rainbow table generation."""
    clear_screen()
    print("--- Generate Rainbow Table ---")
    try:
        charset = input("Enter character set (e.g., 'abcd'): ")
        num_chains = int(input("Enter number of chains (e.g., 5000): "))
        chain_length = int(input("Enter chain length (e.g., 50): "))
        max_len = int(input("Enter max password length (e.g., 4): "))
        filename = input("Enter output filename (e.g., hex_table.pkl): ")

        print("\nStarting table generation... This will take some time.")
        generate_table(num_chains, chain_length, charset, max_len, filename=filename)
        print("\n✅ Table generation complete.")
    except ValueError:
        print("\n❌ Invalid input. Please enter valid numbers.")
    input("\nPress Enter to return to the Rainbow menu...")


def rainbow_crack_menu():
    """Handles the rainbow table cracking."""
    clear_screen()
    print("--- Crack Hash with Rainbow Table ---")
    hash_to_crack = input("Enter the hash to crack: ")
    filename = input("Enter rainbow table filename (e.g., hex_table.pkl): ")

    if not os.path.exists(filename):
        print(f"\n❌ Error: Rainbow table file not found at '{filename}'")
    else:
        print("\nStarting crack attempt...")
        cracked_password = crack_hash(hash_to_crack, filename)
        if cracked_password:
            print(f"\n✅ Successfully cracked! Password is: {cracked_password}")
        else:
            print("\n❌ Failed to crack the hash.")
    input("\nPress Enter to return to the Rainbow menu...")


def main():
    """Main application loop."""
    while True:
        choice = display_main_menu()
        if choice == "1":
            entropy_menu()
        elif choice == "2":
            generate_menu()
        elif choice == "3":
            hash_menu()
        elif choice == "4":
            dictionary_attack_menu()
        elif choice == "5":
            rainbow_menu()
        elif choice == "0":
            clear_screen()
            print("Exiting Password Security Suite. Stay secure!")
            break
        else:
            input("\nInvalid option. Press Enter to try again...")


if __name__ == "__main__":
    main()
