import sys
import os
import ctypes
import psutil
import humanize
import wmi  # Windows only
from collections import defaultdict
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel,
    QPushButton, QListWidget, QMessageBox, QTextEdit, QProgressBar
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal

# **Check if User has Admin Privileges**
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# **Thread for Scanning Disk Usage & File Types (Prevents UI Freezing)**
class DiskScanThread(QThread):
    progress = pyqtSignal(int)  # Progress signal
    finished = pyqtSignal(dict, str)  # Signal with file data

    def __init__(self, disk_path):
        super().__init__()
        self.disk_path = disk_path

    def run(self):
        """Scans the disk for file type distribution (background process)."""
        file_types = defaultdict(int)
        total_size = 0
        scanned_size = 0
        try:
            for root, _, files in os.walk(self.disk_path):
                for file in files:
                    file_ext = os.path.splitext(file)[-1].lower() or "Unknown"
                    file_path = os.path.join(root, file)

                    try:
                        file_size = os.path.getsize(file_path)
                        file_types[file_ext] += file_size
                        total_size += file_size
                        scanned_size += file_size

                        # Emit progress every 100MB scanned
                        if scanned_size > 100 * 1024 * 1024:
                            self.progress.emit(int((scanned_size / (total_size + 1)) * 100))
                            scanned_size = 0  # Reset scanned tracker

                    except (PermissionError, FileNotFoundError):
                        continue  # Skip inaccessible files

        except Exception as e:
            self.finished.emit({"Error": f"Scan failed: {e}"}, "0B")
            return

        # Convert to human-readable sizes
        file_types = {k: humanize.naturalsize(v) for k, v in file_types.items()}
        self.finished.emit(file_types, humanize.naturalsize(total_size))

# **Get Deep Disk Info (Windows Only)**
def get_disk_info(disk_letter):
    try:
        c = wmi.WMI()
        for disk in c.Win32_LogicalDisk():
            if disk.DeviceID == disk_letter:
                return {
                    "Volume Name": disk.VolumeName or "Unknown",
                    "File System": disk.FileSystem or "N/A",
                    "Disk Type": disk.Description or "N/A",
                    "Free Space": humanize.naturalsize(int(disk.FreeSpace)) if disk.FreeSpace else "N/A",
                    "Total Size": humanize.naturalsize(int(disk.Size)) if disk.Size else "N/A",
                    "Serial Number": disk.VolumeSerialNumber or "N/A",
                    "Drive Type": disk.DriveType
                }
        return {"Error": "No deep info available"}
    except Exception as e:
        return {"Error": f"Could not retrieve deep info: {e}"}

# **Main Disk Monitoring App**
class DiskMonitoringApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Advanced Disk Monitoring Tool")
        self.setGeometry(200, 200, 1000, 700)
        self.setStyleSheet("background-color: #121212; color: white;")

        # **Main Layout**
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # **Admin Check**
        self.admin_status = is_admin()
        self.warning_label = QLabel()
        self.warning_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.warning_label.setStyleSheet("color: red; font-size: 16px;")
        self.layout.addWidget(self.warning_label)

        if not self.admin_status:
            self.warning_label.setText("⚠️ WARNING: No Admin Privileges! Some data will be restricted.")
        else:
            self.warning_label.setText("✅ Admin Privileges Detected")

        # **Disk List**
        self.disk_list = QListWidget()
        self.disk_list.itemClicked.connect(self.show_disk_details)
        self.layout.addWidget(self.disk_list)

        # **Progress Bar for Scanning**
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(100)
        self.progress_bar.setTextVisible(True)
        self.layout.addWidget(self.progress_bar)

        # **Disk Info Panel**
        self.disk_info_label = QTextEdit()
        self.disk_info_label.setReadOnly(True)
        self.disk_info_label.setStyleSheet("font-size: 14px; padding: 10px; background-color: #1e1e1e; color: #00ff00;")
        self.layout.addWidget(self.disk_info_label)

        # **Refresh Button**
        self.refresh_button = QPushButton("Refresh Disks")
        self.refresh_button.setStyleSheet("background-color: #444; padding: 10px;")
        self.refresh_button.clicked.connect(self.load_disks)
        self.layout.addWidget(self.refresh_button)

        # **Load Disks**
        self.load_disks()

    def load_disks(self):
        """Scans the system for available disks."""
        self.disk_list.clear()
        self.disks = {}

        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disk_info = f"{partition.device} ({partition.mountpoint}) - {humanize.naturalsize(usage.total)}"
                self.disk_list.addItem(disk_info)

                self.disks[disk_info] = partition.mountpoint

            except PermissionError:
                continue  # Skip inaccessible drives

    def show_disk_details(self, item):
        """Displays detailed disk information when a disk is clicked."""
        disk_path = self.disks.get(item.text(), None)

        if not disk_path:
            QMessageBox.warning(self, "Error", "Unable to access disk information.")
            return

        try:
            usage = psutil.disk_usage(disk_path)
            total_size = humanize.naturalsize(usage.total)
            used_size = humanize.naturalsize(usage.used)
            free_size = humanize.naturalsize(usage.free)
            percent_used = usage.percent

            # Start background scanning for file distribution
            self.progress_bar.setValue(0)
            self.scan_thread = DiskScanThread(disk_path)
            self.scan_thread.progress.connect(self.progress_bar.setValue)
            self.scan_thread.finished.connect(self.display_scan_results)
            self.scan_thread.start()

            # Get deep disk info
            disk_letter = disk_path[:2]  # Example: "C:"
            deep_info = get_disk_info(disk_letter)
            deep_info_text = "\n".join([f"{key}: {value}" for key, value in deep_info.items()])

            self.disk_info_label.setText(f"🛠 Deep Disk Info:\n{deep_info_text}\n\n📂 Scanning file types...")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to retrieve disk details: {e}")

    def display_scan_results(self, file_distribution, total_scanned):
        """Displays the file type scan results."""
        scan_results = "\n".join([f"• {ext.upper()}: {size}" for ext, size in file_distribution.items()])
        self.disk_info_label.append(f"\n📂 File Type Breakdown:\n{scan_results}\n\nTotal Scanned: {total_scanned}")

# **Run the Application**
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DiskMonitoringApp()
    window.show()
    sys.exit(app.exec())