# attacks/dictionary.py
from utils.crypto import hash_password


def dictionary_attack(hash_to_crack: str, wordlist_path: str) -> str | None:
    try:
        with open(wordlist_path, "r", encoding="latin-1") as wordlist_file:
            for line_num, line in enumerate(wordlist_file, start=1):
                password_candidate = line.rstrip("\n")

                candidate_hash = hash_password(password_candidate)

                if candidate_hash == hash_to_crack:
                    print(f"Match found on line {line_num} of the wordlist!")
                    return password_candidate

    except FileNotFoundError:
        print(f"Error: Wordlist file not found at {wordlist_path}")
        return None
    except Exception as e:
        print(f"An error occurred while reading the wordlist: {e}")
        return None

    print("Dictionary attack completed. No match found in the wordlist.")
    return None
