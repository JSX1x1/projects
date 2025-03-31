import sys
import time
import psutil
import GPUtil
import threading
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QTableWidget, QTableWidgetItem, QSlider
from PyQt6.QtCore import Qt, QThread, pyqtSignal


"""
Advanced Process Analysis Tool (PyQt6)

This tool is designed to **monitor and analyze system processes in real-time**  
while allowing users to **set CPU and GPU usage thresholds** to filter out low-impact processes.  
It provides **detailed insights** into process behavior, including:  

- **Live CPU & GPU usage tracking** (User-defined filtering).  
- **RAM consumption, Disk I/O, and Thread count analysis**.  
- **Suspicious Activity Scoring** based on various factors:  
  - Running from temp directories.  
  - High CPU or RAM consumption.  
  - Excessive thread usage.  
  - Recently started processes.  

**Features:**  
- **Modern GUI** with a dark cyberpunk aesthetic.  
- **Real-time updates** without UI freezes (thanks to multithreading).  
- **Fully adjustable CPU/GPU usage thresholds** with sliders.  
- **Suspicious processes are highlighted** (Yellow: Medium | Red: High risk).  

**Use Case Scenarios:**  
- Detect **high-resource processes** that slow down your system.  
- Identify **potential malware** or abnormal system behavior.  
- Monitor **GPU-heavy applications** for troubleshooting.  
- Analyze process **age and resource patterns** for debugging.  

This tool helps **security analysts, system administrators, and performance tuners**  
gain deeper insights into system behavior in an efficient and user-friendly manner.
"""


class ProcessMonitorThread(QThread):
    process_data_signal = pyqtSignal(list)

    def __init__(self, cpu_threshold, gpu_threshold):
        super().__init__()
        self.cpu_threshold = cpu_threshold
        self.gpu_threshold = gpu_threshold
        self.running = True

    def run(self):
        while self.running:
            process_list = self.get_filtered_processes()
            self.process_data_signal.emit(process_list)
            time.sleep(2)  # Update every 2 seconds

    def get_filtered_processes(self):
        processes = {p.pid: p for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info', 'create_time'])}
        gpus = GPUtil.getGPUs()
        gpu_usages = {gpu.id: gpu.load * 100 for gpu in gpus} if gpus else {}

        process_list = []

        for proc in processes.values():
            try:
                cpu_usage = proc.cpu_percent() / psutil.cpu_count()
                gpu_usage = gpu_usages.get(proc.pid, 0)

                # **Filter by CPU/GPU Thresholds**
                if cpu_usage < self.cpu_threshold and gpu_usage < self.gpu_threshold:
                    continue  # Ignore processes below threshold

                ram_usage = proc.memory_info().rss / (1024 * 1024)  # Convert to MB
                disk_usage = proc.io_counters().read_bytes + proc.io_counters().write_bytes
                thread_count = proc.num_threads()
                process_age = time.time() - proc.create_time()

                suspicious_score = self.calculate_suspicious_score(proc, cpu_usage, ram_usage, thread_count, process_age)

                process_list.append((proc.name(), cpu_usage, gpu_usage, ram_usage, disk_usage, thread_count, process_age, suspicious_score))
            except:
                continue  # Skip permission errors

        return process_list

    def calculate_suspicious_score(self, proc, cpu_usage, ram_usage, thread_count, process_age):
        score = 0
        try:
            exe_path = proc.exe().lower()
            if any(s in exe_path for s in ["\\temp", "\\appdata\\local\\temp", "unknown.exe"]):
                score += 3  # Suspicious location
            if cpu_usage > 80:
                score += 2  # High CPU usage
            if ram_usage > 500:  # More than 500MB RAM usage
                score += 2
            if thread_count > 100:
                score += 2  # High thread count (potential malware)
            if process_age < 30:  # Process started in the last 30 seconds
                score += 3
        except:
            score += 1  # Unable to get process details

        return score

    def stop(self):
        self.running = False

class ProcessMonitor(QMainWindow):
    def __init__(self):
        super().__init__()

        # Window Config
        self.setWindowTitle("Advanced Process Analysis Tool")
        self.setGeometry(200, 200, 1000, 600)
        self.setStyleSheet("background-color: #1e1e1e; color: white;")

        # Main Layout
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # Title Label
        self.title_label = QLabel("Real-Time Process Monitor", self)
        self.title_label.setStyleSheet("font-size: 20px; font-weight: bold; padding: 10px;")
        layout.addWidget(self.title_label)

        # CPU/GPU Threshold Sliders
        self.cpu_threshold_label = QLabel("CPU Usage Threshold: 50%", self)
        self.cpu_threshold_slider = QSlider(Qt.Orientation.Horizontal)
        self.cpu_threshold_slider.setMinimum(1)
        self.cpu_threshold_slider.setMaximum(100)
        self.cpu_threshold_slider.setValue(50)
        self.cpu_threshold_slider.setStyleSheet("background: #333; padding: 5px;")
        self.cpu_threshold_slider.valueChanged.connect(self.update_cpu_threshold)

        self.gpu_threshold_label = QLabel("GPU Usage Threshold: 50%", self)
        self.gpu_threshold_slider = QSlider(Qt.Orientation.Horizontal)
        self.gpu_threshold_slider.setMinimum(1)
        self.gpu_threshold_slider.setMaximum(100)
        self.gpu_threshold_slider.setValue(50)
        self.gpu_threshold_slider.setStyleSheet("background: #333; padding: 5px;")
        self.gpu_threshold_slider.valueChanged.connect(self.update_gpu_threshold)

        layout.addWidget(self.cpu_threshold_label)
        layout.addWidget(self.cpu_threshold_slider)
        layout.addWidget(self.gpu_threshold_label)
        layout.addWidget(self.gpu_threshold_slider)

        # Process Table
        self.process_table = QTableWidget()
        self.process_table.setColumnCount(7)
        self.process_table.setHorizontalHeaderLabels(["Name", "CPU (%)", "GPU (%)", "RAM (MB)", "Disk I/O", "Threads", "Suspicious Score"])
        self.process_table.setStyleSheet("""
            QTableWidget { background-color: #252525; color: white; font-size: 14px; }
            QHeaderView::section { background-color: #333; padding: 5px; font-weight: bold; }
        """)
        layout.addWidget(self.process_table)

        # Start Background Thread
        self.cpu_threshold = 50
        self.gpu_threshold = 50
        self.process_thread = ProcessMonitorThread(self.cpu_threshold, self.gpu_threshold)
        self.process_thread.process_data_signal.connect(self.update_process_list)
        self.process_thread.start()

    def update_cpu_threshold(self, value):
        self.cpu_threshold = value
        self.cpu_threshold_label.setText(f"CPU Usage Threshold: {value}%")
        self.process_thread.cpu_threshold = value

    def update_gpu_threshold(self, value):
        self.gpu_threshold = value
        self.gpu_threshold_label.setText(f"GPU Usage Threshold: {value}%")
        self.process_thread.gpu_threshold = value

    def update_process_list(self, process_list):
        self.process_table.setRowCount(0)
        for proc in process_list:
            row_position = self.process_table.rowCount()
            self.process_table.insertRow(row_position)

            for col, data in enumerate(proc):
                item = QTableWidgetItem(str(data))
                if col == 6 and data >= 5:
                    item.setForeground(Qt.GlobalColor.red)
                elif col == 6 and data >= 3:
                    item.setForeground(Qt.GlobalColor.yellow)
                else:
                    item.setForeground(Qt.GlobalColor.green)

                self.process_table.setItem(row_position, col, item)

    def closeEvent(self, event):
        self.process_thread.stop()
        self.process_thread.wait()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProcessMonitor()
    window.show()
    sys.exit(app.exec())
