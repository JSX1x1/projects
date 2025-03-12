import sys
import os
import tarfile
import zipfile
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QFileDialog, QVBoxLayout, QTextEdit
)
from PyQt6.QtCore import Qt


class TarGzUnpacker(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("TAR.GZ Unpacker & Converter")
        self.setGeometry(300, 200, 600, 400)
        self.setStyleSheet("background-color: #121212; color: white;")

        layout = QVBoxLayout()

        # File selection
        self.file_label = QLabel("Select a .tar.gz file to extract and convert:")
        layout.addWidget(self.file_label)
        self.file_button = QPushButton("Choose File")
        self.file_button.clicked.connect(self.select_file)
        layout.addWidget(self.file_button)

        # Extraction log
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setStyleSheet("background-color: #1e1e1e; color: #00ff00; font-size: 14px;")
        layout.addWidget(self.log_output)

        # Extract & Convert buttons
        self.extract_button = QPushButton("Extract .tar.gz")
        self.extract_button.clicked.connect(self.extract_tar_gz)
        layout.addWidget(self.extract_button)

        self.convert_button = QPushButton("Convert Extracted Folder to .zip")
        self.convert_button.clicked.connect(self.convert_to_zip)
        layout.addWidget(self.convert_button)

        self.setLayout(layout)

        # Variables
        self.file_path = None
        self.extract_folder = None

    def select_file(self):
        """Select a .tar.gz file for extraction."""
        self.file_path, _ = QFileDialog.getOpenFileName(self, "Select .tar.gz File", "", "Tar GZ Archives (*.tar.gz)")
        if self.file_path:
            self.file_label.setText(f"📂 Selected File: {self.file_path}")
            self.log_output.setText(f"📝 Ready to extract: {os.path.basename(self.file_path)}")

    def extract_tar_gz(self):
        """Extracts the selected .tar.gz file."""
        if not self.file_path:
            self.log_output.setText("❌ Please select a .tar.gz file first!")
            return

        try:
            self.extract_folder = os.path.splitext(self.file_path)[0]  # Remove .gz
            os.makedirs(self.extract_folder, exist_ok=True)

            self.log_output.append(f"📦 Extracting: {self.file_path}...")
            with tarfile.open(self.file_path, "r:gz") as tar:
                tar.extractall(self.extract_folder)

            self.log_output.append(f"✅ Extraction completed: {self.extract_folder}")
        except Exception as e:
            self.log_output.append(f"❌ Extraction failed: {str(e)}")

    def convert_to_zip(self):
        """Converts extracted files to a ZIP archive."""
        if not self.extract_folder or not os.path.exists(self.extract_folder):
            self.log_output.setText("❌ No extracted folder found! Extract a .tar.gz file first.")
            return

        try:
            zip_file = self.extract_folder + ".zip"
            self.log_output.append(f"🔄 Converting '{self.extract_folder}' to ZIP...")

            with zipfile.ZipFile(zip_file, "w", zipfile.ZIP_DEFLATED) as zipf:
                for root, _, files in os.walk(self.extract_folder):
                    for file in files:
                        file_path = os.path.join(root, file)
                        zipf.write(file_path, os.path.relpath(file_path, self.extract_folder))

            self.log_output.append(f"✅ Conversion completed: {zip_file}")
        except Exception as e:
            self.log_output.append(f"❌ ZIP conversion failed: {str(e)}")


# Run Application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TarGzUnpacker()
    window.show()
    sys.exit(app.exec())