import time
import random
import sys

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


if __name__ == "__main__":
    print("This is a visual demonstration of how the Caesar cipher works. \n" \
    "Each letter is shifted by the same value, which is then used to decode the message by shifting each letter back by the same amount.")
    caesar_demo("helloworld", shift=5, delay=0.09)
