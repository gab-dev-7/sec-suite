import random
import pickle
import multiprocessing
from typing import Dict, List, Set, Optional
from utils.crypto import hash_password, verify_password
import os
from utils.data_downloader import download_rockyou_wordlist


class MarkovModel:
    """Markov chain model for password generation with serialization support"""

    def __init__(self, order: int = 3):
        self.order = order
        self.model: Dict[str, List[str]] = {}
        self.start_states: List[str] = []

    def train(self, passwords_iterator):
        """Train the Markov model on an iterator of passwords"""
        print("Training Markov model...")

        count = 0
        for password in passwords_iterator:
            password = password.strip()
            if not password or len(password) < self.order:
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
            
            count += 1
            if count % 50000 == 0:
                print(f"Processed {count} passwords for training...")

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
        download_rockyou_wordlist()
        if not os.path.exists(training_file):
            raise FileNotFoundError(
                f"Training file not found at '{training_file}'. "
                "Please ensure the file exists. "
                "You may need to download a wordlist like 'rockyou.txt' and place it in the 'data' directory."
            )
        self.training_file = training_file
        self.hash_type = hash_type
        self.max_threads = max_threads
        self.max_passwords = max_passwords
        self.model = MarkovModel(order=3)
        self.trained = False

    def train_model(self):
        """Train the Markov model on the provided file using a stream"""
        try:
            def password_stream():
                count = 0
                with open(self.training_file, "r", encoding="utf-8", errors="ignore") as f:
                    for line in f:
                        yield line
                        count += 1
                        if count >= 100000:  # Still sample for training performance
                            break

            self.model.train(password_stream())
            self.trained = True

        except Exception as e:
            print(f"Error training Markov model: {e}")
            raise

    def _worker(self, target_hash: str, num_passwords: int, result_queue: multiprocessing.Queue):
        """Worker process to generate and test passwords"""
        for _ in range(num_passwords):
            password = self.model.generate_password()
            if verify_password(password, target_hash, self.hash_type):
                result_queue.put(password)
                return
        result_queue.put(None)

    def crack(self, target_hash: str) -> Optional[str]:
        """Attempt to crack the hash using Markov-generated passwords"""
        if not self.trained:
            self.train_model()

        print(f"Starting Markov attack on {self.hash_type} hash")
        print(f"Generating up to {self.max_passwords} password candidates...")
        print(f"Using {self.max_threads} processes")

        result_queue = multiprocessing.Queue()
        passwords_per_process = self.max_passwords // self.max_threads
        
        processes = []
        for _ in range(self.max_threads):
            p = multiprocessing.Process(
                target=self._worker,
                args=(target_hash, passwords_per_process, result_queue)
            )
            p.daemon = True
            p.start()
            processes.append(p)

        # Wait for threads to complete
        found_password = None
        finished_workers = 0
        
        try:
            while finished_workers < len(processes):
                result = result_queue.get()
                if result:
                    found_password = result
                    for p in processes:
                        p.terminate()
                    return found_password
                finished_workers += 1
        except KeyboardInterrupt:
            for p in processes:
                p.terminate()
            raise

        return found_password
