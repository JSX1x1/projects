import ctypes
import random
import psutil
import sys
import os

# Function to check if the script is running with admin privileges (Windows-specific)
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception as e:
        return False

# Function to check if a disk is an SSD or HDD using psutil
def get_disk_type():
    partitions = psutil.disk_partitions()
    for partition in partitions:
        if 'removable' not in partition.opts:
            # Check the device type (e.g., SSD or HDD)
            device = partition.device
            try:
                disk_info = psutil.disk_usage(device)
                if psutil.disk_io_counters(perdisk=True)[device].write_bytes > 0:
                    return "SSD" if disk_info.total > 200_000_000_000 else "HDD"
            except Exception as e:
                return "Unknown"
    return "Unknown"

# Function to simulate a disk with sector status (used or free) and data
def simulate_disk(num_cylinders, num_heads, sectors_per_track):
    disk = {}
    for cylinder in range(num_cylinders):
        for head in range(num_heads):
            for sector in range(sectors_per_track):
                disk[(cylinder, head, sector)] = {
                    "status": random.choice(["used", "free"]),
                    "data": f"Data at Cylinder {cylinder}, Head {head}, Sector {sector}" if random.choice([True, False]) else ""
                }
    return disk

# Convert CHS to LBA
def chs_to_lba(cylinder, head, sector, sectors_per_track=63, heads=16):
    return (cylinder * heads + head) * sectors_per_track + sector - 1

# Convert LBA to CHS
def lba_to_chs(lba, sectors_per_track=63, heads=16):
    sector = lba % sectors_per_track + 1
    head = (lba // sectors_per_track) % heads
    cylinder = lba // (sectors_per_track * heads)
    return cylinder, head, sector

# Check Sector Status
def check_sector_status(cylinder, head, sector, disk):
    if disk.get((cylinder, head, sector))["status"] == "used":
        return "Sector is used."
    return "Sector is free."

# View Data at a Sector (For Admin users)
def view_sector_data(cylinder, head, sector, disk):
    if disk.get((cylinder, head, sector))["status"] == "used":
        return disk.get((cylinder, head, sector))["data"]
    return "No data at this sector."

# Scan the entire disk for used or free sectors (For Admin and Non-Admin users)
def scan_disk(disk, num_cylinders, num_heads, sectors_per_track):
    result = []
    for cylinder in range(num_cylinders):
        for head in range(num_heads):
            for sector in range(sectors_per_track):
                status = check_sector_status(cylinder, head, sector, disk)
                result.append(f"Cylinder: {cylinder}, Head: {head}, Sector: {sector} - {status}")
    return result

# Main CLI function
def main():
    num_cylinders = 100
    num_heads = 16
    sectors_per_track = 63
    
    # Check for admin privileges and initialize the disk
    disk = None
    if is_admin():
        disk_type = get_disk_type()
        if disk_type != "Unknown":
            disk = None  # Real disk handling logic (omitted for simplicity)
            print(f"Connected disk type is: {disk_type}")
        else:
            print("Unable to detect the disk type.")
    else:
        disk = simulate_disk(num_cylinders, num_heads, sectors_per_track)
        print("Running with simulated virtual disk (no admin privileges).")
    
    print("Disk Address Tool CLI")
    print("Select an option:")
    print("1. Convert CHS to LBA")
    print("2. Convert LBA to CHS")
    print("3. Check Sector Status")
    print("4. View Data at Sector (Admin Only)")
    print("5. Scan Entire Disk")
    
    choice = input("Enter choice (1-5): ")

    if choice == "1":
        # CHS to LBA
        cylinder = int(input("Enter Cylinder: "))
        head = int(input("Enter Head: "))
        sector = int(input("Enter Sector: "))
        lba = chs_to_lba(cylinder, head, sector)
        print(f"LBA: {lba}")
        if is_admin() and isinstance(disk, dict):
            status = check_sector_status(cylinder, head, sector, disk)
            print(status)
    
    elif choice == "2":
        # LBA to CHS
        lba = int(input("Enter LBA: "))
        cylinder, head, sector = lba_to_chs(lba)
        print(f"CHS: Cylinder {cylinder}, Head {head}, Sector {sector}")
        if is_admin() and isinstance(disk, dict):
            status = check_sector_status(cylinder, head, sector, disk)
            print(status)

    elif choice == "3":
        # Check Sector Status
        cylinder = int(input("Enter Cylinder: "))
        head = int(input("Enter Head: "))
        sector = int(input("Enter Sector: "))
        if is_admin():
            if isinstance(disk, dict):
                status = check_sector_status(cylinder, head, sector, disk)
                print(status)
            else:
                print("Unable to check real disk, invalid disk simulation.")
        else:
            print("You need admin privileges to check sector status.")

    elif choice == "4":
        # View Data at Sector (Admin Only)
        if not is_admin():
            print("This function requires admin privileges.")
        else:
            cylinder = int(input("Enter Cylinder: "))
            head = int(input("Enter Head: "))
            sector = int(input("Enter Sector: "))
            if isinstance(disk, dict):
                data = view_sector_data(cylinder, head, sector, disk)
                print(f"Data at Sector: {data}")
            else:
                print("Unable to view real disk data, invalid disk simulation.")

    elif choice == "5":
        # Scan Entire Disk
        if isinstance(disk, dict):
            results = scan_disk(disk, num_cylinders, num_heads, sectors_per_track)
            for result in results:
                print(result)
        else:
            print("Unable to scan real disk, invalid disk simulation.")

    else:
        print("Invalid choice. Exiting.")

if __name__ == "__main__":
    main()
