# SEC-SUITE - Advanced Security Testing Toolkit

A comprehensive security testing toolkit with password cracking, network scanning, and security assessment tools.

## 🚀 New Features in v2.0

- **Markov Chain Password Attacks** - Generate realistic passwords using probability models
- **Brute Force Attacks** - Configurable character sets and length ranges
- **Modern Hash Support** - bcrypt, scrypt, and hash auto-detection
- **Multi-threading** - Dramatically improved performance
- **Network Scanner** - Multi-threaded port scanning
- **Advanced Keylogger** - Window title capture and stealth mode
- **Encoding Tools** - Base64, URL, HTML, and Hex encoding/decoding
- **Professional Logging** - Comprehensive logging system

## 📦 Installation

```bash
git clone https://github.com/gab-dev-7/sec-suite.git
cd sec-suite
pip install -r requirements.txt
🛠️ Usage
Password Cracking
bash
# Dictionary attack
python main.py crack -t <target_hash> -a sha256 -m dictionary -w data/rockyou.txt --threads 8

# Markov chain attack
python main.py crack -t <target_hash> -a md5 -m markov -w data/rockyou.txt --max-passwords 50000

# Brute force attack
python main.py crack -t <target_hash> -a sha1 -m bruteforce --charset "luds" --min-length 4 --max-length 6

# Auto-detect hash type
python main.py crack -t <target_hash> -m dictionary -w data/rockyou.txt
Network Scanning
bash
# Scan single host
python main.py scan -t 192.168.1.1 -p 1-1000 --threads 50

# Scan network range
python main.py scan -t 192.168.1.0/24 -p 22,80,443,3389
Keylogging
bash
# Basic keylogger
python main.py keylog -o keystrokes.txt

# Stealth mode with window capture
python main.py keylog -s --capture-window -o keylog.txt

# Timed keylogger
python main.py keylog -d 300 -o session.txt
Encoding/Decoding
bash
# Base64 encode
python main.py encode -d "hello world" -o encode -e base64

# URL decode
python main.py encode -d "hello%20world" -o decode -e url

# Hex encode
python main.py encode -d "secret" -o encode -e hex
🔧 Tools Overview
Password Cracking
Dictionary Attack: Traditional wordlist-based cracking

Markov Attack: Probability-based password generation

Brute Force: Exhaustive character combination testing

Rainbow Tables: Precomputed hash chains (basic)

Security Tools
Keylogger: Advanced logging with window context

Network Scanner: Multi-threaded port discovery

Encoder/Decoder: Multiple encoding scheme support

⚠️ Legal Disclaimer
This tool is for educational and authorized security testing purposes only. The developers are not responsible for any misuse or damage caused by this program. Always ensure you have proper authorization before testing any system.

🏗️ Project Structure
text
sec-suite/
├── main.py                 # Main CLI interface
├── cli.py                  # Command-line argument parser
├── attacks/                # Password cracking modules
│   ├── dictionary.py      # Dictionary attack
│   ├── markov.py          # Markov chain attack
│   ├── bruteforce.py      # Brute force attack
│   └── rainbow.py         # Rainbow table attack
├── tools/                  # Security tools
│   ├── keylogger.py       # Advanced keylogger
│   ├── network_scanner.py # Port scanner
│   └── encoder.py         # Encoding utilities
├── utils/                  # Core utilities
│   ├── banner.py          # Application banner
│   ├── crypto.py          # Cryptographic functions
│   └── password_analyzer.py
└── data/                   # Data files
    └── rockyou.txt        # Example wordlist
🎯 Advanced Usage
Markov Chain Attacks
Markov attacks use statistical models trained on real passwords to generate highly probable password candidates. This is effective against passwords that follow common patterns but aren't in standard wordlists.

Multi-threading
All cracking operations support multi-threading. Adjust the --threads parameter based on your CPU capabilities for optimal performance.

Hash Auto-detection
The tool can automatically detect common hash types based on length and format, making it easier to work with unknown hashes.

🤝 Contributing
Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

text

## Key Improvements Made:

1. **Markov Chain Attacks** - New probabilistic password generation
2. **Brute Force Attacks** - Configurable character sets and lengths  
3. **Modern Hash Support** - bcrypt, scrypt with proper salt handling
4. **Multi-threading** - All attacks now use multiple threads
5. **Hash Auto-detection** - Smart hash type identification
6. **New Tools** - Network scanner, advanced keylogger, encoder/decoder
7. **Professional Logging** - Comprehensive logging system
8. **Better CLI** - More intuitive command structure
9. **Enhanced Documentation** - Comprehensive README with examples

The tool is now much more powerful and professional, with enterprise-grade features while maintaining ease of use.
