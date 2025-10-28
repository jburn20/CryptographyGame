import os, time, shutil
import re
import random
from utils import RED, GREEN, YELLOW, RESET, center_text, clear_screen, ANSI_ESCAPE

# Bitwise XOR animation for a single byte
def xor_byte_animation(byte_val, xor_val, delay=0.22):
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

        clear_screen()
        print(center_text("XOR Round Animation\n"))
        print(center_text(f"Original byte: {highlighted_a}"))
        print(center_text(f"XOR value    : {highlighted_b}\n"))
        print(center_text(f"Result so far: {highlighted_result}"))
        time.sleep(delay)

    final_val = byte_val ^ xor_val
    clear_screen()
    print(center_text("XOR Round Animation - Byte Result\n"))
    print(center_text(f"{GREEN if final_val else RED}{final_val:08b}{RESET} (decimal {final_val})"))
    time.sleep(0.5)
    return final_val


# Apply XOR round animation to full state
def xor_round_animated(state, round_val=0x1F):
    new_state = []
    for idx, byte in enumerate(state):
        print(center_text(f"Processing byte {idx+1}/{len(state)}"))
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

    clear_screen()
    print(center_text(f"Rotation {direction.upper()} Animation\n"))

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
            # Handle non-printable characters
            char = chr(val) if 32 <= val < 127 else "?"
            ascii_line += f"{color}{char}{RESET} "
            val_line += f"{color}{val:3}{RESET} "

        clear_screen()
        print(center_text(f"Rotation {direction.upper()} Animation (step {step+1}/{n})\n"))
        print(center_text(ascii_line))
        print(center_text(val_line))
        time.sleep(delay)

    clear_screen()
    print(center_text(f"Rotation {direction.upper()} Complete!\n"))
    final_ascii = " ".join(chr(x) if 32 <= x < 127 else "?" for x in new_state)
    print(center_text(f"{GREEN}{final_ascii}{RESET}\n"))
    time.sleep(1)

    return new_state

def shuffle_animation(state, round_number=1, delay=1.5):
    """
    Educational shuffle animation for the Symmetric Cipher Demo.
    Shows original row → arrows → shuffled row.
    Returns the shuffled state and the original (before shuffle) state.
    """
    clear_screen()
    
    print(center_text(f"STATE SHUFFLE\n"))
    
    # Save the original state BEFORE shuffling
    original_state = state[:]
    
    # Original row
    original_row = "  ".join(chr(c) if 32 <= c < 127 else "?" for c in state)
    print(center_text(original_row))
    
    # Arrows
    arrows_row = "  ".join("↓" for _ in state)
    print(center_text(arrows_row))
    
    # Shuffle the state
    shuffled_state = state[:]
    random.Random(round_number * 37).shuffle(shuffled_state)
    
    # Shuffled row (highlight green)
    shuffled_row = "  ".join(f"{GREEN}{chr(c) if 32 <= c < 127 else '?'}{RESET}" for c in shuffled_state)
    print(center_text(shuffled_row))
    
    print()
    print(center_text(f"{GREEN}Shuffling spreads data across positions for better diffusion.{RESET}\n"))
    time.sleep(delay)
    
    return shuffled_state, original_state

# Animate non-XOR transformations
def animate_step(state, transform_name, new_state):
    clear_screen()
    print(center_text(f"Symmetric Cipher Demo - {transform_name}\n"))
    row_text = ""
    for val in new_state:
        color = RED if val > 127 else GREEN
        row_text += f"{color}{val:3}{RESET} "
    print(center_text(row_text))
    time.sleep(1)
    return new_state

def reverse_xor_animation(state, xor_val, delay=0.45):
    """Reverse XOR animation - same as forward since XOR is self-inverse"""
    for idx, byte in enumerate(state):
        bin_a = f"{byte:08b}"
        bin_b = f"{xor_val:08b}"
        
        clear_screen()
        print(center_text(f"REVERSING XOR - Byte {idx+1}/{len(state)}\n"))
        print(center_text(f"Hash byte: {bin_a}"))
        print(center_text(f"XOR(1F)  : {bin_b}"))
        
        reversed_byte = byte ^ xor_val
        result = f"{reversed_byte:08b}"
        
        print(center_text(f"Result   : {GREEN}{result}{RESET}"))
        time.sleep(delay)
        state[idx] = reversed_byte
    return state

def reverse_rotate_animation(state, direction, n, delay=0.3):
    """Reverse rotate animation - rotate in opposite direction"""
    reverse_direction = "right" if direction == "left" else "left"
    
    clear_screen()
    print(center_text(f"REVERSING ROTATE {direction.upper()} by {n} positions\n"))
    print(center_text(f"Rotating {reverse_direction.upper()} to undo...\n"))
    time.sleep(1)
    
    # Perform reverse rotation with animation
    for step in range(n):
        if reverse_direction == "left":
            state = state[1:] + state[:1]
        else:
            state = state[-1:] + state[:-1]
        
        ascii_line = "ASCII:  "
        val_line = "Value:  "
        for i, val in enumerate(state):
            color = GREEN if i != 0 else RED
            ascii_line += f"{color}{chr(val)}{RESET} "
            val_line += f"{color}{val:3}{RESET} "
        
        clear_screen()
        print(center_text(f"REVERSING ROTATE {direction.upper()} (step {step+1}/{n})\n"))
        print(center_text(ascii_line))
        print(center_text(val_line))
        time.sleep(delay)
    
    return state

def reverse_shuffle_animation(state, original_state, delay=1.5):
    """Reverse shuffle by showing the original (before shuffle) state"""
    clear_screen()
    
    print(center_text(f"REVERSING SHUFFLE\n"))
    
    # Shuffled row (current state)
    shuffled_row = "  ".join(chr(c) if 32 <= c < 127 else "?" for c in state)
    print(center_text(shuffled_row))
    
    # Arrows going up
    arrows_row = "  ".join("↑" for _ in state)
    print(center_text(arrows_row))
    
    # Unshuffled row (the original state we saved)
    unshuffled_row = "  ".join(f"{GREEN}{chr(c) if 32 <= c < 127 else '?'}{RESET}" for c in original_state)
    print(center_text(unshuffled_row))
    
    print()
    print(center_text(f"{GREEN}Unshuffling restores original order.{RESET}\n"))
    time.sleep(delay)
    
    return original_state

# Display current state in ASCII and binary
def display_state(state):
    clear_screen()
    print(center_text("Current State\n"))
    ascii_line = "ASCII:  "
    binary_line = "Binary: "
    hex_line = "Hex:    "
    for val in state:
        # Handle non-printable characters
        if 32 <= val < 127:
            ascii_line += f"{chr(val)} "
        else:
            ascii_line += f"{YELLOW}?{RESET} "
        binary_line += f"{val:08b} "
        hex_line += f"{val:02X} "
    print(center_text(ascii_line))
    print(center_text(binary_line))
    print(center_text(hex_line))
    time.sleep(1)

# Main interactive symmetric cipher demo
def mini_hash_demo():
    input_string = input("Enter a string to encrypt: ").upper()
    current_state = [ord(c) for c in input_string]
    
    # Track operation history for reversal
    operation_history = []

    transform_map = {
        "1": ("XOR round", xor_round_animated),
        "2": ("Rotate left", rotate_left),
        "3": ("Rotate right", rotate_right),
        "4": ("Shuffle state", shuffle_state)
    }

    while True:
        display_state(current_state)
        print("\n" + center_text("OPERATION HISTORY"))
        if operation_history:
            for idx, op in enumerate(operation_history, 1):
                if op[0] == "xor":
                    print(center_text(f"{idx}. XOR round"))
                elif op[0] == "rotate_left":
                    print(center_text(f"{idx}. Rotate left by {op[1]}"))
                elif op[0] == "rotate_right":
                    print(center_text(f"{idx}. Rotate right by {op[1]}"))
                elif op[0] == "shuffle":
                    print(center_text(f"{idx}. Shuffle"))
        else:
            print(center_text("(No operations yet)"))
        print()
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
            operation_history.append(("xor", 0x1F))
        elif name == "Rotate left":
            n = int(input("Rotate by how many positions? ") or 1)
            current_state = rotate_animation(current_state, "left", n)
            operation_history.append(("rotate_left", n))
        elif name == "Rotate right":
            n = int(input("Rotate by how many positions? ") or 1)
            current_state = rotate_animation(current_state, "right",n)
            operation_history.append(("rotate_right", n))
        elif name == "Shuffle state":
            # Use educational shuffle animation
            round_num = random.randint(1, 100)  # just to give a seed for demo
            # Store the original state before shuffling
            original_before_shuffle = current_state[:]
            current_state, _ = shuffle_animation(current_state, round_num)
            # Store operation with the original state for reversal
            operation_history.append(("shuffle", round_num, original_before_shuffle))
        else:
            current_state = animate_step(current_state, name, func(current_state))

    # Final result display with ASCII and binary
    clear_screen()
    print(center_text("Symmetric Cipher Demo - Final Result\n"))
    
    # Show ASCII representation
    ascii_result = "".join(chr(b) if 32 <= b < 127 else "?" for b in current_state)
    print(center_text(f"ASCII: {GREEN}{ascii_result}{RESET}"))
    
    # Show binary representation
    binary_line = " ".join(f"{b:08b}" for b in current_state)
    print(center_text(f"Binary: {binary_line}"))
    
    # Show hex representation
    final_hash = "".join(f"{x:02X}" for x in current_state)
    print(center_text(f"Hex: {RED}{final_hash}{RESET}"))
    
    time.sleep(2)
    
    # Show operation history
    clear_screen()
    print(center_text("OPERATION HISTORY\n"))
    print(center_text("=" * 50))
    for idx, op in enumerate(operation_history, 1):
        if op[0] == "xor":
            print(center_text(f"{idx}. XOR round (0x{op[1]:02X})"))
        elif op[0] == "rotate_left":
            print(center_text(f"{idx}. Rotate left by {op[1]} positions"))
        elif op[0] == "rotate_right":
            print(center_text(f"{idx}. Rotate right by {op[1]} positions"))
        elif op[0] == "shuffle":
            print(center_text(f"{idx}. Shuffle state"))
    print(center_text("=" * 50))
    
    print()
    input(center_text("Press Enter to see operations in reverse..."))
    
    # Automatically show reverse process
    reverse_hash_demo(current_state, operation_history)
    
    print()
    print(center_text("Demo complete!"))
    time.sleep(2)

def reverse_hash_demo(final_state, operation_history):
    """
    Demonstrates reversing a symmetric cipher by showing the reverse of all transformations.
    This demonstrates how symmetric ciphers are reversible when you know the algorithm and key.
    Real cryptographic hashes are designed to be one-way and non-reversible.
    """
    clear_screen()
    print(center_text("REVERSING CIPHER\n"))
    print(center_text(f"{GREEN}Reversing all operations to recover original plaintext...{RESET}\n"))
    print()
    
    state = final_state[:]
    
    # Reverse operations in reverse order
    for idx, op_tuple in enumerate(reversed(operation_history)):
        operation = op_tuple[0]
        
        clear_screen()
        print(center_text(f"REVERSING OPERATION {len(operation_history) - idx}/{len(operation_history)}\n"))
        
        if operation == "xor":
            param = op_tuple[1]
            state = reverse_xor_animation(state, param)
            
        elif operation == "rotate_left":
            param = op_tuple[1]
            state = reverse_rotate_animation(state, "left", param)
            
        elif operation == "rotate_right":
            param = op_tuple[1]
            state = reverse_rotate_animation(state, "right", param)
            
        elif operation == "shuffle":
            original_state = op_tuple[2] if len(op_tuple) > 2 else None
            if original_state:
                state = reverse_shuffle_animation(state, original_state)
        
        time.sleep(0.5)
    
    # Show the "unhashed" result
    clear_screen()
    print(center_text("REVERSING COMPLETE!\n"))
    
    # Show original ASCII
    original_ascii = "".join(chr(b) if 32 <= b < 127 else "?" for b in state)
    print(center_text(f"Original Plaintext: {GREEN}{original_ascii}{RESET}"))
    
    print()
    print(center_text(f"{GREEN}This demonstrates how reversible operations can be undone!{RESET}"))
    print(center_text(f"{YELLOW}Real cryptographic hashes use irreversible operations.{RESET}"))
    
    time.sleep(3)

if __name__ == "__main__":
    mini_hash_demo()
