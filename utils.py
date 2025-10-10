# utils.py
import shutil
import os
import re

# --- ANSI Color Constants ---
RED = "\033[91m"  # Brighter red for better visibility
RESET = "\033[0m"
ANSI_ESCAPE = re.compile(r'\033\[[0-9;]*m')
UP = "\033[F" 
# --- Terminal Functions ---
def get_terminal_width():
    """Gets the current terminal width, with a fallback."""
    try:
        return shutil.get_terminal_size().columns
    except OSError:
        return 80

def center_text(text):
    """Centers text in the terminal, correctly handling ANSI color codes."""
    width = get_terminal_width()
    # Calculate visible length by removing ANSI codes before measuring
    visible_len = len(ANSI_ESCAPE.sub("", text))
    padding = max(0, (width - visible_len) // 2)
    return " " * padding + text

def clear_screen():
    """Clears the terminal screen for a clean slate."""
    os.system('cls' if os.name == 'nt' else 'clear')