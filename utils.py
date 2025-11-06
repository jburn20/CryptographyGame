# utils.py
import shutil
import os
import re

# --- ANSI Color Constants ---
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[1;33m"
GREY = "\033[90m"  # Add this new color
RESET = "\033[0m"
ANSI_ESCAPE = re.compile(r'\033\[[0-9;]*m')
UP = "\033[F" 
FAST = "\033[H"
FAST_CLEAR = "\033[H\033[2J"
# --- Terminal Functions ---
def get_terminal_width():
    """Gets the current terminal width, with a fallback."""
    try:
        return shutil.get_terminal_size().columns
    except OSError:
        return 80

def left_text(text, width=None, padding=2):
    """Left-aligns text within a given width, handling ANSI codes."""
    if width is None:
        width = get_terminal_width()
    
    # Calculate visible length
    visible_len = len(ANSI_ESCAPE.sub("", text))
    
    # Calculate padding needed to fill the width
    total_padding = max(0, width - visible_len - padding)
    
    # Return left-aligned text
    return " " * padding + text + " " * total_padding

def center_text(text, width=None):
    """Centers text in the terminal or a given width, handling ANSI color codes."""
    if width is None:
        width = get_terminal_width()
    
    # Calculate visible length by removing ANSI codes before measuring
    visible_len = len(ANSI_ESCAPE.sub("", text))
    padding = max(0, (width - visible_len) // 2)
    
    # Return centered text, ensuring it fills the width
    remaining_padding = max(0, width - visible_len - padding)
    return " " * padding + text + " " * remaining_padding

def right_text(text, width=None, padding=2):
    """Right-aligns text within a given width, handling ANSI codes."""
    if width is None:
        width = get_terminal_width()
    
    # Calculate visible length
    visible_len = len(ANSI_ESCAPE.sub("", text))
    
    # Calculate padding needed to push text to the right
    padding_left = max(0, (width - visible_len - padding))
    
    # Return right-aligned text
    return " " * padding_left + text + " " * padding

def clear_screen():
    """Clears the terminal screen for a clean slate."""
    os.system('cls' if os.name == 'nt' else 'clear')