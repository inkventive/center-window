import win32gui
import win32con
import win32api
import ctypes
import time
import keyboard

# List of known tricky emulator titles
KNOWN_WINDOW_TITLES = [
    "MSI App Player",
    "BlueStacks",
    "NoxPlayer",
    "LDPlayer",
    "Memu",
    "GameLoop",
    "Emulator",
    "Android Emulator"
]

def is_visible_and_valid(hwnd):
    if not win32gui.IsWindowVisible(hwnd):
        return False
    if not win32gui.GetWindowText(hwnd):
        return False
    return True

def center_window(hwnd):
    rect = win32gui.GetWindowRect(hwnd)
    width = rect[2] - rect[0]
    height = rect[3] - rect[1]

    screen_width = ctypes.windll.user32.GetSystemMetrics(0)
    screen_height = ctypes.windll.user32.GetSystemMetrics(1)

    x = int((screen_width - width) / 2)
    y = int((screen_height - height) / 2)

    # Restore minimized windows
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    time.sleep(0.1)

    # Move the window
    win32gui.MoveWindow(hwnd, x, y, width, height, True)
    print(f"✅ Moved: {win32gui.GetWindowText(hwnd)}")

def find_known_emulator_window():
    found = []
    def enum_handler(hwnd, _):
        title = win32gui.GetWindowText(hwnd)
        for keyword in KNOWN_WINDOW_TITLES:
            if keyword.lower() in title.lower() and is_visible_and_valid(hwnd):
                found.append(hwnd)
                break
    win32gui.EnumWindows(enum_handler, None)
    return found[0] if found else None

def move_window_to_center():
    hwnd = win32gui.GetForegroundWindow()

    if not is_visible_and_valid(hwnd):
        print("⚠ No active window, trying known emulators...")
        hwnd = find_known_emulator_window()

    if hwnd:
        center_window(hwnd)
    else:
        print("❌ No valid window found to move.")

# Bind hotkey
keyboard.add_hotkey("ctrl+alt+m", move_window_to_center)
print("▶ Press Ctrl+Alt+M to center active or emulator window.")

keyboard.wait()
