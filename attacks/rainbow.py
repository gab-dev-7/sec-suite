# attacks/rainbow.py
import hashlib
import secrets
import pickle
import os

# --- Helper Functions ---


def hash_password(password: str, algorithm: str = "sha256") -> str:
    """Hashes a password string using the specified algorithm."""
    h = hashlib.new(algorithm)
    h.update(password.encode("utf-8"))
    return h.hexdigest()


def generate_random_password(charset: str, length: int) -> str:
    """Generates a random password of given length using the charset."""
    return "".join(secrets.choice(charset) for _ in range(length))


# --- Core Rainbow Table Functions ---


def reduce(hash_digest: str, position: int, charset: str, length: int) -> str:
    """
    A simple reduction function.
    - hash_digest: The hex string of the hash.
    - position: The position in the chain (0, 1, 2...). This is crucial!
    - charset: The set of characters to use for the password.
    - length: The desired length of the reduced password.
    """
    # 1. Convert a part of the hash to a number
    # We use the position to make sure the reduction function is different at each step
    # Take a slice of the hash based on position to get different starting points
    slice_start = position % len(hash_digest)
    sliced_hash = (
        hash_digest[slice_start:] + hash_digest[:slice_start]
    )  # Rotate to avoid always taking the same part
    num = int(sliced_hash, 16)

    # 2. Convert that number into a password using base conversion
    password = ""
    temp_num = num
    for _ in range(length):
        password += charset[temp_num % len(charset)]
        temp_num //= len(charset)

    return password


def generate_table(
    num_chains: int,
    chain_length: int,
    charset: str,
    max_len: int,
    hash_algorithm: str = "sha256",
    filename: str = "rainbow_table.pkl",
):
    """
    Generates a rainbow table and saves it to a file.
    Args:
        num_chains: Number of chains to generate.
        chain_length: Number of steps in each chain (hash -> reduce -> ...).
        charset: Character set to use for passwords.
        max_len: Maximum length of passwords.
        hash_algorithm: Hash algorithm to use (e.g., 'sha256', 'md5').
        filename: Name of the file to save the table.
    """
    print(
        f"Generating table: {num_chains} chains, {chain_length} length, charset: {charset}, max_len: {max_len}, hash: {hash_algorithm}"
    )
    table = {}  # Use a dictionary for O(1) lookup: {end_hash: start_password}

    # 1. Initialize the counter HERE, before the loop starts.
    passwords_shown = 0

    for i in range(num_chains):
        if i % (num_chains // 10) == 0:  # Print progress every 10%
            print(f"Progress: {i}/{num_chains} chains generated...")

        start_password = generate_random_password(charset, max_len)
        current_hash = hash_password(start_password, hash_algorithm)

        # This is the chain generation loop
        for j in range(chain_length):
            reduced_pwd = reduce(current_hash, j, charset, max_len)
            current_hash = hash_password(reduced_pwd, hash_algorithm)

        # Store only the start and end of the chain in the dictionary
        end_hash = current_hash
        if end_hash not in table:
            table[end_hash] = start_password

            # 2. Now, use and increment the counter inside this 'if' block.
            # This ensures we only print when we add a new, unique chain.
            if passwords_shown < 5:
                print(f"  -> Starting chain with password: '{start_password}'")
                passwords_shown += 1

    print(f"Saving table to {filename}...")
    with open(filename, "wb") as f:
        pickle.dump((table, chain_length, charset, max_len, hash_algorithm), f)
    print("Table generation complete.")


def crack_hash(target_hash: str, filename: str = "rainbow_table.pkl"):
    """
    Attempts to crack a target hash using a precomputed rainbow table.
    """
    if not os.path.exists(filename):
        print(f"Error: Rainbow table file '{filename}' not found.")
        return None

    print(f"Loading table from {filename}...")
    try:
        with open(filename, "rb") as f:
            table_data = pickle.load(f)
        table, chain_length, charset, max_len, hash_algorithm = table_data
    except Exception as e:
        print(f"Error loading table: {e}")
        return None

    print(f"Attempting to crack hash: {target_hash}")

    for j in range(chain_length - 1, -1, -1):
        current_hash = target_hash

        # THE FIX IS HERE: Use chain_length instead of chain_length - 1
        for k in range(j, chain_length):
            reduced_pwd = reduce(current_hash, k, charset, max_len)
            current_hash = hash_password(reduced_pwd, hash_algorithm)

        if current_hash in table:
            start_pwd = table[current_hash]
            print(
                f"Potential chain found! End hash {current_hash} corresponds to start password '{start_pwd}'."
            )

            current_pwd = start_pwd
            current_hash_calc = hash_password(current_pwd, hash_algorithm)

            for step in range(chain_length):
                if current_hash_calc == target_hash:
                    print(f"Password found: '{current_pwd}' hashes to '{target_hash}'")
                    return current_pwd

                reduced_pwd_next = reduce(current_hash_calc, step, charset, max_len)
                current_hash_calc = hash_password(reduced_pwd_next, hash_algorithm)
                current_pwd = reduced_pwd_next

    print("Hash not found in the table.")
    return None


# --- Example Usage ---
if __name__ == "__main__":
    # Example parameters
    TEST_CHARSET = "abcd"
    TEST_PASSWORD_LENGTH = 4
    NUM_CHAINS = 100
    CHAIN_LENGTH = 100
    HASH_ALGO = "sha256"
    TABLE_FILE = "test_rainbow_table.pkl"

    # --- Test the reduce function ---
    test_pwd = "abcd"
    test_hash = hash_password(test_pwd, HASH_ALGO)
    print(f"Original Password: {test_pwd}")
    print(f"Hash: {test_hash}")
    reduced_pwd_0 = reduce(test_hash, 0, TEST_CHARSET, TEST_PASSWORD_LENGTH)
    reduced_pwd_1 = reduce(test_hash, 1, TEST_CHARSET, TEST_PASSWORD_LENGTH)
    print(f"Reduce({test_hash}, 0, ...) -> {reduced_pwd_0}")
    print(f"Reduce({test_hash}, 1, ...) -> {reduced_pwd_1}")
    print("---")

    # --- Generate a small test table ---
    print("Generating a small test table...")
    generate_table(
        NUM_CHAINS,
        CHAIN_LENGTH,
        TEST_CHARSET,
        TEST_PASSWORD_LENGTH,
        HASH_ALGO,
        TABLE_FILE,
    )
    print("---")

    # --- Try to crack a hash from a known password ---
    # Let's say we know the password "abca" was used.
    known_password = "abca"
    target_hash_to_find = hash_password(known_password, HASH_ALGO)
    print(f"Known password: {known_password}, its hash: {target_hash_to_find}")

    cracked_password = crack_hash(target_hash_to_find, TABLE_FILE)
    if cracked_password:
        print(f"Successfully cracked! Password is: {cracked_password}")
        assert (
            cracked_password == known_password
        ), f"Cracked password '{cracked_password}' does not match known password '{known_password}'"
    else:
        print("Failed to crack the hash (might not be in the small test table).")

    # --- Try to crack a hash not in the table ---
    unknown_password = "zzzz"  # Very unlikely to be in a table with charset "abcd"
    unknown_hash = hash_password(unknown_password, HASH_ALGO)
    print(f"\nTrying to crack hash for unknown password: {unknown_hash}")
    cracked_unknown = crack_hash(unknown_hash, TABLE_FILE)
    if not cracked_unknown:
        print("Correctly failed to crack hash for password not in table.")
