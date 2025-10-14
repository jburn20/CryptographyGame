import os, time, shutil
import re
import random

# Colors
RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"

# ANSI-aware centering
def visible_len(text):
    return len(re.sub(r'\033\[[0-9;]*m', '', text))

def center_ansi(text):
    width = shutil.get_terminal_size().columns
    pad = max(0, (width - visible_len(text)) // 2)
    return " " * pad + text

# Bitwise XOR animation for a single byte
def xor_byte_animation(byte_val, xor_val, delay=0.45):
    bin_a = f"{byte_val:08b}"
    bin_b = f"{xor_val:08b}"
    result = ""

    for i in range(8):
        bit_a = int(bin_a[i])
        bit_b = int(bin_b[i])
        xor_bit = bit_a ^ bit_b
        result += str(xor_bit)

        # Determine color for current bits
        if bit_a == bit_b:
            color_a = color_b = RED  # same bits → false → red
        else:
            color_a = color_b = GREEN  # different bits → true → green

        # Build highlighted input bytes
        highlighted_a = ""
        highlighted_b = ""
        for j in range(8):
            if j == i:
                highlighted_a += f"{color_a}{bin_a[j]}{RESET}"
                highlighted_b += f"{color_b}{bin_b[j]}{RESET}"
            else:
                highlighted_a += bin_a[j]
                highlighted_b += bin_b[j]

        # Build highlighted result so far
        highlighted_result = ""
        for j, bit in enumerate(result):
            color = GREEN if bit == "1" else RED
            highlighted_result += f"{color}{bit}{RESET}"
        highlighted_result += "_" * (8 - len(result))

        os.system("cls" if os.name == "nt" else "clear")
        print(center_ansi("XOR Round Animation\n"))
        print(center_ansi(f"Original byte: {highlighted_a}"))
        print(center_ansi(f"XOR value    : {highlighted_b}\n"))
        print(center_ansi(f"Result so far: {highlighted_result}"))
        time.sleep(delay)

    final_val = byte_val ^ xor_val
    os.system("cls" if os.name == "nt" else "clear")
    print(center_ansi("XOR Round Animation - Byte Result\n"))
    print(center_ansi(f"{GREEN if final_val else RED}{final_val:08b}{RESET} (decimal {final_val})"))
    time.sleep(0.5)
    return final_val


# Apply XOR round animation to full state
def xor_round_animated(state, round_val=0x1F):
    new_state = []
    for idx, byte in enumerate(state):
        print(center_ansi(f"Processing byte {idx+1}/{len(state)}"))
        time.sleep(0.5)
        new_state.append(xor_byte_animation(byte, round_val))
    return new_state

# Other transformation functions


def rotate_left(state, n=1):
    return state[n:] + state[:n]

def rotate_right(state, n=1):
    return state[-n:] + state[:-n]

def shuffle_state(state):
    new_state = state[:]
    random.shuffle(new_state)
    return new_state

def rotate_animation(state, direction="left", n=1, delay=0.3):
    """
    Animate and perform rotation on the given state.
    direction: "left" or "right"
    n: number of positions to rotate
    """
    new_state = state[:]  # make a copy so original isn't affected until return
    direction = direction.lower()

    os.system("cls" if os.name == "nt" else "clear")
    print(center_ansi(f"Rotation {direction.upper()} Animation\n"))

    for step in range(n):
        # Perform actual rotation
        if direction == "left":
            new_state = new_state[1:] + new_state[:1]
        else:
            new_state = new_state[-1:] + new_state[:-1]

        # Show animation frame
        ascii_line = "ASCII:  "
        val_line = "Value:  "
        for i, val in enumerate(new_state):
            color = GREEN if i != 0 else RED  # highlight first (for visual motion)
            ascii_line += f"{color}{chr(val)}{RESET} "
            val_line += f"{color}{val:3}{RESET} "

        os.system("cls" if os.name == "nt" else "clear")
        print(center_ansi(f"Rotation {direction.upper()} Animation (step {step+1}/{n})\n"))
        print(center_ansi(ascii_line))
        print(center_ansi(val_line))
        time.sleep(delay)

    os.system("cls" if os.name == "nt" else "clear")
    print(center_ansi(f"Rotation {direction.upper()} Complete!\n"))
    final_ascii = " ".join(chr(x) for x in new_state)
    print(center_ansi(f"{GREEN}{final_ascii}{RESET}\n"))
    time.sleep(1)

    return new_state

def shuffle_animation(state, round_number=1, delay=1.5):
    """
    Educational shuffle animation for the Mini Hash Demo.
    Shows original row → arrows → shuffled row.
    """
    os.system("cls" if os.name == "nt" else "clear")
    
    print(center_ansi(f"STATE SHUFFLE\n"))
    
    # Original row
    original_row = "  ".join(chr(c) for c in state)
    print(center_ansi(original_row))
    
    # Arrows
    arrows_row = "  ".join("↓" for _ in state)
    print(center_ansi(arrows_row))
    
    # Deterministic shuffle for reproducibility
    shuffled_state = state[:]
    random.Random(round_number * 37).shuffle(shuffled_state)
    
    # Shuffled row (highlight green)
    shuffled_row = "  ".join(f"{GREEN}{chr(c)}{RESET}" for c in shuffled_state)
    print(center_ansi(shuffled_row))
    
    print()
    print(center_ansi(f"{GREEN}Shuffling spreads data across positions for better diffusion.{RESET}\n"))
    time.sleep(delay)
    
    return shuffled_state

# Animate non-XOR transformations
def animate_step(state, transform_name, new_state):
    os.system("cls" if os.name == "nt" else "clear")
    print(center_ansi(f"Mini Hash Demo - {transform_name}\n"))
    row_text = ""
    for val in new_state:
        color = RED if val > 127 else GREEN
        row_text += f"{color}{val:3}{RESET} "
    print(center_ansi(row_text))
    time.sleep(1)
    return new_state

# Display current state in ASCII and binary
def display_state(state):
    os.system("cls" if os.name == "nt" else "clear")
    print(center_ansi("Current State\n"))
    ascii_line = "ASCII:  "
    binary_line = "Binary: "
    for val in state:
        ascii_line += f"{chr(val)} "
        binary_line += f"{val:08b} "
    print(center_ansi(ascii_line))
    print(center_ansi(binary_line))
    time.sleep(1)

# Main interactive hash demo
def mini_hash_demo():
    input_string = input("Enter a string to hash: ").upper()
    current_state = [ord(c) for c in input_string]

    transform_map = {
        "1": ("XOR round", xor_round_animated),
        "2": ("Rotate left", rotate_left),
        "3": ("Rotate right", rotate_right),
        "4": ("Shuffle state", shuffle_state)
    }

    while True:
        display_state(current_state)
        print("\nChoose a function to apply next:")
        print("1 = XOR round, 2 = Rotate left, 3 = Rotate right, 4 = Shuffle state, Q = Quit")
        choice = input("Your choice: ").strip().upper()

        if choice == "Q" or choice == "q":
            break

        if choice not in transform_map:
            continue

        name, func = transform_map[choice]
        if name == "XOR round":
            current_state = func(current_state)
        elif name == "Rotate left":
            n = int(input("Rotate by how many positions? ") or 1)
            current_state = rotate_animation(current_state, "left", n)
        elif name == "Rotate right":
            n = int(input("Rotate by how many positions? ") or 1)
            current_state = rotate_animation(current_state, "right",n)
        elif name == "Shuffle state":
            
        # Use educational shuffle animation
            round_num = random.randint(1, 100)  # just to give a seed for demo
            current_state = shuffle_animation(current_state, round_num)
        else:
            current_state = animate_step(current_state, name, func(current_state))

    # Final hash as hex
    final_hash = "".join(f"{x:02X}" for x in current_state)
    os.system("cls" if os.name == "nt" else "clear")
    print(center_ansi("Mini Hash Demo - Final Hash\n"))
    print(center_ansi(f"{RED}{final_hash}{RESET}"))
    time.sleep(3)

# Run demo
mini_hash_demo()
