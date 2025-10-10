import time, string, shutil, re, keyboard, os, sys, random
from utils import  UP, RED, RESET, get_terminal_width, center_text, clear_screen, ANSI_ESCAPE

demo_registry = {}
def register_demo(name):
    def decorator(func):
        demo_registry[name] = func
        return func
    return decorator

@register_demo("Caesar")

def caesar_demo(word="hello", shift=3, delay=0.21):
    def visible_len(text):
        return len(ANSI_ESCAPE.sub("", text))

    if shift is None:
        shift = random.randint(1, 25)

    bottom_row = ["." for _ in word]

    FRAME_LINES = 5

    # --- Initial Setup ---
    # Print the initial, static frame just once.
    print(center_text(f"Original word: {word}"))
    print(center_text(f"Shift amount: {shift}"))
    print() # Blank line
    print(center_text(" ".join(list(word))))
    print(center_text(" ".join(bottom_row)))
    
    time.sleep(1) # Pause before starting the animation
    
    for index, ch in enumerate(word):
        if not ch.isalpha():
            bottom_row[index] = ch
            continue # Skip animation for non-letters

        start = ord('a') if ch.islower() else ord('A')
        original_ord = ord(ch) - start

        # Animate the shift for the current letter
        for step in range(shift + 1):
            demo_ch = chr(start + ((original_ord + step) % 26))
            bottom_row[index] = demo_ch

            # --- Prepare the text for the two lines that change ---
            top_row_display = " ".join(
                f"{RED}{c}{RESET}" if j == index else c
                for j, c in enumerate(word)
            )
            bottom_row_display = " ".join(
                f"{RED}{c}{RESET}" if j == index else c
                for j, c in enumerate(bottom_row)
            )

            # --- Redraw only the changing lines ---
            sys.stdout.write(UP * 2) # Move cursor up 2 lines (to the top row)
            terminal_width = get_terminal_width()

            # Overwrite the old top and bottom rows
            sys.stdout.write(center_text(top_row_display).ljust(terminal_width) + "\n")
            sys.stdout.write(center_text(bottom_row_display).ljust(terminal_width) + "\n")
            
            sys.stdout.flush() # Force the update
            time.sleep(delay)

    # Move cursor to a new line after the animation is complete
    print("\n")
    print(center_text("Final Ciphertext: " + "".join(bottom_row)))

"""if __name__ == "__main__":
    print("This is a visual demonstration of how the Caesar cipher works. \n" \
    "Each letter is shifted by the same value, which is then used to decode the message by shifting each letter back by the same amount.")
    caesar_demo("helloworld", shift=5, delay=0.09)"""

@register_demo("Rot13")

def rot13_word_animation(word="helloworld"):

    shift = 13
    alphabet = list(string.ascii_lowercase)
    ciphered_display = [" " if c != " " else " " for c in word]

    last_frame_height = 0  # dynamically tracked

    def draw_frame(display_phrase, display_alphabet, display_cipher):
        nonlocal last_frame_height
        frame_lines = [
            center_text("ROT13 Demo: Letters move 13 slots through the alphabet"),
            center_text("Phrase : " + display_phrase),
            center_text("Alphabet: " + " ".join(display_alphabet)),
            center_text("Cipher  : " + " ".join(display_cipher))
        ]
        if last_frame_height:
            sys.stdout.write("\033[F" * last_frame_height)
        for line in frame_lines:
            sys.stdout.write("\033[2K")  # clear whole line regardless of width
            print(line)
        sys.stdout.flush()
        last_frame_height = len(frame_lines)


    # Print initial frame
    draw_frame(word, alphabet, ciphered_display)

    for idx, letter in enumerate(word):
        if not letter.isalpha():
            ciphered_display[idx] = letter
            draw_frame(word, alphabet, ciphered_display)
            continue

        current_index = alphabet.index(letter.lower())

        for step in range(1, shift + 1):
            display_alphabet = alphabet.copy()
            for s in range(step):
                trail_index = (current_index + s) % 26
                display_alphabet[trail_index] = f"{RED}{alphabet[trail_index]}{RESET}"

            moving_index = (current_index + step - 1) % 26
            display_alphabet[moving_index] = f"{RED}{alphabet[moving_index].upper()}{RESET}"

            display_phrase = "".join(
                (f"{RED}{c.upper()}{RESET}" if i == idx else c) for i, c in enumerate(word)
            )

            draw_frame(display_phrase, display_alphabet, ciphered_display)
            time.sleep(0.1)

        final_index = (current_index + shift) % 26
        ciphered_display[idx] = alphabet[final_index]

        display_alphabet = alphabet.copy()
        display_alphabet[final_index] = alphabet[final_index].upper()
        display_phrase = "".join(
            (c.upper() if i == idx else c) for i, c in enumerate(word)
        )

        draw_frame(display_phrase, display_alphabet, ciphered_display)
        time.sleep(0.15)

    print("\nFinal ciphered phrase:", "".join(ciphered_display))

@register_demo("Railfence")

def rail_fence_demo(word="HELLOWORLD", rails=3, delay=0.4):


    print(center_text("The rail fence cipher is a transposition cipher that writes characters in a zigzag pattern across a given number of rows(rails)."))

    header = f"Word: {word} | Rails: {rails}"
    print(center_text(header) + "\n")

    # Initialize rail structure
    fence = [["-" for _ in range(len(word))] for _ in range(rails)]

    # Print initial rails
    for row in fence:
        print(center_text(" ".join(row)))

    rail = 0
    direction = 1

    for col, ch in enumerate(word):
        # Place the letter in the correct rail
        fence[rail][col] = ch

        # Move cursor up to the start of rail lines
        sys.stdout.write(f"\033[{rails}F")  # move cursor up N lines
        # Print each rail line centered
        for row in fence:
            print(center_text(" ".join(row)))
        sys.stdout.flush()
        time.sleep(delay)

        # Move to next rail
        rail += direction
        if rail == 0 or rail == rails - 1:
            direction *= -1

    # Build final ciphertext
    cipher = "".join(ch for row in fence for ch in row if ch != "-")
    print("\n" + center_text("Final Ciphertext: " + cipher))

"""

if __name__ == "__main__":
    rail_fence_demo("HELLOWORLD", rails=3, delay=0.4)
"""

#! VIGENERE
@register_demo("Vigenere")
def vigenere_number_animation(plaintext="HELLO WORLD", key="KEY", delay=0.8):
    """
    Animates Vigenère cipher with numeric values without clearing entire terminal.
    """

    def center_text(text):
        width = shutil.get_terminal_size().columns
        return text.center(width)

    plaintext = plaintext.upper()
    key = key.upper()
    key_len = len(key)
    ciphertext = ""

    # Initial display of plaintext and aligned key
    aligned_key = [key[i % key_len] for i in range(len(plaintext))]
    print(center_text("Phrase:     " + " ".join(plaintext)))
    print(center_text("Key:        " + " ".join(aligned_key)))
    print(center_text("Calculation:"))
    print(center_text("Ciphertext:"))

    for i, p_char in enumerate(plaintext):
        if not p_char.isalpha():
            ciphertext += p_char
            continue

        k_char = key[i % key_len]

        # Numeric values
        p_num = ord(p_char) - ord('A')
        k_num = ord(k_char) - ord('A')
        c_num = (p_num + k_num) % 26
        c_char = chr(c_num + ord('A'))
        ciphertext += c_char

        # Build highlighted plaintext and key
        plaintext_display = " ".join(
            f"{RED}{c}{RESET}" if j == i else c
            for j, c in enumerate(plaintext)
        )
        key_display = " ".join(
            f"{RED}{key[j % key_len]}{RESET}" if j == i else key[j % key_len]
            for j in range(len(plaintext))
        )

        # Move cursor up 4 lines to overwrite previous output
        sys.stdout.write(UP*4)

        print(center_text("Phrase:     " + plaintext_display))
        print(center_text("Key:        " + key_display))
        print(center_text(f"Calculation: {p_char}={p_num} + {k_char}={k_num} -> {c_num} = {c_char}"))
        print(center_text("Ciphertext: " + " ".join(ciphertext)))

        time.sleep(delay)

#vigenere_number_animation("HELLO WORLD", "KEY", delay=1)

@register_demo("Circularbitshift")

def circular_bit_shift_animation(value=178, shift=5, direction='left', delay=0.5):
    """
    Animates circular bit shifts for an 8-bit integer.
    The same bit is highlighted in red as it moves across positions.
    
    value: integer 0-255
    shift: number of positions to shift
    direction: 'left' or 'right'
    delay: seconds between steps
    """

        
    if not 0 <= value <= 255:
        raise ValueError("Value must be 0-255 (8-bit).")

    bits = list(f"{value:08b}")  # 8-bit binary
    #clear_screen()

    print(center_text(f"Initial value: {value} -> {''.join(bits)}"))
    time.sleep(1.5)

    # Track the index of the bit we want to follow
    tracked_index = 0 if direction == 'left' else len(bits) - 1
    tracked_bit = bits[tracked_index]
    FRAME_LINES = 1
    for s in range(shift):
        sys.stdout.write(UP * FRAME_LINES)

        # Circular shift
        if direction == 'left':
            bit = bits.pop(0)
            bits.append(bit)
        else:  # right
            bit = bits.pop()
            bits.insert(0, bit)

        # Update tracked_index after shift
        if direction == 'left':
            tracked_index = (tracked_index - 1) % 8
        else:
            tracked_index = (tracked_index + 1) % 8

        # Build display with highlighted tracked bit
        bit_display = ""
        for i, b in enumerate(bits):
            if i == tracked_index:
                bit_display += f"{RED}{b}{RESET}"
            else:
                bit_display += b

        current_value = int(''.join(bits), 2)
        print(center_text(f"Shift {s+1}/{shift} ({direction}): {bit_display} -> {current_value}"))
        time.sleep(delay)

    print(center_text(f"Final value after {shift} circular {direction} shift: {current_value}"))
    time.sleep(1.99)

# Example usage:
#circular_bit_shift_animation(178, shift=5, direction='left', delay=0.9)
@register_demo("Columnar")

def columnar_demo():


    key = "KEY"
    plaintext = "HELLO_WORLD_"   # padded with underscores
    cols = len(key)
    rows = (len(plaintext) + cols - 1) // cols  # ceiling division
    grid = [[" " for _ in range(cols)] for _ in range(rows)]

    # Column order: 2 above col 0, 1 above col 1, 3 above col 2
    order = [2, 1, 3]

    def display(ciphertext="", highlight=None):
        """
        highlight: tuple (row, col) -> highlight the cell in red
        """
        os.system("cls" if os.name == "nt" else "clear")
        print("Columnar Transposition Cipher Demo\n")
        print(" K   E   Y")
        print(" 2   1   3")
        for r, row in enumerate(grid):
            line = []
            for c, x in enumerate(row):
                if highlight == (r, c):
                    line.append(f"[{RED}{x}{RESET}]")   # highlight in red
                else:
                    line.append(f"[{x}]")
            print(" ".join(line))
        print("\nCiphertext:", ciphertext)

    # Step 1: fill plaintext row by row
    for i, ch in enumerate(plaintext):
        r, c = divmod(i, cols)
        grid[r][c] = ch
        display()
        time.sleep(0.3)

    time.sleep(1)

    # Step 2: read ciphertext column by column in given order
    ciphertext = ""
    for col in sorted(range(cols), key=lambda x: order[x]):
        for row in range(rows):
            ciphertext += grid[row][col]
            display(ciphertext, highlight=(row, col))
            time.sleep(0.45)

    print("\nFinal Ciphertext:", ciphertext)

@register_demo("Vertical Spinner")

def vertical_spinner_alternating_demo(input_phrase="HELLO"):

    alphabet = string.ascii_uppercase
    input_phrase = input_phrase.upper()

    # Initialize columns with random shifts
    columns = []
    for ch in input_phrase:
        if ch not in alphabet:
            ch = "_"
            idx = 0
        else:
            idx = alphabet.index(ch)
        spins = random.randint(3, 10)  # random spin count per column
        top = alphabet[(idx - 1) % 26]
        middle = alphabet[idx]
        bottom = alphabet[(idx + 1) % 26]
        columns.append({
            "top": top,
            "middle": middle,
            "bottom": bottom,
            "idx": idx,
            "counter": spins
        })

    ciphertext = ""  # assembled ciphertext
    FRAME_LINES = 10
    print("\n" * FRAME_LINES)
    # Animate columns one at a time
    for col_num, col in enumerate(columns):
        shift_up = (col_num % 2 == 0)  # even columns up, odd columns down

        while col['counter'] > 0:
            sys.stdout.write(UP * FRAME_LINES)
            frame_buffer = []
            frame_buffer.append(center_text("Vertical Spinner Cipher Demo"))
            frame_buffer.append("") # For the newline

            counter_line = "Counter: "
            for c_num, c in enumerate(columns):
                counter_line += f"{c['counter']:2} " if c_num == col_num else " - "
            frame_buffer.append(center_text(counter_line))
            frame_buffer.append("") # For the newline

            for row_name in ["top", "middle", "bottom"]:
                row_text = f"{row_name.capitalize():<8}"
                for c_num, c in enumerate(columns):
                    row_text += f"{RED}{c[row_name]}{RESET} " if c_num == col_num else f"{c[row_name]} "
                frame_buffer.append(center_text(row_text))
            
            frame_buffer.append("") # Blank separator line
            frame_buffer.append(center_text(f"Ciphertext: {ciphertext}"))
            frame_buffer.append("") # For the final newline

            # --- Print the entire frame at once ---
            # We use .ljust() to ensure any previous text on a line is fully overwritten
            terminal_width = get_terminal_width()
            for line in frame_buffer:
                sys.stdout.write(line.ljust(terminal_width) + "\n")
            
            sys.stdout.flush() # Force the terminal to draw the update
            time.sleep(0.3)

            # --- (Shift column logic remains the same) ---
            if shift_up:
                col['top'], col['middle'] = col['middle'], col['bottom']
                col['idx'] = (col['idx'] + 1) % 26
                col['bottom'] = alphabet[(col['idx'] + 1) % 26]
            else:
                col['bottom'], col['middle'] = col['middle'], col['top']
                col['idx'] = (col['idx'] - 1) % 26
                col['top'] = alphabet[(col['idx'] - 1) % 26]
            
            col['counter'] -= 1

        ciphertext += col['middle']
    # Final display
    # Final display: middle letters (ciphertext) in red, others normal

    # Helper to compute visible length ignoring ANSI codes
    def visible_len(text):
        return len(re.sub(r'\033\[[0-9;]*m', '', text))

    # Center text while ignoring ANSI codes

    # Final display: middle letters in red, others normal
    print(center_text("Vertical Spinner Cipher Demo\n"))

    for row_name in ["top", "middle", "bottom"]:
        row_text = f"{row_name.capitalize():<8}"
        for c in columns:
            if row_name == "middle":
                row_text += f"{RED}{c[row_name]}{RESET} "
            else:
                row_text += f"{c[row_name]} "
        print(center_text(row_text))

    print()
    print(center_text(f"Ciphertext: {RED}{ciphertext}{RESET}"))
    time.sleep(3.5)

@register_demo("Playfair")

#!PLAYFAIR
def playfair_interactive_demo(plaintext="HELLO"):

    # 5x5 Playfair key grid (drop J)
    grid = [
        ['P','L','A','Y','F'],
        ['I','B','C','D','E'],
        ['G','H','K','M','N'],
        ['O','Q','R','S','T'],
        ['U','V','W','X','Z']
    ]

    def find_pos(ch):
        for r, row in enumerate(grid):
            for c, val in enumerate(row):
                if val == ch:
                    return r, c
        return None

    def display_grid(highlight=None):
        lines = []
        for r, row in enumerate(grid):
            line = ""
            for c, val in enumerate(row):
                if highlight and (r, c) in highlight:
                    line += f"{RED}{val}!{RESET}  "  # red highlight
                else:
                    line += f"{val}  "
            lines.append(line)
        return "\n".join(lines)

    # Prepare plaintext
    plaintext = plaintext.upper().replace("J","I").replace(" ", "")
    
    # Create digraphs
    digraphs = []
    i = 0
    while i < len(plaintext):
        a = plaintext[i]
        b = plaintext[i+1] if i+1 < len(plaintext) and plaintext[i+1] != a else 'X'
        digraphs.append(a+b)
        i += 2 if b != 'X' else 1

    history = []  # (plaintext, cipher)
    dig_index = 0
    sub_step = 0  # 0 = highlight original, 1 = show transformed

    while dig_index < len(digraphs):
        pair = digraphs[dig_index]
        r1, c1 = find_pos(pair[0])
        r2, c2 = find_pos(pair[1])

        # Compute transformed positions
        if r1 == r2:
            new_positions = [(r1, (c1+1)%5), (r2, (c2+1)%5)]
            rule = "Same Row -> Shift Right"
        elif c1 == c2:
            new_positions = [((r1+1)%5, c1), ((r2+1)%5, c2)]
            rule = "Same Column -> Shift Down"
        else:
            new_positions = [(r1, c2), (r2, c1)]
            rule = "Rectangle -> Swap Corners"

        # Reconstruct ciphertext from history
        ciphertext = "".join(c for _, c in history)

        os.system("cls" if os.name == "nt" else "clear")
        sys.stdout.write("Playfair Cipher Interactive Demo\n\n")
        
        if sub_step == 0:
            sys.stdout.write(display_grid(highlight=[(r1,c1),(r2,c2)]) + "\n\n")
            sys.stdout.write(f"Original digraph: {pair}\n")
            sys.stdout.write("Step A: Highlight plaintext pair. Press Enter to see transformation.\n")
        else:
            cipher_pair = "".join([grid[r][c] for r, c in new_positions])
            if len(history) <= dig_index:
                history.append((pair, cipher_pair))
            ciphertext = "".join(c for _, c in history)

            sys.stdout.write(display_grid(highlight=new_positions) + "\n\n")
            sys.stdout.write(f"Original digraph: {pair} | Rule: {rule}\n")
            sys.stdout.write("Step B: Transformation applied.\n")

        if history:
            sys.stdout.write("\nHistory (plaintext -> ciphertext):\n")
            for p, c in history:
                sys.stdout.write(f"{p} -> {c}\n")
        sys.stdout.write(f"\nCiphertext so far: {ciphertext}\n")
        sys.stdout.flush()

        choice = input("Press Enter/c to continue, b to go back, q to quit: ").lower().strip()
        if choice in ("", "c"):
            if sub_step == 0:
                sub_step = 1
            else:
                sub_step = 0
                dig_index += 1
        elif choice == "b":
            if sub_step == 1:
                sub_step = 0
                if history and history[-1][0] == pair:
                    history.pop()
            elif sub_step == 0:
                if dig_index > 0:
                    dig_index -= 1
                    sub_step = 1
                else:
                    print("Already at first step.")
        elif choice == "q":
            sys.stdout.write("\nDemo quit by user.\n")
            sys.stdout.flush()
            return
        else:
            print("Invalid input. Use Enter/c to continue, b to go back, q to quit.")

    sys.stdout.write(f"\nFinal Ciphertext: {ciphertext}\n")
    sys.stdout.flush()

# Run demo
#playfair_interactive_demo("HELLO")
