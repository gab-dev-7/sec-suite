# utils/banner.py
import random


def get_banner():
    """Returns a random ASCII art banner for the welcome screen."""
    banners = [
        # Banner 1: The Lock & Key
        """
╔══════════════════════════════════════╗
║                                      ║
║   🔐   PASSWORD    SECURITY   🔐     ║
║                                      ║
║   A Toolkit for Modern Cryptography  ║
║                                      ║
╚══════════════════════════════════════╝
        """,
        # Banner 2: The Terminal Hacker
        """
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓                                       ▓▓
▓▓  > P A S S W O R D - S E C U R I T Y  ▓▓
▓▓  > SUITE v1.0                         ▓▓
▓▓                                       ▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
        """,
        # Banner 3: The Matrix
        """
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░ P A S S W O R D ░ S E C U R I T Y ░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░ Wake up... They have everything  ░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
        """,
        # Banner 4: The Minimalist
        """
==================================
||  PASSWORD SECURITY SUITE     ||
||  ------------------------    ||
|| [Analyze | Generate | Crack] ||
==================================
        """,
    ]
    return random.choice(banners)


def clear_screen():
    """Clears the terminal screen."""
    import os

    os.system("cls" if os.name == "nt" else "clear")
