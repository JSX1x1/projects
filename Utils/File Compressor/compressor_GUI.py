import sys
import os
import zlib
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QFileDialog, QVBoxLayout, QSlider, QTextEdit
)
from PyQt6.QtCore import Qt


class AdvancedCompressionTool(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("File Compression Tool")
        self.setGeometry(300, 200, 650, 450)
        self.setStyleSheet("background-color: #121212; color: white;")

        layout = QVBoxLayout()

        # File selection
        self.file_label = QLabel("Select a file to compress:")
        layout.addWidget(self.file_label)
        self.file_button = QPushButton("Choose File")
        self.file_button.clicked.connect(self.select_file)
        layout.addWidget(self.file_button)

        # Compression level slider
        self.compression_label = QLabel("Compression Level (1 - 20):")
        layout.addWidget(self.compression_label)
        self.compression_slider = QSlider(Qt.Orientation.Horizontal)
        self.compression_slider.setMinimum(1)
        self.compression_slider.setMaximum(20)
        self.compression_slider.setValue(5)
        self.compression_slider.valueChanged.connect(self.update_compression_level)
        layout.addWidget(self.compression_slider)

        # Live compression stats
        self.size_info = QTextEdit()
        self.size_info.setReadOnly(True)
        self.size_info.setStyleSheet("background-color: #1e1e1e; color: #00ff00; font-size: 14px;")
        layout.addWidget(self.size_info)

        # Compress & Decompress buttons
        self.compress_button = QPushButton("Compress File")
        self.compress_button.clicked.connect(self.compress_file)
        layout.addWidget(self.compress_button)

        self.decompress_button = QPushButton("Decompress File")
        self.decompress_button.clicked.connect(self.decompress_file)
        layout.addWidget(self.decompress_button)

        self.setLayout(layout)

        # Variables
        self.file_path = None
        self.compressed_path = None

    def select_file(self):
        """Select a file for compression."""
        self.file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*)")
        if self.file_path and os.path.exists(self.file_path):
            self.file_label.setText(f"📂 Selected File: {self.file_path}")
            self.update_compression_level()
        else:
            self.size_info.setText("❌ File selection failed or file does not exist!")

    def update_compression_level(self):
        """Live update of compressed size estimate based on slider value."""
        if not self.file_path or not os.path.exists(self.file_path):
            self.size_info.setText("❌ No valid file selected!")
            return

        compression_level = self.compression_slider.value()

        try:
            original_size = os.path.getsize(self.file_path)
            if original_size == 0:
                self.size_info.setText("⚠️ Cannot compress an empty file!")
                return

            with open(self.file_path, "rb") as f:
                data = f.read()

            # Ensure file is not empty before compression
            if not data:
                self.size_info.setText("⚠️ File is empty or unreadable!")
                return

            # zlib compression level maps from 1-20 slider -> 1-9 valid range
            zlib_level = min(9, max(1, compression_level // 2))

            compressed_data = zlib.compress(data, zlib_level)
            compressed_size = len(compressed_data)
            reduction = 100 - ((compressed_size / original_size) * 100)

            # Gain/Loss ratio
            gain_loss_ratio = original_size / compressed_size if compressed_size > 0 else 0

            # Color coding based on efficiency
            color = "#00ff00" if reduction > 0 else "#ff0000"  # Green for reduction, Red for increase

            self.size_info.setStyleSheet(f"background-color: #1e1e1e; color: {color}; font-size: 14px;")
            self.size_info.setText(
                f"📊 Compression Level: {compression_level} (Zlib: {zlib_level})\n"
                f"📏 Original Size: {original_size / 1024:.2f} KB\n"
                f"📦 Estimated Compressed Size: {compressed_size / 1024:.2f} KB\n"
                f"🔽 Reduction: {reduction:.2f}%\n"
                f"📈 Gain/Loss Ratio: {gain_loss_ratio:.2f}"
            )
        except Exception as e:
            self.size_info.setText(f"❌ Error updating compression level: {str(e)}")

    def compress_file(self):
        """Compress the selected file."""
        if not self.file_path:
            self.size_info.setText("❌ Please select a file first!")
            return

        compression_level = self.compression_slider.value()
        self.compressed_path = self.file_path + ".compressed"

        try:
            with open(self.file_path, "rb") as f:
                data = f.read()

            if not data:
                self.size_info.setText("⚠️ Cannot compress an empty file!")
                return

            zlib_level = min(9, max(1, compression_level // 2))

            compressed_data = zlib.compress(data, zlib_level)

            with open(self.compressed_path, "wb") as f:
                f.write(compressed_data)

            compressed_size = os.path.getsize(self.compressed_path)
            original_size = os.path.getsize(self.file_path)
            reduction = 100 - ((compressed_size / original_size) * 100)
            gain_loss_ratio = original_size / compressed_size if compressed_size > 0 else 0

            color = "#00ff00" if reduction > 0 else "#ff0000"

            self.size_info.setStyleSheet(f"background-color: #1e1e1e; color: {color}; font-size: 14px;")
            self.size_info.append(f"✅ File compressed successfully: {self.compressed_path}")
            self.size_info.append(
                f"📏 Original Size: {original_size / 1024:.2f} KB\n"
                f"📦 Compressed Size: {compressed_size / 1024:.2f} KB\n"
                f"🔽 Reduction: {reduction:.2f}%\n"
                f"📈 Gain/Loss Ratio: {gain_loss_ratio:.2f}"
            )
        except Exception as e:
            self.size_info.setText(f"❌ Compression failed: {str(e)}")

    def decompress_file(self):
        """Decompress the selected file."""
        if not self.compressed_path:
            self.size_info.setText("❌ No compressed file found!")
            return

        decompressed_path = self.compressed_path.replace(".compressed", ".decompressed")

        try:
            with open(self.compressed_path, "rb") as f:
                compressed_data = f.read()

            decompressed_data = zlib.decompress(compressed_data)

            with open(decompressed_path, "wb") as f:
                f.write(decompressed_data)

            self.size_info.append(f"✅ File decompressed successfully: {decompressed_path}")
        except zlib.error:
            self.size_info.append("❌ Decompression failed! File may be corrupted.")


# Run Application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AdvancedCompressionTool()
    window.show()
    sys.exit(app.exec())
