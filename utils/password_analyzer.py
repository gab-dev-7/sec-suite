import math
import string
import secrets


def calculate_password_entropy(password: str) -> float:
    if not password:
        return 0.0

    # Define character sets
    lowercase = set(string.ascii_lowercase)
    uppercase = set(string.ascii_uppercase)
    digits = set(string.digits)
    symbols = set(string.punctuation)

    password_chars = set(password)

    # Determine which character sets are used
    char_pool_size = 0
    if password_chars.intersection(lowercase):
        char_pool_size += len(lowercase)
    if password_chars.intersection(uppercase):
        char_pool_size += len(uppercase)
    if password_chars.intersection(digits):
        char_pool_size += len(digits)
    if password_chars.intersection(symbols):
        char_pool_size += len(symbols)

    # Calculate entropy
    L = len(password)
    N = char_pool_size

    if N > 0:
        entropy = L * math.log2(N)
    else:
        entropy = 0.0

    print(f"Password: '{password}'")
    print(f"Length (L): {L}")
    print(f"Character Pool Size (N): {N}")
    print(f"Calculated Entropy: {entropy:.2f} bits")
    print("-" * 20)

    return entropy


def generate_password(length: int, use_symbols: bool = True):
    if length <= 0:
        raise ValueError("Password length must be a positive integer.")

    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    symbols = string.punctuation

    character_pool = lowercase + uppercase + digits
    if use_symbols:
        character_pool += symbols

    password = "".join(secrets.choice(character_pool) for _ in range(length))

    return password
