import sys
import os
import ctypes
import psutil
import re
import struct
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel,
    QPushButton, QListWidget, QFileDialog, QMessageBox, QProgressBar,
    QComboBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from tqdm import tqdm

# **Check for Admin Privileges**
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# **Thread for Scanning Deleted Files**
class ScanThread(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(list)

    def __init__(self, disk_path):
        super().__init__()
        self.disk_path = disk_path

    def run(self):
        """Scans disk sectors for deleted file signatures."""
        deleted_files = []

        # **File Type Signatures**
        signatures = {
            "jpg": b"\xFF\xD8\xFF",
            "png": b"\x89PNG\r\n\x1A\n",
            "pdf": b"%PDF",
            "docx": b"PK\x03\x04",
            "xlsx": b"PK\x03\x04",
            "pptx": b"PK\x03\x04",
            "mp4": b"\x00\x00\x00\x18ftypmp4",
            "zip": b"PK\x03\x04",
            "rar": b"Rar!\x1A\x07\x00",
            "exe": b"MZ",
            "mp3": b"ID3",
            "txt": b"\xEF\xBB\xBF"  # UTF-8 encoded text
        }

        try:
            with open(self.disk_path, "rb") as disk:
                disk_data = disk.read()

                for file_type, signature in signatures.items():
                    matches = [m.start() for m in re.finditer(re.escape(signature), disk_data)]

                    if matches:
                        for i, start in enumerate(matches):
                            deleted_files.append((file_type, start))

                            # **Update progress**
                            self.progress.emit(int((i / len(matches)) * 100))

        except Exception as e:
            print(f"Error: {e}")

        self.finished.emit(deleted_files)

# **Main File Recovery Application**
class FileRecoveryApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("File Recovery Tool")
        self.setGeometry(200, 200, 850, 600)
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
            self.warning_label.setText("⚠️ WARNING: No Admin Privileges! Recovery functions are disabled!")
        else:
            self.warning_label.setText("✅ Admin Privileges Detected")

        # **Drive Selection**
        self.drive_label = QLabel("Select a Drive:")
        self.layout.addWidget(self.drive_label)

        self.drive_selector = QComboBox()
        self.layout.addWidget(self.drive_selector)

        self.scan_button = QPushButton("Scan for Deleted Files")
        self.scan_button.setStyleSheet("background-color: #444; padding: 10px;")
        self.scan_button.clicked.connect(self.scan_drive)
        self.layout.addWidget(self.scan_button)

        # **File List**
        self.file_list = QListWidget()
        self.layout.addWidget(self.file_list)

        # **Progress Bar**
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(100)
        self.progress_bar.setTextVisible(True)
        self.layout.addWidget(self.progress_bar)

        # **Recover Button**
        self.recover_button = QPushButton("Recover Selected File")
        self.recover_button.setStyleSheet("background-color: #0066cc; padding: 10px;")
        self.recover_button.clicked.connect(self.recover_file)
        self.layout.addWidget(self.recover_button)

        # **Disable functions if no admin rights**
        if not self.admin_status:
            self.scan_button.setEnabled(False)
            self.recover_button.setEnabled(False)
            self.drive_selector.setEnabled(False)

        # **Populate Drive List**
        self.get_available_drives()

    def get_available_drives(self):
        """List all available drives."""
        partitions = psutil.disk_partitions()
        for partition in partitions:
            self.drive_selector.addItem(partition.device)

    def scan_drive(self):
        """Starts scanning for deleted files."""
        self.file_list.clear()
        selected_drive = self.drive_selector.currentText()
        
        if not selected_drive:
            QMessageBox.warning(self, "Error", "No drive selected!")
            return

        QMessageBox.information(self, "Scanning", f"Scanning drive: {selected_drive}")

        self.scan_thread = ScanThread(selected_drive)
        self.scan_thread.progress.connect(self.progress_bar.setValue)
        self.scan_thread.finished.connect(self.display_files)
        self.scan_thread.start()

    def display_files(self, files):
        """Displays detected deleted files."""
        self.file_list.clear()

        if not files:
            self.file_list.addItem("No recoverable files found.")
            return

        for file_type, sector in files:
            self.file_list.addItem(f"{file_type.upper()} found at sector {sector}")

    def recover_file(self):
        """Recovers a selected file."""
        selected_item = self.file_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Error", "No file selected!")
            return

        file_info = selected_item.text().split(" found at sector ")
        file_type, sector = file_info[0].lower(), int(file_info[1])

        selected_drive = self.drive_selector.currentText()
        recovery_path = QFileDialog.getExistingDirectory(self, "Select Recovery Location")

        if not recovery_path:
            QMessageBox.warning(self, "Error", "No recovery location selected!")
            return

        try:
            with open(selected_drive, "rb") as disk:
                disk.seek(sector)
                file_data = disk.read(10 * 1024 * 1024)  # Recover up to 10MB

                output_path = os.path.join(recovery_path, f"recovered.{file_type}")
                with open(output_path, "wb") as f:
                    f.write(file_data)

            QMessageBox.information(self, "Success", f"File recovered to: {output_path}")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

# **Run the Application**
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileRecoveryApp()
    window.show()
    sys.exit(app.exec())
