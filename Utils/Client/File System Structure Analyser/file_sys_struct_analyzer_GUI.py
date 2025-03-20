import sys
import os
import psutil
import ctypes
import platform
import struct
import subprocess
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QListWidget, QWidget, QMessageBox
from PyQt6.QtGui import QFont

# Function to check if the script is running as admin
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() if os.name == 'nt' else os.geteuid() == 0
    except:
        return False

# Function to get available drives (Windows & Linux/Mac)
def get_drives():
    partitions = psutil.disk_partitions()
    return [p.device for p in partitions]

# Function to analyze basic file system details
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

# Function to get advanced drive details (only available for admins)
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

# Main GUI class
class FileSystemAnalyzer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("File System Analyzer")
        self.setGeometry(100, 100, 700, 500)
        self.setStyleSheet("background-color: #2E3440; color: white;")

        self.layout = QVBoxLayout()

        # Admin check
        self.admin_label = QLabel("🔹 Checking permissions...")
        self.admin_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        self.layout.addWidget(self.admin_label)

        self.update_admin_status()

        # Drive list
        self.drive_list = QListWidget()
        self.drive_list.setStyleSheet("background-color: #3B4252; color: white;")
        self.layout.addWidget(self.drive_list)

        self.load_drives()

        # Analyze button
        self.analyze_button = QPushButton("Analyze Selected Drive")
        self.analyze_button.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        self.analyze_button.setStyleSheet("background-color: #5E81AC; color: white; padding: 8px;")
        self.analyze_button.clicked.connect(self.analyze_selected_drive)
        self.layout.addWidget(self.analyze_button)

        # Info display
        self.info_label = QLabel("")
        self.info_label.setWordWrap(True)
        self.layout.addWidget(self.info_label)

        # Main container
        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def update_admin_status(self):
        if is_admin():
            self.admin_label.setText("✅ Running as Admin (Advanced Analysis Enabled)")
            self.admin_label.setStyleSheet("color: #A3BE8C;")
        else:
            self.admin_label.setText("⚠️ Running as User (Limited Information)")
            self.admin_label.setStyleSheet("color: #BF616A;")

    def load_drives(self):
        self.drive_list.clear()
        drives = get_drives()
        if not drives:
            self.drive_list.addItem("No drives found")
        else:
            for drive in drives:
                self.drive_list.addItem(drive)

    def analyze_selected_drive(self):
        selected_item = self.drive_list.currentItem()
        if selected_item:
            drive = selected_item.text()
            basic_info = analyze_drive_basic(drive)
            details = "\n".join([f"{key}: {value}" for key, value in basic_info.items()])

            if is_admin():
                advanced_info = analyze_drive_advanced(drive)
                advanced_details = "\n".join([f"{key}: {value}" for key, value in advanced_info.items()])
                details += f"\n\n🔍 **Advanced Analysis (Admin Mode)**:\n{advanced_details}"

            self.info_label.setText(details)
        else:
            QMessageBox.warning(self, "Selection Error", "Please select a drive to analyze.")

# Run Application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileSystemAnalyzer()
    window.show()
    sys.exit(app.exec())
