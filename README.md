
# 🔐 Password Security Suite

A comprehensive, educational, and practical command-line toolkit for exploring password security, cryptography, and cracking techniques.

![ASCII Art Banner](https://i.imgur.com/your-gif-here.gif) <!-- You can create a GIF of your tool in action later! -->

## Features

- **🔢 Password Entropy Calculator:** Quantitatively measures password strength using information theory.
- **🔑 Secure Password Generator:** Creates cryptographically secure random passwords with customizable rules.
- **🧮 Cryptographic Hashing:** Hashes passwords using standard algorithms like SHA-256.
- **📚 Dictionary Attack:** Simulates a basic cracking attack using a wordlist.
- **🌈 Rainbow Table Attack:** Implements a sophisticated time-memory trade-off attack to crack hashes without a massive wordlist.

## Installation

Get up and running in seconds.

1. **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/password-security-suite.git
    cd password-security-suite
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Run the application:**

    ```bash
    python main.py
    ```

## Usage

The suite is driven by an interactive menu. Simply run `python main.py` and follow the on-screen prompts.

### Example Walkthrough

1. **Calculate Entropy:** Choose option `1` from the main menu, then enter a password like `MyP@ssw0rd123!` to see its entropy in bits.
2. **Generate a Rainbow Table:**
    - Choose option `4` (Rainbow Table Utilities).
    - Choose option `1` (Generate Table).
    - Enter the parameters when prompted (e.g., charset `abcd`, chains `5000`, length `50`, password length `4`).
3. **Crack a Hash:**
    - First, get a hash for a known password using option `3`.
    - Then, go into Rainbow Table Utilities (`4`) and choose option `2` (Crack Hash).
    - Paste the hash and select the table file you generated.

## How It Works

This project is a practical exploration of concepts from discrete mathematics and cybersecurity.

### Dictionary Attack

This is the simplest cracking method. It takes a hash and iterates through every word in a list (a "wordlist"), hashing each one and comparing it to the target hash. It's fast but only effective against passwords that are common words.

### Rainbow Tables

A rainbow table is a pre-computed table for reversing cryptographic hash functions. It's a time-memory trade-off:

- **Time-Intensive Generation:** We spend a lot of time upfront generating chains of `hash -> reduce -> hash -> reduce...` and storing only the start and end points.
- **Fast Cracking:** To crack a hash, we don't need to re-generate everything. We can perform a lookup to see if the hash could be part of a chain, and if so, re-compute just that one chain to find the original password. This allows cracking passwords that would be infeasible with a pure dictionary attack on a small character set.

## Project Structure

password-security-suite/
├── main.py # Entry point of the application
├── cli.py # Interactive menu and user interface logic
├── utils/
│ ├── init.py
│ ├── password_analyzer.py # Entropy and generation logic
│ └── crypto.py # Hashing logic
└── attacks/
├── init.py
├── dictionary.py # Dictionary attack implementation
└── rainbow.py # Rainbow table generation and cracking

## Future Enhancements

- [ ] **Markov Chain Cracker:** Implement a probabilistic model for more intelligent password guessing.
- [ ] **Multiprocessing:** Speed up rainbow table generation using parallel processing.
- [ ] **More Hash Algorithms:** Add support for MD5, SHA1, etc.
- [ ] **GUI Version:** Create a graphical user interface using Tkinter or PyQt.
