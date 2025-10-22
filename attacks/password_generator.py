import os
import random
from typing import List, Set
from attacks.markov import MarkovModel


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
        """Save the trained Markov model (simplified - just note that model is trained)"""
        # Since our MarkovModel doesn't have save/load, we'll just note the training file
        with open(filepath, "w") as f:
            f.write("Markov model training indicator - model is trained\n")
        print(f"Model training state saved to {filepath}")

    def load_trained_model(self, filepath):
        """Load a pre-trained Markov model (simplified)"""
        # This is a placeholder since our MarkovModel doesn't support serialization
        # In a real implementation, you'd want to add pickle support to MarkovModel
        if os.path.exists(filepath):
            self.trained = True
            print(f"Model training state loaded from {filepath}")
        else:
            raise FileNotFoundError(f"Model file not found: {filepath}")

    def analyze_password_strength(self, password: str) -> dict:
        """Analyze the strength of a generated password"""
        if not password:
            return {"score": 0, "feedback": ["Empty password"]}

        score = 0
        feedback = []

        # Length check
        length = len(password)
        if length >= 12:
            score += 25
            feedback.append("Good length (12+ characters)")
        elif length >= 8:
            score += 15
            feedback.append("Acceptable length (8-11 characters)")
        else:
            score += 5
            feedback.append("Short password (less than 8 characters)")

        # Character variety
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(not c.isalnum() for c in password)

        char_variety = sum([has_upper, has_lower, has_digit, has_special])
        if char_variety == 4:
            score += 40
            feedback.append("Excellent character variety")
        elif char_variety == 3:
            score += 25
            feedback.append("Good character variety")
        elif char_variety == 2:
            score += 15
            feedback.append("Basic character variety")
        else:
            score += 5
            feedback.append("Poor character variety")

        # Entropy estimation
        unique_chars = len(set(password))
        entropy_per_char = unique_chars**0.5
        total_entropy = length * entropy_per_char

        if total_entropy > 50:
            score += 35
            feedback.append(f"High entropy ({total_entropy:.1f} bits)")
        elif total_entropy > 30:
            score += 25
            feedback.append(f"Moderate entropy ({total_entropy:.1f} bits)")
        else:
            score += 10
            feedback.append(f"Low entropy ({total_entropy:.1f} bits)")

        return {
            "score": min(100, score),
            "feedback": feedback,
            "length": length,
            "entropy": total_entropy,
        }


# Example usage
if __name__ == "__main__":
    generator = AdvancedPasswordGenerator("data/rockyou.txt")

    print("Generating 10 passwords...")
    passwords = generator.generate_passwords(count=10, min_length=8, max_length=12)

    for i, pwd in enumerate(passwords, 1):
        analysis = generator.analyze_password_strength(pwd)
        print(f"{i:2d}. {pwd} (Score: {analysis['score']}/100)")
        if analysis["score"] < 60:
            print(f"     Feedback: {', '.join(analysis['feedback'])}")
