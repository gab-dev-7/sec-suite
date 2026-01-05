import os
import random
from typing import List, Set
from attacks.markov import MarkovModel
import pickle
from utils.password_analyzer import analyze_password_strength


class AdvancedPasswordGenerator:
    def __init__(self, training_file=None):
        self.markov = MarkovModel(order=3)
        self.trained = False
        if training_file and os.path.exists(training_file):
            self.train_from_file(training_file)

    def train_from_file(self, filepath):
        """Train Markov model from a password file"""
        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                passwords = [line.strip() for line in f if line.strip()]

            # Use a sample for training to avoid memory issues
            training_sample = min(len(passwords), 100000)
            self.markov.train(passwords[:training_sample])
            self.trained = True
            print(
                f"Trained Markov model with {len(passwords[:training_sample])} passwords"
            )

        except Exception as e:
            print(f"Error training from file: {e}")
            raise

    def generate_passwords(self, count=1000, min_length=6, max_length=16):
        """Generate passwords using Markov chain"""
        if not self.trained:
            raise ValueError("Model must be trained before generating passwords")

        passwords: Set[str] = set()
        attempts = 0
        max_attempts = count * 10

        while len(passwords) < count and attempts < max_attempts:
            pwd = self.markov.generate_password(max_length)
            if pwd and min_length <= len(pwd) <= max_length and pwd not in passwords:
                passwords.add(pwd)
            attempts += 1

        return list(passwords)

    def generate_password_with_fallback(
        self, min_length=6, max_length=16, max_attempts=1000
    ):
        """Generate a single password with length constraints"""
        if not self.trained:
            raise ValueError("Model must be trained before generating passwords")

        for _ in range(max_attempts):
            pwd = self.markov.generate_password(max_length)
            if pwd and min_length <= len(pwd) <= max_length:
                return pwd

        # Fallback: generate any password
        return self.markov.generate_password(max_length)

    def save_trained_model(self, filepath):
        """Save the trained Markov model using pickle"""
        with open(filepath, "wb") as f:
            pickle.dump(self.markov, f)
        print(f"Model saved to {filepath}")

    def load_trained_model(self, filepath):
        """Load a pre-trained Markov model"""
        if os.path.exists(filepath):
            with open(filepath, "rb") as f:
                self.markov = pickle.load(f)
            self.trained = True
            print(f"Model loaded from {filepath}")
        else:
            raise FileNotFoundError(f"Model file not found: {filepath}")


# Example usage
if __name__ == "__main__":
    generator = AdvancedPasswordGenerator("data/rockyou.txt")

    print("Generating 10 passwords...")
    passwords = generator.generate_passwords(count=10, min_length=8, max_length=12)

    for i, pwd in enumerate(passwords, 1):
        score = analyze_password_strength(pwd)
        print(f"{i:2d}. {pwd} (Score: {score}/100)")

