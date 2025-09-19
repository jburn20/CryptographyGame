import time, string
import os, sys, random
demo_registry = {}

def register_demo(name):
    def decorator(func):
        demo_registry[name] = func
        return func
    return decorator
@register_demo("Caesar")
def caesar_demo(word="hello", shift=None, delay=0.1):
    if shift is None:
        shift = random.randint(1, 25)

    print(f"Original word: {word}")
    print(f"Shift amount: {shift}\n")

    # Prepare top and bottom rows
    top_row = " ".join(list(word))
    bottom_row = ["." for _ in word]

    # Print top row once
    print(top_row)

    # Print bottom row (will update in place)
    sys.stdout.write(" ".join(bottom_row))
    sys.stdout.flush()

    for i, ch in enumerate(word):
        if ch.isalpha():
            start = ord('A') if ch.isupper() else ord('a')
            original_ord = ord(ch) - start
            new_ord = (original_ord + shift) % 26
            new_ch = chr(start + new_ord)

            # Animate this letter shifting
            for step in range(shift + 1):
                demo_ch = chr(start + ((original_ord + step) % 26))
                bottom_row[i] = demo_ch
                # Move cursor back to overwrite bottom row
                sys.stdout.write("\r" + " ".join(bottom_row))
                sys.stdout.flush()
                time.sleep(delay)

            # Lock in final letter
            bottom_row[i] = new_ch
            sys.stdout.write("\r" + " ".join(bottom_row))
            sys.stdout.flush()
        else:
            bottom_row[i] = ch

    print("\n\nFinal Ciphertext:", "".join(bottom_row))


"""
if __name__ == "__main__":
    print("This is a visual demonstration of how the Caesar cipher works. \n" \
    "Each letter is shifted by the same value, which is then used to decode the message by shifting each letter back by the same amount.")
    caesar_demo("helloworld", shift=5, delay=0.09)
"""
@register_demo("Rot13")
def rot13_word_animation(word="helloworld"):
    shift = 13
    alphabet = list(string.ascii_lowercase)

    # Initialize ciphered display
    ciphered_display = [" " if c != " " else " " for c in word]

    print("ROT13 Demo: Letters move 13 slots through the alphabet")
    print("Phrase : " + word)
    print("Alphabet: " + " ".join(alphabet))
    print("Cipher  : " + " ".join(ciphered_display))

    for idx, letter in enumerate(word):
        if not letter.isalpha():
            ciphered_display[idx] = letter
            sys.stdout.write("\033[F")  # Move cursor up one line to overwrite cipher
            print("Cipher  : " + " ".join(ciphered_display))
            continue

        current_index = alphabet.index(letter.lower())

        # Animate letter moving 13 slots
        for step in range(1, shift + 1):
            display_alphabet = alphabet.copy()
            for s in range(step - 1):
                display_alphabet[(current_index + s) % 26] = "."
            moving_index = (current_index + step - 1) % 26
            display_alphabet[moving_index] = alphabet[moving_index].upper()

            # Move cursor up 3 lines to overwrite Phrase, Alphabet, Cipher
            sys.stdout.write("\033[F\033[F\033[F")

            # Build display phrase with spaces around current letter for highlighting
            display_phrase = "".join(
                (f" {c.upper()} " if i == idx else c) for i, c in enumerate(word)
            )

            print("Phrase : " + display_phrase)
            print("Alphabet: " + " ".join(display_alphabet))
            print("Cipher  : " + " ".join(ciphered_display))
            time.sleep(0.1)

        # Finalize cipher letter
        final_index = (current_index + shift) % 26
        ciphered_display[idx] = alphabet[final_index]

        # Update final display in-place
        sys.stdout.write("\033[F\033[F\033[F")
        display_alphabet = alphabet.copy()
        display_alphabet[final_index] = alphabet[final_index].upper()
        display_phrase = "".join(
            (f" {c.upper()} " if i == idx else c) for i, c in enumerate(word)
        )
        print("Phrase : " + display_phrase)
        print("Alphabet: " + " ".join(display_alphabet))
        print("Cipher  : " + " ".join(ciphered_display))
        time.sleep(0.15)

    print("\nFinal ciphered phrase:", "".join(ciphered_display))


#! Example usage
#rot13_word_animation("hello world")
@register_demo("Railfence")

def rail_fence_demo(word="HELLOWORLD", rails=3, delay=0.4):
    print("The rail fence cipher is a transposition cipher that writes characters in a zigzag pattern across a given number of rows(rails).")

    header = f"Word: {word} | Rails: {rails}"
    print(header, "\n")
    

    # Initialize rail structure
    fence = [["-" for _ in range(len(word))] for _ in range(rails)]

    # Print initial rails
    for row in fence:
        print(" ".join(row))

    rail = 0
    direction = 1

    for col, ch in enumerate(word):
        # Place the letter in the correct rail
        fence[rail][col] = ch

        # Move cursor up to the start of rail lines
        sys.stdout.write(f"\033[{rails}F")  # move cursor up N lines
        # Print each rail line
        for row in fence:
            print(" ".join(row))
        # Move cursor down again so next print is after rails
        sys.stdout.flush()
        time.sleep(delay)

        # Move to next rail
        rail += direction
        if rail == 0 or rail == rails - 1:
            direction *= -1

    # Build final ciphertext
    cipher = "".join(ch for row in fence for ch in row if ch != "-")
    print("\nFinal Ciphertext:", cipher)

"""

if __name__ == "__main__":
    rail_fence_demo("HELLOWORLD", rails=3, delay=0.4)
"""
@register_demo("Vigenere")
def vigenere_number_animation(plaintext="HELLO WORLD", key="KEY", delay=0.8):
    """
    Animates Vigenère cipher with numeric values.
    
    Shows:
    1. Highlighted current plaintext and key letters
    2. Their numeric values (A=0..Z=25)
    3. Sum modulo 26
    4. Builds ciphertext in real-time
    """
    plaintext = plaintext.upper()
    key = key.upper()
    key_len = len(key)
    ciphertext = ""
    print("Plaintext: ", end="")
    for char in plaintext:
        print(char, end=" ",flush=True) #! flush=True or else it wont display on powershell
    print()
    
    print("Key:       ", end="")
    for i in range(len(plaintext)):
        aligned_key_char = key[i % key_len]
        print(aligned_key_char, end=" ",flush=True) #! flush=True “send whatever is in the buffer to the terminal immediately”
        time.sleep(0.35)
    
    for i, p_char in enumerate(plaintext):
        os.system('cls' if os.name == 'nt' else 'clear')
        
        #* Skip non-alphabet characters (space, punctuation)
        if not p_char.isalpha():
            ciphertext += p_char
            continue
        
        k_char = key[i % key_len]
        
        #* Numeric values (A=0)
        p_num = (ord(p_char)+ 1 )- ord('A') 
        k_num = (ord(k_char)+ 1 )- ord('A')
        c_num = (p_num + k_num) % 26
        c_char = chr(c_num + ord('A')-1)
        ciphertext += c_char
        
        #* Print plaintext with highlight
        print("Phrase:    ", end="")
        for j, c in enumerate(plaintext):
            print(f"[{c}]" if j == i else c, end="")
        print()
        
        #* Print key with highlight
        print("Key:       ", end="")
        for j in range(len(plaintext)):
            kc = key[j % key_len]
            print(f"[{kc}]" if j == i else kc, end="")
        print()
        
        #* Show numeric calculation
        print(f"\nCalculation: {p_char}={p_num} + {k_char}={k_num} -> {c_num} = {c_char}")
        
        #* Show current ciphertext
        print("\nCiphertext:", end=" ")
        for c in ciphertext:
            print(c, end=" ")
        print("\n")
        
        time.sleep(delay)

#! Example usage
#vigenere_number_animation("HELLO WORLD", "KEY", delay=1)
@register_demo("Circularbitshift")
def circular_bit_shift_animation(value=178, shift=5, direction='left', delay=0.5):
    """
    Animates circular bit shifts for an 8-bit integer.
    
    value: integer 0-255
    shift: number of positions to shift
    direction: 'left' or 'right'
    delay: seconds between steps
    """
    if not 0 <= value <= 255:
        raise ValueError("Value must be 0-255 (8-bit).")
    os.system('cls' if os.name == 'nt' else 'clear')
    
    bits = list(f"{value:08b}")  # Convert to 8-bit binary list
    
    print(f"Initial value: {value} -> {''.join(bits)}")
    time.sleep(1.75)
    
    for s in range(shift):
        os.system('cls' if os.name == 'nt' else 'clear')
        
        if direction == 'left':
            shifted_bit = bits.pop(0)
            bits.append(shifted_bit)
        elif direction == 'right':
            shifted_bit = bits.pop()
            bits.insert(0, shifted_bit)
        else:
            raise ValueError("Direction must be 'left' or 'right'.")
        
        current_value = int(''.join(bits), 2)
        print(f"Shift {s+1}/{shift} ({direction}): {''.join(bits)} -> {current_value}")
        time.sleep(delay)
    
    print(f"\nFinal value after {shift} circular {direction} shift: {current_value}")

# Example usage:
#circular_bit_shift_animation(178, shift=5, direction='left', delay=0.9)
