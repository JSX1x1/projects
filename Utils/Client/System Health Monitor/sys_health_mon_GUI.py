import sys
import os
import psutil
import GPUtil
import ctypes
import time
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QSpinBox
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont
from ping3 import ping

def is_admin():
    try:
        return os.geteuid() == 0  
    except AttributeError:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0  

class CPUCheckThread(QThread):
    result_signal = pyqtSignal(str)

    def __init__(self, duration):
        super().__init__()
        self.duration = duration

    def run(self):
        stability_ratio = self.get_cpu_stability(self.duration)
        cpu_usage = psutil.cpu_percent(interval=1)
        fail_rate, issues = self.calculate_fail_rate(cpu_usage, stability_ratio, "CPU")
        health_rate = 100 - fail_rate
        result = f"CPU Health: {health_rate}% | Fail Rate: {fail_rate}%\nStability: {stability_ratio}%\nIssues: {issues}"
        self.result_signal.emit(result)

    def get_cpu_stability(self, duration):
        cpu_readings = []
        for _ in range(duration):
            cpu_readings.append(psutil.cpu_percent(interval=1))
        
        avg_usage = sum(cpu_readings) / len(cpu_readings)
        max_deviation = max(abs(x - avg_usage) for x in cpu_readings)
        stability_ratio = max(0, 100 - max_deviation)

        return round(stability_ratio, 2)

    def calculate_fail_rate(self, usage, stability, component):
        fail_rate = 0
        issues = []

        if usage > 80:
            fail_rate += 30
            issues.append(f"High {component} usage ({usage}%) - Close unused apps.")

        if stability < 50:
            fail_rate += 40
            issues.append(f"Unstable {component} performance ({stability}% stability) - Possible CPU/GPU throttling.")

        if usage < 80 and stability >= 50:
            fail_rate = 10  

        fail_rate = max(0, min(100, fail_rate))
        return fail_rate, ", ".join(issues) if issues else "No major issues detected."

class GPUCheckThread(QThread):
    result_signal = pyqtSignal(str)

    def run(self):
        try:
            gpus = GPUtil.getGPUs()
            if not gpus:
                self.result_signal.emit("No GPU detected.")
                return
            gpu = gpus[0]
            gpu_usage = gpu.load * 100
            gpu_power = gpu.powerUsage
            fail_rate, issues = self.calculate_fail_rate(gpu_usage, gpu_power, "GPU")
            health_rate = 100 - fail_rate
            result = f"GPU Health: {health_rate}% | Fail Rate: {fail_rate}%\nIssues: {issues}"
            self.result_signal.emit(result)
        except:
            self.result_signal.emit("GPU check failed (Run as Admin).")

    def calculate_fail_rate(self, usage, power, component):
        fail_rate = 0
        issues = []

        if usage > 80:
            fail_rate += 30
            issues.append(f"High {component} usage ({usage}%) - Close unused apps.")

        if power > 200:
            fail_rate += 30
            issues.append("High GPU power draw - Possible driver issues.")

        if usage < 80 and power < 200:
            fail_rate = 10  

        fail_rate = max(0, min(100, fail_rate))
        return fail_rate, ", ".join(issues) if issues else "No major issues detected."

class WiFiCheckThread(QThread):
    result_signal = pyqtSignal(str)

    def run(self):
        ping_google = ping("8.8.8.8") or 100
        ping_cloudflare = ping("1.1.1.1") or 100
        avg_ping = round((ping_google + ping_cloudflare) / 2, 2)
        stability_rate = max(0, min(100, round(100 - avg_ping / 2, 2)))

        issues = []
        if avg_ping > 100:
            issues.append("High latency - check your connection.")
        if stability_rate < 50:
            issues.append("Unstable network - possible packet loss.")

        issues_text = ", ".join(issues) if issues else "No major issues detected."
        result = f"WiFi Stability: {stability_rate}%\nIssues: {issues_text}"
        self.result_signal.emit(result)

class SystemHealthMonitor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("System Health Monitor")
        self.setGeometry(100, 100, 500, 450)

        self.layout = QVBoxLayout()
        self.status_label = QLabel("System Health Monitor", self)
        self.status_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.layout.addWidget(self.status_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.cpu_button = QPushButton("Check CPU Health", self)
        self.cpu_button.clicked.connect(self.start_cpu_check)
        self.layout.addWidget(self.cpu_button)

        self.gpu_button = QPushButton("Check GPU Health", self)
        self.gpu_button.clicked.connect(self.start_gpu_check)
        self.layout.addWidget(self.gpu_button)

        self.wifi_button = QPushButton("Check WiFi Stability", self)
        self.wifi_button.clicked.connect(self.start_wifi_check)
        self.layout.addWidget(self.wifi_button)

        self.duration_label = QLabel("Set Monitoring Duration (Seconds):", self)
        self.layout.addWidget(self.duration_label)
        self.duration_box = QSpinBox()
        self.duration_box.setRange(5, 60)
        self.duration_box.setValue(10)
        self.layout.addWidget(self.duration_box)

        if not is_admin():
            self.gpu_button.setEnabled(False)
            self.wifi_button.setEnabled(False)
            self.status_label.setText("Run as Admin to enable all features.")

        self.container = QWidget()
        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)

    def start_cpu_check(self):
        duration = self.duration_box.value()
        self.status_label.setText("Checking CPU Health...")
        self.cpu_thread = CPUCheckThread(duration)
        self.cpu_thread.result_signal.connect(self.update_status)
        self.cpu_thread.start()

    def start_gpu_check(self):
        self.status_label.setText("Checking GPU Health...")
        self.gpu_thread = GPUCheckThread()
        self.gpu_thread.result_signal.connect(self.update_status)
        self.gpu_thread.start()

    def start_wifi_check(self):
        self.status_label.setText("Checking WiFi Stability...")
        self.wifi_thread = WiFiCheckThread()
        self.wifi_thread.result_signal.connect(self.update_status)
        self.wifi_thread.start()

    def update_status(self, result):
        self.status_label.setText(result)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SystemHealthMonitor()
    window.show()
    sys.exit(app.exec())
