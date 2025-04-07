import time
import win32api
import win32file
import psutil
import ctypes
import hashlib
from tkinter import Tk, simpledialog, messagebox

# 🔒 Store the hashed password (test123)
STORED_HASH = "ecd71870d1963316a97e3ac3408c9835ad8cf0f3c1bc703527c30265534f75ae"

# Log file path
LOG_FILE = "usb_access_log.txt"

# Store authorized drives
authorized_drives = set()

# Function to log messages
def log_event(message):
    with open(LOG_FILE, "a") as log:
        timestamp = time.strftime("[%Y-%m-%d %H:%M:%S]")
        log.write(f"{timestamp} {message}\n")
    print(message)

# Function to hash a password with SHA-256
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to get all currently connected USB drives
def get_usb_drives():
    drives = []
    bitmask = win32api.GetLogicalDrives()
    for letter in range(26):
        if bitmask & (1 << letter):
            drive = f"{chr(65 + letter)}:\\"
            if win32file.GetDriveType(drive) == win32file.DRIVE_REMOVABLE:
                drives.append(drive)
    return set(drives)

# Function to prompt authentication with hashed password check
def authenticate():
    root = Tk()
    root.withdraw()  # Hide the main window
    user_input = simpledialog.askstring("Authentication Required", "Enter password to allow USB access:", show='*')
    
    if user_input and hash_password(user_input) == STORED_HASH:
        log_event("Authentication successful.")
        return True
    else:
        log_event("Authentication failed!")
        return False

# Function to eject a USB drive
def eject_usb(drive):
    try:
        for partition in psutil.disk_partitions():
            if partition.device.startswith(drive):
                ctypes.windll.kernel32.DeviceIoControl(
                    ctypes.windll.kernel32.CreateFileW(f"\\\\.\\{drive}", 0, 0, None, 3, 0, None),
                    0x2D4808, None, 0, None, 0, ctypes.byref(ctypes.c_ulong()), None
                )
                log_event(f"USB drive {drive} ejected due to failed authentication.")
                messagebox.showwarning("Security Alert", f"Unauthorized USB {drive} has been ejected.")
    except Exception as e:
        log_event(f"Error ejecting USB {drive}: {e}")

# GUI alert for USB detection
def show_usb_alert(drive):
    root = Tk()
    root.withdraw()
    messagebox.showinfo("New USB Detected", f"A new USB drive {drive} has been detected.")
    root.destroy()

# Main loop
known_drives = get_usb_drives()
log_event("USB monitoring started...")

while True:
    current_drives = get_usb_drives()
    
    new_drives = current_drives - known_drives  # Detect new USB drives
    removed_drives = known_drives - current_drives  # Detect removed USB drives

    for drive in new_drives:
        log_event(f"New USB detected: {drive}")
        show_usb_alert(drive)

        # If no USBs are currently authorized, require authentication before allowing any
        if not authorized_drives:
            if authenticate():
                log_event(f"USB {drive} authorized.")
                authorized_drives.add(drive)
            else:
                log_event(f"Blocking USB {drive}.")
                eject_usb(drive)
        else:
            log_event(f"New USB {drive} blocked. Only one authorized USB is allowed.")
            eject_usb(drive)

    # Remove from authorized list if the drive is unplugged
    for drive in removed_drives:
        if drive in authorized_drives:
            authorized_drives.remove(drive)
            log_event(f"USB {drive} removed. Authentication required for new devices.")

    known_drives = current_drives  # Update known drives
    time.sleep(2)  # Check every 2 seconds
