import multiprocessing
from typing import Optional
from utils.crypto import verify_password
import os
from utils.data_downloader import download_rockyou_wordlist


class DictionaryAttack:
    """Multi-process dictionary attack"""

    def __init__(self, wordlist_path: str, hash_type: str, max_threads: int = 4):
        download_rockyou_wordlist()
        if not os.path.exists(wordlist_path):
            raise FileNotFoundError(
                f"Wordlist not found at '{wordlist_path}'. "
                "Please ensure the file exists. "
                "You may need to download a wordlist like 'rockyou.txt' and place it in the 'data' directory."
            )
        self.wordlist_path = wordlist_path
        self.hash_type = hash_type
        self.max_threads = max_threads

    def _password_producer(self, password_queue: multiprocessing.Queue):
        """Produce passwords from wordlist"""
        try:
            with open(self.wordlist_path, "r", encoding="utf-8", errors="ignore") as f:
                for line_num, line in enumerate(f, 1):
                    password = line.strip()
                    if password:
                        password_queue.put(password)

                    if line_num % 50000 == 0:
                        print(f"Loaded {line_num} passwords...")

            # Signal end of production
            for _ in range(self.max_threads):
                password_queue.put(None)

        except Exception as e:
            print(f"Error reading wordlist: {e}")
            for _ in range(self.max_threads):
                password_queue.put(None)

    def _password_consumer(
        self, password_queue: multiprocessing.Queue, target_hash: str, result_queue: multiprocessing.Queue
    ):
        """Consume passwords and test against hash"""
        attempts = 0

        while True:
            password = password_queue.get()

            # Check for termination signal
            if password is None:
                break

            attempts += 1
            if attempts % 10000 == 0:
                # Note: Progress reporting from processes can be messy, but keeping it simple for now
                pass

            if verify_password(password, target_hash, self.hash_type):
                result_queue.put(password)
                return

        result_queue.put(None)

    def crack(self, target_hash: str) -> Optional[str]:
        """Perform dictionary attack"""
        print(f"Starting dictionary attack on {self.hash_type} hash")
        print(f"Using wordlist: {self.wordlist_path}")
        print(f"Using {self.max_threads} processes")

        password_queue = multiprocessing.Queue(maxsize=10000)
        result_queue = multiprocessing.Queue()

        # Start producer process
        producer_process = multiprocessing.Process(
            target=self._password_producer, args=(password_queue,)
        )
        producer_process.daemon = True
        producer_process.start()

        # Start consumer processes
        consumer_processes = []
        for _ in range(self.max_threads):
            process = multiprocessing.Process(
                target=self._password_consumer,
                args=(password_queue, target_hash, result_queue),
            )
            process.daemon = True
            process.start()
            consumer_processes.append(process)

        # Wait for a result
        found_password = None
        results_received = 0

        try:
            while results_received < self.max_threads and found_password is None:
                result = result_queue.get()
                if result is not None:
                    found_password = result
                    # Terminate other processes as soon as we find it
                    for p in consumer_processes:
                        p.terminate()
                    producer_process.terminate()
                results_received += 1
        except KeyboardInterrupt:
            print("\n[!] Attack interrupted by user")
            for p in consumer_processes:
                p.terminate()
            producer_process.terminate()
            raise

        return found_password
