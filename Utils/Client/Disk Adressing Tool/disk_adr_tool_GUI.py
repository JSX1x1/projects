import sys
import os
import ctypes
import random
import psutil
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QPushButton, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
import qdarkstyle  # For dark mode styling

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

# Main window class using PyQt6
class DiskToolWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize the disk simulation or real disk information
        self.num_cylinders = 100
        self.num_heads = 16
        self.sectors_per_track = 63
        if is_admin():
            disk_type = get_disk_type()
            if disk_type != "Unknown":
                self.disk = None  # Real disk handling logic (omitted for simplicity)
                QMessageBox.information(self, "Disk Type", f"Connected disk type is: {disk_type}")
            else:
                self.disk = None  # Handle case when the disk type cannot be determined
        else:
            self.disk = simulate_disk(self.num_cylinders, self.num_heads, self.sectors_per_track)

        self.init_ui()

    def init_ui(self):
        # Set up the window layout
        self.setWindowTitle("Disk Addressing Tool")
        self.setGeometry(100, 100, 400, 300)

        # Apply dark theme
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt6())

        # Layouts
        main_layout = QVBoxLayout()
        input_layout = QVBoxLayout()
        result_layout = QVBoxLayout()

        # CHS to LBA section
        self.cylinder_input = QLineEdit(self)
        self.head_input = QLineEdit(self)
        self.sector_input = QLineEdit(self)
        self.lba_result = QLabel("LBA: ", self)
        
        self.chs_to_lba_button = QPushButton("Convert CHS to LBA", self)
        self.chs_to_lba_button.clicked.connect(self.convert_chs_to_lba)
        
        input_layout.addWidget(QLabel("Cylinder:"))
        input_layout.addWidget(self.cylinder_input)
        input_layout.addWidget(QLabel("Head:"))
        input_layout.addWidget(self.head_input)
        input_layout.addWidget(QLabel("Sector:"))
        input_layout.addWidget(self.sector_input)
        input_layout.addWidget(self.chs_to_lba_button)
        input_layout.addWidget(self.lba_result)

        # LBA to CHS section
        self.lba_input = QLineEdit(self)
        self.chs_result = QLabel("CHS: ", self)
        
        self.lba_to_chs_button = QPushButton("Convert LBA to CHS", self)
        self.lba_to_chs_button.clicked.connect(self.convert_lba_to_chs)
        
        input_layout.addWidget(QLabel("LBA:"))
        input_layout.addWidget(self.lba_input)
        input_layout.addWidget(self.lba_to_chs_button)
        input_layout.addWidget(self.chs_result)

        # Sector Status Section
        self.check_status_button = QPushButton("Check Sector Status", self)
        self.check_status_button.clicked.connect(self.check_status)
        self.status_result = QLabel("Sector status will appear here.", self)
        
        result_layout.addWidget(self.check_status_button)
        result_layout.addWidget(self.status_result)

        # View Data at Sector Section (Admin only)
        self.view_data_button = QPushButton("View Data at Sector", self)
        self.view_data_button.clicked.connect(self.view_data_at_sector)
        self.data_result = QLabel("Data at Sector will appear here.", self)
        
        result_layout.addWidget(self.view_data_button)
        result_layout.addWidget(self.data_result)

        # Scan the whole disk for used/free sectors
        self.scan_disk_button = QPushButton("Scan Whole Disk", self)
        self.scan_disk_button.clicked.connect(self.scan_whole_disk)
        
        result_layout.addWidget(self.scan_disk_button)

        # Add the layouts to the main layout
        main_layout.addLayout(input_layout)
        main_layout.addLayout(result_layout)

        self.setLayout(main_layout)

        # Show warning if the user is not an admin
        if not is_admin():
            QMessageBox.warning(self, "Limited Access", "You do not have administrative privileges. Some features may be limited.")

    def convert_chs_to_lba(self):
        try:
            cylinder = int(self.cylinder_input.text())
            head = int(self.head_input.text())
            sector = int(self.sector_input.text())
            lba = chs_to_lba(cylinder, head, sector)
            self.lba_result.setText(f"LBA: {lba}")
            
            if is_admin() and isinstance(self.disk, dict):
                status = check_sector_status(cylinder, head, sector, self.disk)
                self.status_result.setText(status)
        except ValueError:
            QMessageBox.critical(self, "Input Error", "Please enter valid numbers.")

    def convert_lba_to_chs(self):
        try:
            lba = int(self.lba_input.text())
            cylinder, head, sector = lba_to_chs(lba)
            self.chs_result.setText(f"CHS: Cylinder {cylinder}, Head {head}, Sector {sector}")
            
            if is_admin() and isinstance(self.disk, dict):
                status = check_sector_status(cylinder, head, sector, self.disk)
                self.status_result.setText(status)
        except ValueError:
            QMessageBox.critical(self, "Input Error", "Please enter a valid LBA.")

    def check_status(self):
        try:
            cylinder = int(self.cylinder_input.text())
            head = int(self.head_input.text())
            sector = int(self.sector_input.text())

            if is_admin():
                if isinstance(self.disk, dict):
                    status = check_sector_status(cylinder, head, sector, self.disk)
                    self.status_result.setText(status)
                else:
                    self.status_result.setText("Unable to check real disk, invalid disk simulation.")
            else:
                QMessageBox.warning(self, "Access Denied", "You need admin privileges to check sector status.")
        except ValueError:
            QMessageBox.critical(self, "Input Error", "Please enter valid numbers.")

    def view_data_at_sector(self):
        try:
            cylinder = int(self.cylinder_input.text())
            head = int(self.head_input.text())
            sector = int(self.sector_input.text())
            
            if is_admin():
                if isinstance(self.disk, dict):
                    data = view_sector_data(cylinder, head, sector, self.disk)
                    self.data_result.setText(data)
                else:
                    self.data_result.setText("Unable to view real disk data, invalid disk simulation.")
            else:
                self.data_result.setText("You need admin privileges to view the data at this sector.")
        except ValueError:
            QMessageBox.critical(self, "Input Error", "Please enter valid numbers.")
    
    def scan_whole_disk(self):
        if is_admin():
            if isinstance(self.disk, dict):
                results = scan_disk(self.disk, self.num_cylinders, self.num_heads, self.sectors_per_track)
                result_text = "\n".join(results)
                self.status_result.setText(result_text[:500])  # Display first 500 characters for preview
            else:
                self.status_result.setText("Unable to scan real disk, invalid disk simulation.")
        else:
            self.status_result.setText("Cannot scan real disk. Please run with admin privileges.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DiskToolWindow()
    window.show()
    sys.exit(app.exec())
