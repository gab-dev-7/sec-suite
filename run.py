#!/usr/bin/env python3
"""
SEC-SUITE Launcher
Run this file to start the interactive interface
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from interactive_cli import main

    main()
except ImportError as e:
    print(f"Error: Could not start interactive interface - {e}")
    print("Falling back to command-line interface...")
    from main import main as cli_main

    cli_main()
