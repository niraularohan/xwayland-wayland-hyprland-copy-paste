#!/usr/bin/env python3
import subprocess

def command_exists(cmd):
    return subprocess.run(['which', cmd], capture_output=True).returncode == 0

def get_x11_clipboard():
    try:
        out = subprocess.run(['xclip', '-selection', 'clipboard', '-o'], capture_output=True, timeout=1)
        return out.stdout
    except:
        return b''

def set_wayland_clipboard(data):
    try:
        subprocess.run(['wl-copy'], input=data, check=True)
    except:
        pass

def main():
    for tool in ['wl-copy', 'xclip', 'clipnotify']:
        if not command_exists(tool):
            print(f"Error: '{tool}' not found in PATH.")
            return

    print("Starting clipboard sync: X11 → Wayland only (Ctrl+C to quit)")

    last_data = b''

    while True:
        try:
            # Wait for any clipboard change event on X11
            subprocess.run(['clipnotify'])
        except KeyboardInterrupt:
            print("\nClipboard sync stopped by user.")
            break
        except:
            continue

        x_data = get_x11_clipboard()

        if x_data and x_data != last_data:
            set_wayland_clipboard(x_data)
            last_data = x_data
            print("[X11 -> Wayland] Clipboard updated")

if __name__ == '__main__':
    main()

