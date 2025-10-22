import random
import pickle
import threading
from typing import Dict, List, Set, Optional
from utils.crypto import hash_password, verify_password


class MarkovModel:
    """Markov chain model for password generation with serialization support"""

    def __init__(self, order: int = 3):
        self.order = order
        self.model: Dict[str, List[str]] = {}
        self.start_states: List[str] = []

    def train(self, passwords: List[str]):
        """Train the Markov model on a list of passwords"""
        print("Training Markov model...")

        for password in passwords:
            if len(password) < self.order:
                continue

            # Add start state
            start = password[: self.order]
            self.start_states.append(start)

            # Build transitions
            for i in range(len(password) - self.order):
                state = password[i : i + self.order]
                next_char = password[i + self.order]

                if state not in self.model:
                    self.model[state] = []
                self.model[state].append(next_char)

        print(
            f"Model trained with {len(self.model)} states and {len(self.start_states)} start states"
        )

    def generate_password(self, max_length: int = 20) -> str:
        """Generate a password using the Markov model"""
        if not self.start_states:
            return ""

        # Choose random start state
        state = random.choice(self.start_states)
        password = state

        while len(password) < max_length:
            if state not in self.model or not self.model[state]:
                break

            # Choose next character based on frequency
            next_char = random.choice(self.model[state])
            password += next_char

            # Update state (slide window)
            state = password[-self.order :]

        return password

    def save_model(self, filepath: str):
        """Save the trained model to a file"""
        with open(filepath, "wb") as f:
            pickle.dump(
                {
                    "order": self.order,
                    "model": self.model,
                    "start_states": self.start_states,
                },
                f,
            )
        print(f"Model saved to {filepath}")

    def load_model(self, filepath: str):
        """Load a trained model from a file"""
        with open(filepath, "rb") as f:
            data = pickle.load(f)
            self.order = data["order"]
            self.model = data["model"]
            self.start_states = data["start_states"]
        print(f"Model loaded from {filepath}")


class MarkovAttack:
    """Markov chain-based password attack"""

    def __init__(
        self,
        training_file: str,
        hash_type: str,
        max_threads: int = 4,
        max_passwords: int = 100000,
    ):
        self.training_file = training_file
        self.hash_type = hash_type
        self.max_threads = max_threads
        self.max_passwords = max_passwords
        self.model = MarkovModel(order=3)
        self.trained = False

    def train_model(self):
        """Train the Markov model on the provided file"""
        try:
            with open(self.training_file, "r", encoding="utf-8", errors="ignore") as f:
                passwords = [line.strip() for line in f if line.strip()]

            # Use a sample for training to avoid memory issues
            training_sample = min(len(passwords), 100000)
            self.model.train(passwords[:training_sample])
            self.trained = True

        except Exception as e:
            print(f"Error training Markov model: {e}")
            raise

    def crack(self, target_hash: str) -> Optional[str]:
        """Attempt to crack the hash using Markov-generated passwords"""
        if not self.trained:
            self.train_model()

        print(f"Starting Markov attack on {self.hash_type} hash")
        print(f"Generating up to {self.max_passwords} password candidates...")

        found_password: Optional[str] = None
        lock = threading.Lock()
        attempts = 0

        def worker():
            nonlocal found_password, attempts
            while found_password is None and attempts < self.max_passwords:
                with lock:
                    if attempts >= self.max_passwords:
                        break
                    attempts += 1
                    if attempts % 1000 == 0:
                        print(f"Tried {attempts} passwords...")

                password = self.model.generate_password()
                if verify_password(password, target_hash, self.hash_type):
                    with lock:
                        found_password = password
                    return

        # Create and start threads
        threads = []
        for _ in range(self.max_threads):
            thread = threading.Thread(target=worker)
            thread.start()
            threads.append(thread)

        # Wait for threads to complete
        for thread in threads:
            thread.join()

        return found_password
