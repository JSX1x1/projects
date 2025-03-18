import sys
import os
import hashlib
import stat
import time
import magic
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QTextEdit, QProgressBar, QMessageBox
)
from PyQt6.QtCore import QThread, pyqtSignal


class IntegrityCheckerThread(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(str)

    def __init__(self, path, is_directory):
        super().__init__()
        self.path = path
        self.is_directory = is_directory

    def run(self):
        """Performs integrity checks on the selected file or directory."""
        if self.is_directory:
            files = list(Path(self.path).rglob("*"))
        else:
            files = [Path(self.path)]

        total_files = len(files)
        if total_files == 0:
            self.finished.emit("No valid files found.")
            return

        results = []
        for i, file in enumerate(files):
            if file.is_file():
                results.append(self.analyze_file(file))

            self.progress.emit(int((i + 1) / total_files * 100))

        self.finished.emit("\n".join(results))

    def analyze_file(self, file_path):
        """Analyzes a file for integrity and security checks."""
        try:
            file_info = f"File: {file_path}\n"
            file_info += f"Size: {file_path.stat().st_size} bytes\n"
            file_info += f"Last Modified: {time.ctime(file_path.stat().st_mtime)}\n"
            file_info += f"Last Accessed: {time.ctime(file_path.stat().st_atime)}\n"

            # Checksum
            sha256_hash = self.calculate_checksum(file_path, "sha256")
            md5_hash = self.calculate_checksum(file_path, "md5")
            file_info += f"SHA-256: {sha256_hash}\n"
            file_info += f"MD5: {md5_hash}\n"

            # Encoding & MIME Type Detection
            mime = magic.Magic(mime=True)
            encoding = magic.Magic(mime_encoding=True)
            file_info += f"MIME Type: {mime.from_file(str(file_path))}\n"
            file_info += f"Encoding: {encoding.from_file(str(file_path))}\n"

            # File Readability Ratio
            readability_ratio = self.calculate_readability(file_path)
            file_info += f"Readability Ratio: {readability_ratio:.2f}%\n"

            # File Entropy (randomness detection)
            entropy_value = self.calculate_entropy(file_path)
            file_info += f"Entropy: {entropy_value:.2f} (Higher values indicate encrypted/compressed data)\n"

            # Hidden or System File Detection
            if file_path.name.startswith(".") or (
                os.name == "nt" and file_path.stat().st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN
            ):
                file_info += "Status: Hidden/System File\n"

            # Symbolic Link & Broken Link Check
            if file_path.is_symlink():
                target = os.readlink(file_path)
                file_info += f"Symbolic Link -> {target}\n"

            # File Permissions
            permissions = stat.filemode(file_path.stat().st_mode)
            file_info += f"Permissions: {permissions}\n"

            return file_info + "\n" + "-" * 60 + "\n"

        except Exception as e:
            return f"Error processing {file_path}: {e}\n"

    def calculate_checksum(self, file_path, algorithm="sha256"):
        """Calculates the checksum of a file."""
        hash_func = hashlib.sha256() if algorithm == "sha256" else hashlib.md5()
        try:
            with open(file_path, "rb") as f:
                while chunk := f.read(8192):
                    hash_func.update(chunk)
            return hash_func.hexdigest()
        except Exception:
            return "Unreadable File"

    def calculate_readability(self, file_path):
        """Estimates the readability ratio of a file (based on binary vs. text content)."""
        try:
            with open(file_path, "rb") as f:
                data = f.read(1024)
                text_chars = sum(1 for byte in data if 32 <= byte < 127 or byte in (9, 10, 13))
                return (text_chars / len(data)) * 100 if data else 0
        except:
            return 0

    def calculate_entropy(self, file_path):
        """Calculates the entropy (randomness) of a file."""
        try:
            with open(file_path, "rb") as f:
                data = f.read()
            if not data:
                return 0
            entropy = -sum((data.count(byte) / len(data)) * (data.count(byte) / len(data)).bit_length() for byte in set(data))
            return entropy
        except:
            return 0


class IntegrityCheckerGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Integrity Checker")
        self.setGeometry(100, 100, 600, 500)

        self.layout = QVBoxLayout()

        self.label_status = QLabel("Select a file or folder for integrity check.")
        self.layout.addWidget(self.label_status)

        self.btn_select_file = QPushButton("Select File")
        self.btn_select_file.clicked.connect(self.select_file)
        self.layout.addWidget(self.btn_select_file)

        self.btn_select_folder = QPushButton("Select Folder")
        self.btn_select_folder.clicked.connect(self.select_folder)
        self.layout.addWidget(self.btn_select_folder)

        self.btn_start_check = QPushButton("Start Integrity Check")
        self.btn_start_check.clicked.connect(self.start_integrity_check)
        self.btn_start_check.setEnabled(False)
        self.layout.addWidget(self.btn_start_check)

        self.progress_bar = QProgressBar()
        self.layout.addWidget(self.progress_bar)

        self.text_output = QTextEdit()
        self.text_output.setReadOnly(True)
        self.layout.addWidget(self.text_output)

        self.btn_save_results = QPushButton("Save Results to File")
        self.btn_save_results.clicked.connect(self.save_results)
        self.btn_save_results.setEnabled(False)
        self.layout.addWidget(self.btn_save_results)

        self.setLayout(self.layout)
        self.selected_path = None
        self.is_directory = False
        self.results = ""

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File")
        if file_path:
            self.selected_path = file_path
            self.is_directory = False
            self.label_status.setText(f"Selected File: {file_path}")
            self.btn_start_check.setEnabled(True)

    def select_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_path:
            self.selected_path = folder_path
            self.is_directory = True
            self.label_status.setText(f"Selected Folder: {folder_path}")
            self.btn_start_check.setEnabled(True)

    def start_integrity_check(self):
        self.btn_start_check.setEnabled(False)
        self.progress_bar.setValue(0)
        self.text_output.clear()

        self.worker = IntegrityCheckerThread(self.selected_path, self.is_directory)
        self.worker.progress.connect(self.progress_bar.setValue)
        self.worker.finished.connect(self.on_check_complete)
        self.worker.start()

    def on_check_complete(self, results):
        self.results = results
        self.text_output.setText(results)
        self.btn_start_check.setEnabled(True)
        self.btn_save_results.setEnabled(True)

    def save_results(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Results", "integrity_results.txt", "Text Files (*.txt)")
        if file_name:
            with open(file_name, "w") as f:
                f.write(self.results)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = IntegrityCheckerGUI()
    window.show()
    sys.exit(app.exec())
