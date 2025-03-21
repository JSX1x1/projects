import sys
import psutil
import time
import threading
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, 
    QProgressBar, QLabel, QHBoxLayout, QSpinBox
)
from PyQt6.QtCore import Qt, QTimer, QMutex

class CPUProcessMonitor(QWidget):
    def __init__(self):
        super().__init__()

        # ** GUI Configuration **
        self.setWindowTitle("🔍 Multi-Threaded CPU Process Monitor")
        self.setGeometry(200, 200, 1000, 600)
        self.setStyleSheet("background-color: #2e2e2e; color: white;")

        # ** Layouts **
        self.main_layout = QVBoxLayout()

        # ** System Stats Panel **
        self.stats_layout = QHBoxLayout()
        self.cpu_label = QLabel("🔹 CPU Usage: 0%")
        self.ram_label = QLabel("🔹 RAM Usage: 0%")
        self.disk_label = QLabel("🔹 Disk Usage: 0%")
        self.limit_label = QLabel("🔹 Show Top:")
        self.process_limit = QSpinBox()
        self.process_limit.setMinimum(5)
        self.process_limit.setMaximum(100)
        self.process_limit.setValue(25)  # Default to show top 25 processes
        self.process_limit.valueChanged.connect(self.update_table_limit)

        for widget in [self.cpu_label, self.ram_label, self.disk_label, self.limit_label, self.process_limit]:
            widget.setStyleSheet("font-size: 14px; font-weight: bold; padding: 5px;")
            self.stats_layout.addWidget(widget)

        self.main_layout.addLayout(self.stats_layout)

        # ** Table Setup **
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["PID", "Process Name", "CPU (%)", "Memory (%)", "Threads", "Status"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #1e1e1e; 
                border: 1px solid #555; 
                font-size: 13px;
            }
            QHeaderView::section {
                background-color: #444; 
                padding: 5px; 
                font-size: 13px; 
                font-weight: bold;
            }
        """)

        self.main_layout.addWidget(self.table)
        self.setLayout(self.main_layout)

        # ** Timers for UI Updates **
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_process_list)
        self.timer.start(2000)  # Updates every 2 seconds

        self.stats_timer = QTimer()
        self.stats_timer.timeout.connect(self.update_system_stats)
        self.stats_timer.start(1500)  # Updates every 1.5 seconds

        # ** Multi-Threading Setup **
        self.process_data = []
        self.data_lock = QMutex()  # Thread safety

        # ** Start background threads **
        self.monitor_thread = threading.Thread(target=self.fetch_processes, daemon=True)
        self.monitor_thread.start()

        self.stats_thread = threading.Thread(target=self.fetch_system_stats, daemon=True)
        self.stats_thread.start()

    def fetch_processes(self):
        """ Fetch process data in a separate thread to prevent UI lag. """
        while True:
            processes = []
            for proc in psutil.process_iter(attrs=['pid', 'name', 'memory_percent', 'num_threads', 'status']):
                try:
                    proc_info = proc.info
                    proc_info['cpu_percent'] = proc.cpu_percent()  # CPU usage is calculated separately
                    processes.append(proc_info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

            # ** Sort processes by CPU usage (Highest First) **
            processes.sort(key=lambda x: x['cpu_percent'], reverse=True)

            # ** Lock thread before modifying shared data **
            self.data_lock.lock()
            self.process_data = processes
            self.data_lock.unlock()

            time.sleep(1)  # Adjust update frequency to reduce lag

    def update_process_list(self):
        """ Updates the UI with the latest process data efficiently. """
        self.data_lock.lock()
        process_data_copy = self.process_data[:self.process_limit.value()]  # Limit display
        self.data_lock.unlock()

        self.table.setRowCount(len(process_data_copy))

        for row, proc in enumerate(process_data_copy):
            self.table.setItem(row, 0, QTableWidgetItem(str(proc['pid'])))
            self.table.setItem(row, 1, QTableWidgetItem(proc['name'][:38]))

            cpu_usage = proc['cpu_percent']
            cpu_bar = self.create_progress_bar(cpu_usage, 100)
            mem_usage = proc['memory_percent']
            mem_bar = self.create_progress_bar(mem_usage, 100)

            self.table.setItem(row, 4, QTableWidgetItem(str(proc['num_threads'])))
            self.table.setItem(row, 5, QTableWidgetItem(proc['status']))
            self.table.setCellWidget(row, 2, cpu_bar)
            self.table.setCellWidget(row, 3, mem_bar)

    def fetch_system_stats(self):
        """ Fetch system stats in a separate thread. """
        while True:
            cpu_usage = psutil.cpu_percent(interval=0.5)
            ram_usage = psutil.virtual_memory().percent
            disk_usage = psutil.disk_usage('/').percent

            # ** Lock thread before modifying shared data **
            self.data_lock.lock()
            self.current_cpu = cpu_usage
            self.current_ram = ram_usage
            self.current_disk = disk_usage
            self.data_lock.unlock()

            time.sleep(1)

    def update_system_stats(self):
        """ Updates system-wide statistics in real-time. """
        self.data_lock.lock()
        cpu = self.current_cpu
        ram = self.current_ram
        disk = self.current_disk
        self.data_lock.unlock()

        self.cpu_label.setText(f"🔹 CPU Usage: {cpu}%")
        self.ram_label.setText(f"🔹 RAM Usage: {ram}%")
        self.disk_label.setText(f"🔹 Disk Usage: {disk}%")

    def create_progress_bar(self, value, max_value):
        """ Creates a color-coded progress bar. """
        progress_bar = QProgressBar()
        progress_bar.setValue(int(value))
        progress_bar.setTextVisible(True)

        if value < 30:
            color = "green"
        elif 30 <= value < 70:
            color = "yellow"
        else:
            color = "red"

        progress_bar.setStyleSheet(f"""
            QProgressBar {{
                background-color: #444;
                border-radius: 3px;
                height: 10px;
            }}
            QProgressBar::chunk {{
                background-color: {color};
            }}
        """)

        return progress_bar

    def update_table_limit(self):
        """ Trigger a table update when the process limit is changed. """
        self.update_process_list()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CPUProcessMonitor()
    window.show()
    sys.exit(app.exec())
