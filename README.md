# 🛡️ SEC-SUITE

> **Advanced Security Testing Toolkit & Password Analysis Engine**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Poetry](https://img.shields.io/badge/package-poetry-blueviolet)](https://python-poetry.org/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

**SEC-SUITE** is a comprehensive security toolkit designed for professionals, penetration testers, and educators. It unifies powerful password auditing capabilities with essential network reconnaissance tools in a single, modular interface.

Whether you prefer an **Interactive CLI** for ease of use or **Raw Terminal Commands** for automation, SEC-SUITE adapts to your workflow.

---

## 🚀 Key Features

| Category | Capabilities |
| :--- | :--- |
| **🔐 Password Attacks** | **Markov Chain** (Probabilistic), **Brute Force** (Configurable), **Dictionary** (Multi-process), **Rainbow Table** |
| **⚡ Performance** | **Multi-processing** across all attack modules for true parallelism, optimized password batching. |
| **🛡️ Modern Hashes** | Support for **Argon2**, **Bcrypt**, **Scrypt**, SHA-256/512, MD5, and more with auto-detection. |
| **📡 Network Ops** | Stealthy **SYN Port Scanner** (requires root/sudo), Service Discovery, CIDR support. |
| **🤖 Gen-AI** | **Advanced Password Generator** using trained Markov models to create realistic password lists. |
| **🛠️ Utilities** | **Encoding/Decoding** (Base64, Hex, URL, HTML), Password Strength Analyzer. |

---

## 📦 Quick Start

### Prerequisites
* Python 3.10 or higher
* [Poetry](https://python-poetry.org/) (Dependency Manager)

### Installation & Setup

1. **Clone the repository**
```bash
git clone https://github.com/gab-dev-7/sec-suite.git
cd sec-suite
```

2. **Install dependencies**
```bash
poetry install
```

3. **Activate the environment** (Important!)
```bash
poetry shell
```

*Note: This command enters the virtual environment. Your terminal prompt should change. You can now run the commands below without `poetry run`.*

---

## 🎮 Interactive Mode (Recommended)

For a user-friendly, menu-driven experience, start the tool with:

```bash
python run.py
```

The interactive mode provides access to all of SEC-SUITE's core features, including:
*   **Password Cracking**: Guided setup for Dictionary, Brute-force, and Markov attacks.
*   **Network Scanner**: A fully interactive interface for the SYN scanner.
*   **Password Generation**: Create customized password lists using trained Markov models.
*   **Hash Analysis & Encoding**: Easily access all the utility functions.

---

## 🛠️ CLI Usage (Advanced)

*(Ensure you have run `poetry shell` first)*

### 1. Password Cracking

<details>
<summary><strong>📖 Dictionary Attack</strong></summary>

High-performance, multi-process wordlist recovery. Automatically downloads `rockyou.txt` if missing.

```bash
python main.py crack -t <HASH> -a sha256 -m dictionary
```

</details>

<details>
<summary><strong>🧠 Markov Chain Attack</strong> (New in v2.0)</summary>

Probabilistic generation using machine learning models trained on real password databases.

```bash
python main.py crack -t <HASH> -a md5 -m markov --max-passwords 50000
```

</details>

<details>
<summary><strong>🔢 Brute Force</strong></summary>

Exhaustive, multi-process search with custom character sets (`l`=lower, `u`=upper, `d`=digits, `s`=special).

```bash
# Brute force a SHA1 hash, length 4-6, lowercase + digits
python main.py crack -t <HASH> -a sha1 -m bruteforce --charset "ld" --min-length 4 --max-length 6
```

</details>

<details>
<summary><strong>🌈 Rainbow Table</strong></summary>

Instant lookup using precomputed tables (now uses a secure JSON format).

```bash
python main.py crack -t <HASH> -m rainbow --rainbow-table my_table.json
```

</details>

### 2. Network Reconnaissance

The network scanner performs a **SYN Scan** (also known as a "half-open" scan), which is stealthier than a full TCP connect. This requires raw socket permissions.

⚠️ **Important:** You must run network scans with root privileges.

```bash
# Scan a single IP with sudo
sudo python main.py scan -t 192.168.1.5 -p 1-1000 --threads 50

# Scan a subnet (CIDR)
sudo python main.py scan -t 192.168.1.0/24 -p 22,80,443
```

### 3. Utilities & Encoders

```bash
# Analyze password strength
python main.py analyze -p "Sup3rS3cr3t!"

# Base64 Encode
python main.py encode -d "hello world" -e base64 -o encode

# URL Decode
python main.py encode -d "hello%20world" -e url -o decode
```

---

## ⚙️ Configuration

### Project Structure

```text
sec-suite/
├── attacks/          # Modular attack implementations
├── tools/            # Network scanner and Encoders
├── utils/            # Core logic (Hash detection, Crypto)
├── data/             # Wordlists (auto-downloads rockyou.txt)
└── main.py           # CLI Entry point
```

### Custom Wordlists

SEC-SUITE uses `data/rockyou.txt` by default. To use your own:

1. Place the file in the `data/` directory.
2. Run with the `-w` flag:
```bash
python main.py crack ... -w data/my_custom_list.txt
```

---

## ⚠️ Legal & Ethical Disclaimer

**SEC-SUITE is strictly for educational purposes, authorized security research, and personal auditing.**

* **DO NOT** use this tool against systems you do not own or do not have explicit permission to test.
* **DO NOT** use this tool for malicious purposes.

The developers assume no liability and are not responsible for any misuse or damage caused by this program. By using SEC-SUITE, you agree to these terms.

---

## 🤝 Contributing

We welcome contributions!

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

---

*SEC-SUITE v2.1 - Advanced Security Testing Toolkit*
