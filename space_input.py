import ctypes
import time
# --- Structures ---

PUL = ctypes.POINTER(ctypes.c_ulong)

class KeyBdInput(ctypes.Structure):
    _fields_ = [
        ("wVk", ctypes.c_ushort),
        ("wScan", ctypes.c_ushort),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", PUL)
    ]

class HardwareInput(ctypes.Structure):
    _fields_ = [
        ("uMsg", ctypes.c_ulong),
        ("wParamL", ctypes.c_short),
        ("wParamH", ctypes.c_ushort)
    ]

class MouseInput(ctypes.Structure):
    _fields_ = [
        ("dx", ctypes.c_long),
        ("dy", ctypes.c_long),
        ("mouseData", ctypes.c_ulong),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", PUL)
    ]

class Input_I(ctypes.Union):
    _fields_ = [
        ("ki", KeyBdInput),
        ("mi", MouseInput),
        ("hi", HardwareInput)
    ]

class Input(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.c_ulong),
        ("ii", Input_I)
    ]


INPUT_KEYBOARD = 1
KEYEVENTF_SCANCODE = 0x0008
KEYEVENTF_KEYUP = 0x0002
SPACE_SCANCODE = 0x39

SendInput = ctypes.windll.user32.SendInput

def press_space():
    extra = ctypes.c_ulong(0)

    ii = Input_I()
    ii.ki = KeyBdInput(
        wVk=0,
        wScan=SPACE_SCANCODE,
        dwFlags=KEYEVENTF_SCANCODE,
        time=0,
        dwExtraInfo=ctypes.pointer(extra)
    )

    x = Input(INPUT_KEYBOARD, ii)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

    time.sleep(0.6)

    ii2 = Input_I()
    ii2.ki = KeyBdInput(
        wVk=0,
        wScan=SPACE_SCANCODE,
        dwFlags=KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP,
        time=0,
        dwExtraInfo=ctypes.pointer(extra)
    )

    x2 = Input(INPUT_KEYBOARD, ii2)
    SendInput(1, ctypes.pointer(x2), ctypes.sizeof(x2))

