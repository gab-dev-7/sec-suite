import threading
import queue
import time
from typing import Optional
from utils.crypto import verify_password
import os


class DictionaryAttack:
    """Multi-threaded dictionary attack"""

    def __init__(self, wordlist_path: str, hash_type: str, max_threads: int = 4):
        if not os.path.exists(wordlist_path):
            raise FileNotFoundError(
                f"Wordlist not found at '{wordlist_path}'. "
                "Please ensure the file exists. "
                "You may need to download a wordlist like 'rockyou.txt' and place it in the 'data' directory."
            )
        self.wordlist_path = wordlist_path
        self.hash_type = hash_type
        self.max_threads = max_threads

    def _password_producer(self, password_queue: queue.Queue):
        """Produce passwords from wordlist"""
        try:
            with open(self.wordlist_path, "r", encoding="utf-8", errors="ignore") as f:
                for line_num, line in enumerate(f, 1):
                    password = line.strip()
                    if password:  # Skip empty lines
                        password_queue.put(password)

                    if line_num % 10000 == 0:
                        print(f"Loaded {line_num} passwords...")

            # Signal end of production
            for _ in range(self.max_threads):
                password_queue.put(None)

        except Exception as e:
            print(f"Error reading wordlist: {e}")
            for _ in range(self.max_threads):
                password_queue.put(None)

    def _password_consumer(
        self, password_queue: queue.Queue, target_hash: str, result_queue: queue.Queue
    ):
        """Consume passwords and test against hash"""
        attempts = 0

        while True:
            password = password_queue.get()

            # Check for termination signal
            if password is None:
                password_queue.task_done()
                break

            attempts += 1
            if attempts % 1000 == 0:
                print(f"Tested {attempts} passwords...")

            if verify_password(password, target_hash, self.hash_type):
                result_queue.put(password)
                password_queue.task_done()
                return

            password_queue.task_done()

        result_queue.put(None)

    def crack(self, target_hash: str) -> Optional[str]:
        """Perform dictionary attack"""
        print(f"Starting dictionary attack on {self.hash_type} hash")
        print(f"Using wordlist: {self.wordlist_path}")

        password_queue = queue.Queue(maxsize=10000)
        result_queue = queue.Queue()

        # Start producer thread
        producer_thread = threading.Thread(
            target=self._password_producer, args=(password_queue,)
        )
        producer_thread.daemon = True
        producer_thread.start()

        # Start consumer threads
        consumer_threads = []
        for _ in range(self.max_threads):
            thread = threading.Thread(
                target=self._password_consumer,
                args=(password_queue, target_hash, result_queue),
            )
            thread.daemon = True
            thread.start()
            consumer_threads.append(thread)

        # Wait for a result
        found_password = None
        results_received = 0

        while results_received < self.max_threads and found_password is None:
            try:
                result = result_queue.get(timeout=1)
                if result is not None:
                    found_password = result
                results_received += 1
            except queue.Empty:
                pass

        # Clean up
        if found_password is None:
            # Wait for all threads to finish naturally
            password_queue.join()

        return found_password
