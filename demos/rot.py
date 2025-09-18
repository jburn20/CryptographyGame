import string
import time
import sys

def rot13_word_animation(word):
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


# Example usage
rot13_word_animation("hello world")
