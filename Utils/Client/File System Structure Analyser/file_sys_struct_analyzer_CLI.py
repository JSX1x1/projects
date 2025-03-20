import os
import sys
import psutil
import ctypes
import platform
import subprocess

# Check if running as admin/root
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() if os.name == "nt" else os.geteuid() == 0
    except:
        return False

# Get available drives (Windows & Linux/Mac)
def get_drives():
    partitions = psutil.disk_partitions()
    return [p.device for p in partitions]

# Analyze basic file system details
def analyze_drive_basic(drive):
    info = {}
    try:
        usage = psutil.disk_usage(drive)
        info["Total Space"] = f"{usage.total / (1024**3):.2f} GB"
        info["Used Space"] = f"{usage.used / (1024**3):.2f} GB"
        info["Free Space"] = f"{usage.free / (1024**3):.2f} GB"
        info["Usage Percent"] = f"{usage.percent}%"
    except Exception as e:
        info["Error"] = f"Failed to retrieve usage info: {e}"

    try:
        for part in psutil.disk_partitions():
            if part.device == drive:
                info["File System"] = part.fstype
                info["Mount Point"] = part.mountpoint
    except Exception as e:
        info["Error"] = f"Failed to retrieve partition info: {e}"

    return info

# Get advanced drive details (Admin Mode)
def analyze_drive_advanced(drive):
    info = {}

    if platform.system() == "Windows":
        try:
            output = subprocess.check_output(["fsutil", "fsinfo", "ntfsinfo", drive], universal_newlines=True)
            for line in output.splitlines():
                if ":" in line:
                    key, value = line.split(":", 1)
                    info[key.strip()] = value.strip()
        except Exception as e:
            info["Error"] = f"Failed to retrieve NTFS details: {e}"

        try:
            smart_output = subprocess.check_output(["wmic", "diskdrive", "get", "Status,Model"], universal_newlines=True)
            info["Drive Health (S.M.A.R.T)"] = smart_output.strip()
        except Exception as e:
            info["Error"] += f"\nSMART check failed: {e}"

    elif platform.system() == "Linux":
        try:
            output = subprocess.check_output(["tune2fs", "-l", drive], universal_newlines=True)
            for line in output.splitlines():
                if ":" in line:
                    key, value = line.split(":", 1)
                    info[key.strip()] = value.strip()
        except Exception as e:
            info["Error"] = f"Failed to retrieve EXT4 details: {e}"

        try:
            smart_output = subprocess.check_output(["smartctl", "-H", drive], universal_newlines=True)
            info["Drive Health (S.M.A.R.T)"] = smart_output.strip()
        except Exception as e:
            info["Error"] += f"\nSMART check failed: {e}"

    return info

# CLI Menu
def main():
    print("\n=== File System Analyzer CLI ===\n")
    
    if is_admin():
        print("Running as Admin (Advanced Analysis Enabled)\n")
    else:
        print("Running as User (Limited Information)\n")

    drives = get_drives()
    if not drives:
        print("No drives found.")
        return
    
    print("Available Drives:")
    for i, drive in enumerate(drives, 1):
        print(f"[{i}] {drive}")
    
    try:
        choice = int(input("\nEnter the number of the drive to analyze: ")) - 1
        if choice < 0 or choice >= len(drives):
            print("Invalid selection.")
            return
    except ValueError:
        print("Invalid input. Please enter a number.")
        return
    
    selected_drive = drives[choice]
    print(f"\nAnalyzing drive: {selected_drive}\n")

    # Basic Information
    basic_info = analyze_drive_basic(selected_drive)
    for key, value in basic_info.items():
        print(f"{key}: {value}")

    # Advanced Information (Admin only)
    if is_admin():
        print("\n=== Advanced Analysis ===\n")
        advanced_info = analyze_drive_advanced(selected_drive)
        for key, value in advanced_info.items():
            print(f"{key}: {value}")

    print("\nAnalysis Complete.")

if __name__ == "__main__":
    main()
