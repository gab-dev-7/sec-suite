# SEC-SUITE - Advanced Security Testing Toolkit v2.0

A comprehensive, multi-functional security testing toolkit designed for security professionals, penetration testers, and educational purposes. SEC-SUITE combines powerful password cracking capabilities with essential security tools in an intuitive interface.

## 🚀 What's New in v2.0

- **Markov Chain Password Attacks** - Advanced probabilistic password generation
- **Brute Force Attacks** - Configurable character sets and length ranges
- **Modern Hash Support** - bcrypt, scrypt, argon2 with proper salt handling
- **Multi-threading** - Dramatic performance improvements across all attacks
- **Network Security Tools** - Port scanner and network reconnaissance
- **Encoding Utilities** - Multiple encoding/decoding schemes
- **Interactive CLI** - User-friendly menu-driven interface
- **Hash Auto-detection** - Smart hash type identification
- **Professional Logging** - Comprehensive activity tracking

## 📦 Installation

### Prerequisites
- Python 3.10 or higher
- Poetry (for dependency management)

### Quick Setup
```bash
# Clone the repository
git clone https://github.com/gab-dev-7/sec-suite.git
cd sec-suite

# Install dependencies using Poetry
poetry install

# Run the interactive interface
poetry run python run.py
```

## 🎮 Interactive Interface (Recommended for Beginners)

Start the user-friendly menu system:

```bash
poetry run python run.py
```

Or alternatively:
```bash
poetry run python main.py interactive
```

### Interactive Features:
- **Number-based navigation** - Simply type numbers to select options
- **Clear menu hierarchy** - Organized categories with breadcrumb navigation
- **Input validation** - Handles invalid inputs gracefully
- **Visual feedback** - Emojis, headers, and formatted output
- **Back/Exit at every level** - Never get stuck in menus
- **Progress indicators** - Real-time operation status

## 🛠️ Command-Line Usage (Advanced Users)

### Password Cracking Tools

#### Dictionary Attack
```bash
poetry run python main.py crack -t <target_hash> -a sha256 -m dictionary -w data/rockyou.txt --threads 8
```

#### Markov Chain Attack
```bash
poetry run python main.py crack -t <target_hash> -a md5 -m markov -w data/rockyou.txt --max-passwords 50000
```

#### Brute Force Attack
```bash
poetry run python main.py crack -t <target_hash> -a sha1 -m bruteforce --charset "luds" --min-length 4 --max-length 6
```

#### Rainbow Table Attack
```bash
poetry run python main.py crack -t <target_hash> -m rainbow --rainbow-table my_table.rt
```

### Security Tools

#### Network Port Scanner
```bash
# Scan single host
poetry run python main.py scan -t 192.168.1.1 -p 1-1000 --threads 50

# Scan network range
poetry run python main.py scan -t 192.168.1.0/24 -p 22,80,443,3389
```

#### Encoding/Decoding Tools
```bash
# Base64 encode
poetry run python main.py encode -d "hello world" -o encode -e base64

# URL decode
poetry run python main.py encode -d "hello%20world" -o decode -e url

# Hex encode
poetry run python main.py encode -d "secret" -o encode -e hex

# HTML encode
poetry run python main.py encode -d "<script>alert('xss')</script>" -o encode -e html
```

### Password Analysis & Utilities

#### Password Strength Analysis
```bash
# Single password
poetry run python main.py analyze -p "MyPassword123!"

# Analyze password file
poetry run python main.py analyze -f passwords.txt
```

#### Password Hashing
```bash
# Hash a password
poetry run python main.py crack -p "mypassword" -a bcrypt

# Auto-detect hash type
poetry run python main.py crack -t "5e884898da28047151d0e56f8dc62927" -m dictionary
```

## 🔧 Tool Overview

### Password Cracking Capabilities

#### 1. Dictionary Attack
- **Description**: Traditional wordlist-based password recovery
- **Features**: 
  - Multi-threaded processing
  - Support for large wordlists (with automatic download of `rockyou.txt`)
  - Progress tracking
- **Best For**: Common passwords, dictionary words

#### 2. Markov Chain Attack
- **Description**: Probability-based password generation using machine learning
- **Features**:
  - Trains on real password databases
  - Generates realistic password candidates
  - Configurable generation limits
  - Multi-threaded execution
- **Best For**: Pattern-based passwords, human-generated passwords

#### 3. Brute Force Attack
- **Description**: Exhaustive character combination testing
- **Features**:
  - Configurable character sets:
    - `l` - lowercase letters
    - `u` - uppercase letters  
    - `d` - digits
    - `s` - special characters
  - Custom length ranges
  - Progress estimation
  - Early termination on success
- **Best For**: Short passwords, known character sets

#### 4. Rainbow Table Attack
- **Description**: Precomputed hash lookup tables
- **Features**:
  - Instant password recovery for known hashes
  - Support for custom rainbow tables
  - Multiple table formats
- **Best For**: Fast recovery of common hashes

### Supported Hash Algorithms

| Algorithm | Status | Notes |
|-----------|--------|-------|
| MD5 | ✅ Supported | Fast but insecure |
| SHA-1 | ✅ Supported | Deprecated, use with caution |
| SHA-256 | ✅ Supported | Current standard |
| SHA-512 | ✅ Supported | High security |
| bcrypt | ✅ Supported | Modern, slow hashing |
| scrypt | ✅ Supported | Memory-hard function |
| argon2 | ✅ Supported | State-of-the-art |

### Security Tools

#### Network Scanner
- Multi-threaded port scanning
- CIDR notation support
- Custom port ranges
- Host discovery
- Service detection

#### Encoding/Decoding Utilities
- Base64 encoding/decoding
- URL encoding/decoding  
- HTML entity encoding/decoding
- Hexadecimal encoding/decoding

## 📁 Project Structure

```
sec-suite/
├── main.py                     # Main command-line interface
├── run.py                      # Interactive mode launcher
├── interactive_cli.py          # Interactive menu system
├── pyproject.toml              # Python dependencies (managed by Poetry)
│
├── attacks/                    # Password cracking modules
│   ├── dictionary.py           # Dictionary attack implementation
│   ├── markov.py               # Markov chain attack
│   ├── bruteforce.py           # Brute force attack
│   └── rainbow.py              # Rainbow table attack
│
├── tools/                      # Security utilities
│   ├── network_scanner.py      # Port scanning
│   └── encoder.py              # Encoding/decoding
│
├── utils/                      # Core utilities
│   ├── banner.py               # Application branding
│   ├── crypto.py               # Cryptographic functions
│   ├── password_analyzer.py    # Strength analysis
│   └── data_downloader.py      # Automatic wordlist downloader
│
└── data/                       # Data files (e.g., rockyou.txt)
    └── .gitkeep
```

## 🎯 Advanced Usage Examples

### Comprehensive Password Audit
```bash
# Step 1: Analyze password strength
poetry run python main.py analyze -f user_passwords.txt

# Step 2: Test against common hashes
poetry run python main.py crack -t "5d41402abc4b2a76b9719d911017c592" -m dictionary

# Step 3: Brute force short passwords
poetry run python main.py crack -t "7c6a180b36896a0a8c02787eeafb0e4c" -m bruteforce --min-length 1 --max-length 4
```

### Network Security Assessment
```bash
# Discover live hosts and open ports
poetry run python main.py scan -t 192.168.1.0/24 -p 21,22,23,80,443,3389

# Generate report of network services
poetry run python main.py scan -t 10.0.0.1-50 -p 1-1000 --threads 100
```

### Password Hash Analysis
```bash
# Identify unknown hash types
poetry run python main.py crack -t "e10adc3949ba59abbe56e057f20f883e" -m dictionary

# Test multiple hash algorithms
for algo in md5 sha1 sha256 sha512; do
    poetry run python main.py crack -p "password123" -a $algo
done
```

## ⚙️ Configuration

### Custom Wordlists
Place your wordlist files in the `data/` directory. The application will use `data/rockyou.txt` by default and will download it if it's missing.
```bash
cp my_wordlist.txt data/
poetry run python main.py crack -t <hash> -m dictionary -w data/my_wordlist.txt
```

### Thread Configuration
Adjust thread counts based on your system:
- **Dictionary attacks**: 4-8 threads
- **Brute force**: 2-4 threads per length
- **Network scanning**: 50-100 threads
- **Markov attacks**: 4-8 threads

### Logging
All operations are logged to `sec-suite.log`:
```bash
tail -f sec-suite.log  # Monitor real-time activity
```

## 🔒 Legal & Ethical Usage

### ⚠️ IMPORTANT DISCLAIMER

SEC-SUITE is designed for:

- ✅ Educational purposes and security research
- ✅ Authorized penetration testing
- ✅ Personal security auditing (your own systems)
- ✅ Academic research and learning

### ❌ PROHIBITED USES

- Unauthorized testing of systems you don't own
- Malicious hacking activities  
- Password cracking without explicit permission
- Any illegal cybersecurity activities

### Compliance Notice
Users are solely responsible for ensuring they have proper authorization before using these tools. The developers assume no liability for misuse of this software.

## 🐛 Troubleshooting

### Common Issues

**Import errors:**
```bash
# Reinstall dependencies with Poetry
poetry install
```

**Missing wordlists:**
The `rockyou.txt` wordlist will be downloaded automatically on first use if it's missing. If you want to use a different wordlist, place it in the `data/` directory.

**Performance issues:**
- Reduce thread count with `--threads` parameter
- Use smaller wordlists for testing
- Close other resource-intensive applications

### Getting Help

1. Check the `sec-suite.log` file for detailed error information
2. Ensure all dependencies are properly installed
3. Verify Python version (3.10+ required)
4. Check file permissions and paths

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup
```bash
git clone https://github.com/gab-dev-7/sec-suite.git
cd sec-suite
poetry install
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by various security tools and frameworks
- Thanks to the security research community
- Contributors and testers who helped improve SEC-SUITE
- Open-source libraries that make this project possible

## 📞 Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/gab-dev-7/sec-suite/issues)
- **Documentation**: Check the `docs/` directory for detailed guides
- **Community**: Share experiences and tips with other users

---

**Remember**: With great power comes great responsibility. Use SEC-SUITE ethically and legally! 🔐

*SEC-SUITE v2.0 - Advanced Security Testing Toolkit*
