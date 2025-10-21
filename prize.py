import os, sys, json, time, shutil
from utils import clear_screen

def ensure_terminal_size(min_cols=80, min_rows=20):
    """Check if terminal is large enough for animation"""
    cols, rows = shutil.get_terminal_size(fallback=(80, 24))
    if cols < min_cols or rows < min_rows:
        print(f"[!] Terminal too small ({cols}x{rows}).")
        print(f"    Please resize to at least {min_cols}x{min_rows} for best experience.")
        input("Press Enter when ready...")
        # Recheck
        cols, rows = shutil.get_terminal_size(fallback=(80, 24))
        if cols < min_cols or rows < min_rows:
            print("Showing simplified version...")
            return False
    return True

def load_frames(path):
    """Load animation frames from JSON file"""
    try:
        with open(path) as f:
            data = json.load(f)
        return ["\n".join(frame) for frame in data]
    except FileNotFoundError:
        print(f"[X] Animation file not found: {path}")
        print("    Available animations:")
        prizes_dir = os.path.join(os.path.dirname(__file__), "prizes")
        if os.path.exists(prizes_dir):
            for f in os.listdir(prizes_dir):
                if f.endswith('.json'):
                    print(f"    - {f}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"[X] Invalid JSON in: {path}")
        sys.exit(1)

def scale_to_fit(frame_text):
    """Scale frame to fit terminal size"""
    cols, rows = shutil.get_terminal_size(fallback=(80, 24))
    lines = frame_text.splitlines()
    
    # Vertical scaling
    if len(lines) > rows - 2:  # Leave room for margins
        step = len(lines) / (rows - 2)
        lines = [lines[int(i * step)] for i in range(rows - 2)]
    
    # Horizontal scaling (truncate if needed)
    lines = [line[:cols] for line in lines]
    
    return "\n".join(lines)

def animate(frames, delay=0.07, loop=1):
    """Play animation frames"""
    clear_screen()
    sys.stdout.write("\033[H")
    
    for _ in range(loop):
        for frame in frames:
            sys.stdout.write("\033[H")
            print(scale_to_fit(frame))
            sys.stdout.flush()
            time.sleep(delay)
    
    # Show final frame
    sys.stdout.write("\033[H")
    print(scale_to_fit(frames[-1]))

if __name__ == "__main__":
    # Get file path from argument or use default
    if len(sys.argv) > 1:
        file = sys.argv[1]
    else:
        # Default to prizes directory
        file = os.path.join("prizes", "cat.json")
    
    # Ensure file exists, try relative to script location
    if not os.path.exists(file):
        script_dir = os.path.dirname(__file__)
        file = os.path.join(script_dir, file)
    
    print(f">> Loading animation: {os.path.basename(file)}")
    
    # Check terminal size
    if ensure_terminal_size(60, 20):
        frames = load_frames(file)
        print(f"   Frames: {len(frames)}")
        input("Press Enter to start animation...")
        animate(frames, delay=0.07, loop=1)
        print("\n[*] Animation complete!")
    else:
        print("[*] Enjoy your prize! (Terminal too small for animation)")
