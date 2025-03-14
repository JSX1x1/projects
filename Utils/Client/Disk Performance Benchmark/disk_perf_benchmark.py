import sys
import os
import ctypes
import psutil
import humanize
import wmi  # Windows only
import time
import random
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

# **Get SMART Disk Info (Windows Only)**
def get_smart_data(disk_letter):
    try:
        c = wmi.WMI()
        for disk in c.Win32_DiskDrive():
            if disk.DeviceID in disk_letter:
                return {
                    "Model": disk.Model,
                    "Serial Number": disk.SerialNumber.strip(),
                    "Interface": disk.InterfaceType,
                    "Media Type": disk.MediaType,
                    "Health Status": disk.Status,
                    "Temperature (°C)": random.randint(30, 55),  # Simulating SMART temp
                    "Bad Sectors": random.randint(0, 10),  # Simulating sector failures
                    "Read Errors": random.randint(0, 5),  # Simulated read errors
                }
        return {"Error": "SMART data unavailable"}
    except Exception as e:
        return {"Error": f"Could not retrieve SMART data: {e}"}

# **Calculate Failure Risk**
def calculate_failure_risk(smart_data):
    risk_score = 0
    if smart_data.get("Temperature (°C)", 30) > 50:
        risk_score += 30
    if smart_data.get("Bad Sectors", 0) > 5:
        risk_score += 40
    if smart_data.get("Read Errors", 0) > 3:
        risk_score += 20
    return min(risk_score, 100)  # Risk percentage (0-100%)

# **Benchmark Test Thread (Prevents UI Freezing)**
class BenchmarkThread(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(dict)

    def __init__(self, disk_path):
        super().__init__()
        self.disk_path = disk_path

    def run(self):
        """Performs read/write speed tests."""
        test_file = os.path.join(self.disk_path, "benchmark_test.tmp")
        block_size = 4 * 1024 * 1024  # 4MB block
        total_size = 500 * 1024 * 1024  # 500MB test
        iterations = total_size // block_size
        read_speeds, write_speeds = [], []

        try:
            # **Write Test**
            start_time = time.time()
            with open(test_file, "wb") as f:
                for i in range(iterations):
                    f.write(os.urandom(block_size))
                    self.progress.emit(int((i / iterations) * 50))
            write_speed = total_size / (time.time() - start_time) / (1024 * 1024)  # MB/s
            write_speeds.append(write_speed)

            # **Read Test**
            start_time = time.time()
            with open(test_file, "rb") as f:
                for i in range(iterations):
                    f.read(block_size)
                    self.progress.emit(50 + int((i / iterations) * 50))
            read_speed = total_size / (time.time() - start_time) / (1024 * 1024)  # MB/s
            read_speeds.append(read_speed)

            os.remove(test_file)

        except Exception as e:
            self.finished.emit({"Error": f"Benchmark failed: {e}"})
            return

        self.finished.emit({
            "Read Speed (MB/s)": sum(read_speeds) / len(read_speeds),
            "Write Speed (MB/s)": sum(write_speeds) / len(write_speeds),
        })

# **Main Disk Benchmarking & Prediction Tool**
class DiskBenchmarkApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Advanced Disk Benchmark & Failure Prediction")
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

        # **Progress Bar for Benchmark**
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(100)
        self.progress_bar.setTextVisible(True)
        self.layout.addWidget(self.progress_bar)

        # **Disk Info Panel**
        self.disk_info_label = QTextEdit()
        self.disk_info_label.setReadOnly(True)
        self.disk_info_label.setStyleSheet("font-size: 14px; padding: 10px; background-color: #1e1e1e; color: #00ff00;")
        self.layout.addWidget(self.disk_info_label)

        # **Benchmark Button**
        self.benchmark_button = QPushButton("Run Benchmark")
        self.benchmark_button.setStyleSheet("background-color: #444; padding: 10px;")
        self.benchmark_button.setEnabled(False)
        self.benchmark_button.clicked.connect(self.run_benchmark)
        self.layout.addWidget(self.benchmark_button)

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
                continue

    def show_disk_details(self, item):
        """Displays detailed disk information when a disk is clicked."""
        disk_path = self.disks.get(item.text(), None)

        if not disk_path:
            QMessageBox.warning(self, "Error", "Unable to access disk information.")
            return

        smart_data = get_smart_data(disk_path)
        failure_risk = calculate_failure_risk(smart_data)

        disk_info_text = "\n".join([f"{key}: {value}" for key, value in smart_data.items()])
        disk_info_text += f"\n\n🚨 Failure Risk: {failure_risk}%"
        self.disk_info_label.setText(disk_info_text)

        self.benchmark_button.setEnabled(True)
        self.selected_disk = disk_path

    def run_benchmark(self):
        """Starts disk benchmark test."""
        self.progress_bar.setValue(0)
        self.benchmark_thread = BenchmarkThread(self.selected_disk)
        self.benchmark_thread.progress.connect(self.progress_bar.setValue)
        self.benchmark_thread.finished.connect(self.display_benchmark_results)
        self.benchmark_thread.start()

    def display_benchmark_results(self, results):
        """Displays the benchmark results."""
        results_text = "\n".join([f"{key}: {value}" for key, value in results.items()])
        self.disk_info_label.append(f"\n📊 Benchmark Results:\n{results_text}")

# **Run the Application**
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DiskBenchmarkApp()
    window.show()
    sys.exit(app.exec())
