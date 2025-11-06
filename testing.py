import time
import sys
import os

# --- Try to import utils.py ---
# This assumes utils.py is in the same directory
try:
    import utils
except ImportError:
    print("Error: 'utils.py' not found.")
    print("Please make sure 'utils.py' is in the same directory as this script.")
    sys.exit(1)
# --- End of import ---

def run_full_scytale_animation(plaintext, cols, sleep_time=0.2, pause_time=2.0):
    """
    Runs the complete 4-part Scytale cipher animation as one function,
    using sys.stdout.write for a flicker-free experience.
    """

    # =========================================================================
    # --- NESTED HELPER FUNCTIONS FOR DRAWING ---
    # These functions build a list of strings (frame_buffer) and write it
    # all at once with sys.stdout.write to prevent flickering.
    # =========================================================================

    def _draw_part1_frame(grid_state, full_text, current_index, num_rows, num_cols, width):
        """Draws Part 1: Writing Plaintext"""
        frame_buffer = [utils.FAST_CLEAR] # Start with a screen clear and reset
        
        frame_buffer.append(utils.center_text("--- Part 1: Writing the Message (Row by Row) ---", width))
        
        # 1. Draw the Top Input Phrase
        top_phrase = "Plaintext: "
        if current_index == -1: # Final state
            top_phrase += full_text
        else:
            top_phrase += (
                full_text[:current_index]
                + utils.RED
                + full_text[current_index]
                + utils.RESET
                + full_text[current_index + 1 :]
            )
        frame_buffer.append(utils.center_text(top_phrase, width))
        frame_buffer.append("") # Newline

        # 2. Draw the Grid
        frame_buffer.append(utils.center_text("--- Scytale Grid ---", width))
        highlight_r, highlight_c = (-1, -1) if current_index == -1 else (current_index // num_cols, current_index % num_cols)
        
        for r in range(num_rows):
            row_str = ""
            for c in range(num_cols):
                char = grid_state[r][c]
                if r == highlight_r and c == highlight_c:
                    row_str += f"[{utils.RED}{char}{utils.RESET}] "
                elif char == " ":
                    row_str += f"[{utils.GREY}.{utils.RESET}] "
                else:
                    row_str += f"[{char}] "
            frame_buffer.append(utils.center_text(row_str.strip(), width))
        frame_buffer.append("") # Newline
        
        # Write the entire frame buffer to stdout at once
        sys.stdout.write("\n".join(frame_buffer))
        sys.stdout.flush()

    def _draw_part2_frame(grid_state, built_ciphertext, char_being_added, highlight_r, highlight_c, num_rows, num_cols, width):
        """Draws Part 2: Reading Ciphertext"""
        frame_buffer = [utils.FAST_CLEAR]

        frame_buffer.append(utils.center_text("--- Part 2: Reading the Ciphertext (Column by Column) ---", width))
        frame_buffer.append("")

        # 1. Draw the Grid
        for r in range(num_rows):
            row_str = ""
            for c in range(num_cols):
                char = grid_state[r][c]
                if r == highlight_r and c == highlight_c:
                    row_str += f"[{utils.RED}{char}{utils.RESET}] "
                else:
                    row_str += f"[{char}] "
            frame_buffer.append(utils.center_text(row_str.strip(), width))
        frame_buffer.append("")

        # 2. Draw the Ciphertext
        if char_being_added:
            display_text = f"Ciphertext: {built_ciphertext}{utils.RED}{char_being_added}{utils.RESET}"
        else:
            display_text = f"Ciphertext: {built_ciphertext}"
        frame_buffer.append(utils.center_text(display_text, width))
        frame_buffer.append("")
        
        sys.stdout.write("\n".join(frame_buffer))
        sys.stdout.flush()

    def _draw_part3_frame(grid_state, ciphertext, current_index, num_rows, num_cols, width):
        """Draws Part 3: Writing Ciphertext (Decrypt)"""
        frame_buffer = [utils.FAST_CLEAR]

        frame_buffer.append(utils.center_text("--- Part 3: Decrypting (Writing by Column) ---", width))

        # 1. Draw the Top Ciphertext Phrase
        top_phrase = "Ciphertext: "
        if current_index == -1: # Final state
            top_phrase += ciphertext
        else:
            top_phrase += (
                ciphertext[:current_index]
                + utils.RED
                + ciphertext[current_index]
                + utils.RESET
                + ciphertext[current_index + 1 :]
            )
        frame_buffer.append(utils.center_text(top_phrase, width))
        frame_buffer.append("")

        # 2. Draw the Grid
        frame_buffer.append(utils.center_text("--- Decryption Grid ---", width))
        highlight_r, highlight_c = (-1, -1) if current_index == -1 else (current_index % num_rows, current_index // num_rows)
        
        for r in range(num_rows):
            row_str = ""
            for c in range(num_cols):
                char = grid_state[r][c]
                if r == highlight_r and c == highlight_c:
                    row_str += f"[{utils.RED}{char}{utils.RESET}] "
                elif char == " ":
                    row_str += f"[{utils.GREY}.{utils.RESET}] "
                else:
                    row_str += f"[{char}] "
            frame_buffer.append(utils.center_text(row_str.strip(), width))
        frame_buffer.append("")
        
        sys.stdout.write("\n".join(frame_buffer))
        sys.stdout.flush()

    def _draw_part4_frame(grid_state, built_text, char_being_added, highlight_r, highlight_c, num_rows, num_cols, width):
        """Draws Part 4: Reading Original Text"""
        frame_buffer = [utils.FAST_CLEAR]
        
        frame_buffer.append(utils.center_text("--- Part 4: Reading the Original Message (Row by Row) ---", width))
        frame_buffer.append("")

        # 1. Draw the Grid
        for r in range(num_rows):
            row_str = ""
            for c in range(num_cols):
                char = grid_state[r][c]
                if r == highlight_r and c == highlight_c:
                    row_str += f"[{utils.RED}{char}{utils.RESET}] "
                else:
                    row_str += f"[{char}] "
            frame_buffer.append(utils.center_text(row_str.strip(), width))
        frame_buffer.append("")

        # 2. Draw the Final Decrypted Text
        if char_being_added:
            display_text = f"Original Text: {built_text}{utils.RED}{char_being_added}{utils.RESET}"
        else:
            display_text = f"Original Text: {built_text}"
        frame_buffer.append(utils.center_text(display_text, width))
        frame_buffer.append("")

        sys.stdout.write("\n".join(frame_buffer))
        sys.stdout.flush()

    # =========================================================================
    # --- MAIN ANIMATION LOGIC ---
    # =========================================================================

    try:
        # --- 1. Setup ---
        # Hide cursor
        sys.stdout.write("\033[?25l")
        
        width = utils.get_terminal_width()
        text_len = len(plaintext)
        rows = (text_len + cols - 1) // cols
        padded_text = plaintext + "@" * ((rows * cols) - text_len)
        
        # --- Part 1: Write Rows (Encrypt) ---
        grid = [[" " for _ in range(cols)] for _ in range(rows)]
        for i in range(len(padded_text)):
            r, c = i // cols, i % cols
            grid[r][c] = padded_text[i]
            _draw_part1_frame(grid, padded_text, i, rows, cols, width)
            time.sleep(sleep_time)
        
        _draw_part1_frame(grid, padded_text, -1, rows, cols, width)
        sys.stdout.write(utils.center_text("Part 1 Complete!", width) + "\n")
        sys.stdout.flush()
        time.sleep(pause_time)

        # --- Part 2: Read Cols (Encrypt) ---
        ciphertext = ""
        for c in range(cols):
            for r in range(rows):
                char_to_add = grid[r][c]
                _draw_part2_frame(grid, ciphertext, char_to_add, r, c, rows, cols, width)
                time.sleep(sleep_time)
                ciphertext += char_to_add
        
        _draw_part2_frame(grid, ciphertext, "", -1, -1, rows, cols, width)
        sys.stdout.write(utils.center_text("Ciphertext Complete!", width) + "\n")
        sys.stdout.flush()
        time.sleep(pause_time)

        # --- Part 3: Write Cols (Decrypt) ---
        grid3 = [[" " for _ in range(cols)] for _ in range(rows)]
        for i in range(len(ciphertext)):
            r, c = i % rows, i // rows
            grid3[r][c] = ciphertext[i]
            _draw_part3_frame(grid3, ciphertext, i, rows, cols, width)
            time.sleep(sleep_time)
            
        _draw_part3_frame(grid3, ciphertext, -1, rows, cols, width)
        sys.stdout.write(utils.center_text("Part 3 Complete! Grid is refilled.", width) + "\n")
        sys.stdout.flush()
        time.sleep(pause_time)

        # --- Part 4: Read Rows (Decrypt) ---
        original_text = ""
        for r in range(rows):
            for c in range(cols):
                char_to_add = grid3[r][c]
                _draw_part4_frame(grid3, original_text, char_to_add, r, c, rows, cols, width)
                time.sleep(sleep_time)
                original_text += char_to_add
        
        _draw_part4_frame(grid3, original_text, "", -1, -1, rows, cols, width)
        sys.stdout.write(utils.center_text("Decryption Complete!", width) + "\n")
        sys.stdout.flush()

    except KeyboardInterrupt:
        sys.stdout.write("\nAnimation stopped.\n")
    finally:
        # ALWAYS restore the terminal
        # Show cursor, reset colors
        sys.stdout.write(utils.RESET + "\033[?25h" + "\n")
        sys.stdout.flush()

# =============================================================================
# --- MAIN EXECUTION ---
# =============================================================================

if __name__ == "__main__":
    # Ensure terminal is in a sane state if utils.py is missing
    try:
        # Run the full animation
        run_full_scytale_animation(
            plaintext="ciphersarecool!",
            cols=5,
            sleep_time=0.15, # Faster animation
            pause_time=2.0
        )
    except NameError:
        # This will catch if 'utils' failed to import
        print("Failed to run animation due to import error.")