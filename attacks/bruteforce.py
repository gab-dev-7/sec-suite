import itertools
import threading
import string
from typing import Optional
from utils.crypto import verify_password


class BruteForceAttack:
    """Brute force password attack with configurable character sets"""

    # Character sets
    CHAR_SETS = {
        "l": string.ascii_lowercase,  # lowercase letters
        "u": string.ascii_uppercase,  # uppercase letters
        "d": string.digits,  # digits
        "s": string.punctuation,  # special characters
    }

    def __init__(
        self,
        hash_type: str,
        charset: str = "lud",
        min_length: int = 1,
        max_length: int = 8,
        max_threads: int = 4,
    ):
        self.hash_type = hash_type
        self.charset = self._build_charset(charset)
        self.min_length = min_length
        self.max_length = max_length
        self.max_threads = max_threads

    def _build_charset(self, charset_spec: str) -> str:
        """Build character set from specification string"""
        charset = ""
        for char in charset_spec:
            if char in self.CHAR_SETS:
                charset += self.CHAR_SETS[char]
        return "".join(sorted(set(charset)))  # Remove duplicates

    def generate_combinations(self, length: int):
        """Generate all combinations for a given length"""
        for combo in itertools.product(self.charset, repeat=length):
            yield "".join(combo)

    def crack(self, target_hash: str) -> Optional[str]:
        """Perform brute force attack"""
        print(f"Starting brute force attack on {self.hash_type} hash")
        print(f"Character set: {self.charset}")
        print(f"Password length: {self.min_length}-{self.max_length}")
        print(f"Total combinations: {self.calculate_total_combinations()}")

        found_password: Optional[str] = None
        lock = threading.Lock()
        current_length = self.min_length

        def worker():
            nonlocal found_password, current_length
            while found_password is None and current_length <= self.max_length:
                # Get current length to process
                with lock:
                    if current_length > self.max_length:
                        break
                    length = current_length
                    current_length += 1

                print(f"Trying length {length}...")

                for password in self.generate_combinations(length):
                    if found_password is not None:
                        break

                    if verify_password(password, target_hash, self.hash_type):
                        with lock:
                            found_password = password
                        break

        # Create and start threads
        threads = []
        for _ in range(min(self.max_threads, self.max_length - self.min_length + 1)):
            thread = threading.Thread(target=worker)
            thread.start()
            threads.append(thread)

        # Wait for threads to complete
        for thread in threads:
            thread.join()

        return found_password

    def calculate_total_combinations(self) -> int:
        """Calculate total number of possible combinations"""
        total = 0
        charset_size = len(self.charset)
        for length in range(self.min_length, self.max_length + 1):
            total += charset_size**length
        return total
