import sys
import random
import numpy as np
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QTextEdit, QFileDialog, QHBoxLayout, QMessageBox
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from PIL import Image, ImageQt


class ImageCorruptor(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image Corruptor - Detailed Process Output")
        self.setGeometry(100, 100, 900, 600)

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Image Selection Button
        self.select_image_button = QPushButton("📂 Select Image", self)
        self.select_image_button.clicked.connect(self.load_image)

        # Image Display
        self.image_label = QLabel("Original Image", self)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.corrupted_image_label = QLabel("Corrupted Image", self)
        self.corrupted_image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Process Output Box
        self.process_output = QTextEdit(self)
        self.process_output.setReadOnly(True)
        self.process_output.setStyleSheet("background-color: #f0f0f0; font-family: monospace;")
        self.process_output.setPlaceholderText("Corruption process details will appear here...")

        # Corrupt Button
        self.corrupt_button = QPushButton("⚡ Corrupt Image", self)
        self.corrupt_button.setEnabled(False)
        self.corrupt_button.clicked.connect(self.corrupt_image)

        # Save Button
        self.save_button = QPushButton("💾 Save Corrupted Image", self)
        self.save_button.setEnabled(False)
        self.save_button.clicked.connect(self.save_corrupted_image)

        # Layout Arrangement
        image_layout = QHBoxLayout()
        image_layout.addWidget(self.image_label)
        image_layout.addWidget(self.corrupted_image_label)

        layout.addWidget(self.select_image_button)
        layout.addLayout(image_layout)
        layout.addWidget(self.corrupt_button)
        layout.addWidget(self.process_output)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

        self.original_image = None
        self.corrupted_image = None
        self.image_path = None

    def load_image(self):
        """Loads an image file selected by the user."""
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.jpg *.jpeg *.bmp)")

        if file_path:
            self.image_path = file_path
            self.original_image = Image.open(file_path)
            self.display_image(self.original_image, self.image_label)
            self.process_output.clear()
            self.process_output.append(f"✅ Loaded image: {file_path}")
            self.corrupt_button.setEnabled(True)
            self.save_button.setEnabled(False)

    def display_image(self, image, label):
        """Displays a given image in the provided QLabel."""
        qt_image = ImageQt.ImageQt(image)
        pixmap = QPixmap.fromImage(qt_image)
        label.setPixmap(pixmap.scaled(300, 300, Qt.AspectRatioMode.KeepAspectRatio))

    def corrupt_image(self):
        """Applies corruption to the image with detailed output."""
        if self.original_image is None:
            return

        self.process_output.clear()
        self.process_output.append("⚠️ Starting Image Corruption Process...\n")

        image_data = np.array(self.original_image)
        height, width, channels = image_data.shape

        self.process_output.append(f"🔍 Image Size: {width}x{height} pixels, Channels: {channels}\n")
        corruption_type = random.choice(["bit_flip", "random_noise", "byte_injection"])

        if corruption_type == "bit_flip":
            self.process_output.append("🛠 Applying Bit-Flipping Corruption...")
            num_pixels = random.randint(50, 500)  # Number of pixels to flip
            for _ in range(num_pixels):
                x, y = random.randint(0, width - 1), random.randint(0, height - 1)
                channel = random.randint(0, channels - 1)
                original_value = image_data[y, x, channel]
                image_data[y, x, channel] ^= 0xFF  # Flip bits
                self.process_output.append(f"⚡ Pixel ({x},{y}) Channel {channel}: {original_value} -> {image_data[y, x, channel]}")

        elif corruption_type == "random_noise":
            self.process_output.append("🔊 Adding Random Noise...")
            noise_intensity = random.randint(10, 100)
            noise = np.random.randint(-noise_intensity, noise_intensity, image_data.shape, dtype=np.int16)
            image_data = np.clip(image_data.astype(np.int16) + noise, 0, 255).astype(np.uint8)

        elif corruption_type == "byte_injection":
            self.process_output.append("🛠 Injecting Random Byte Corruption...")
            num_corruptions = random.randint(100, 1000)
            for _ in range(num_corruptions):
                x, y = random.randint(0, width - 1), random.randint(0, height - 1)
                channel = random.randint(0, channels - 1)
                corruption_value = random.randint(0, 255)
                self.process_output.append(f"⚡ Injecting at ({x},{y}) Channel {channel}: {image_data[y, x, channel]} -> {corruption_value}")
                image_data[y, x, channel] = corruption_value

        self.process_output.append("\n✅ Image Corruption Complete!")
        self.corrupted_image = Image.fromarray(image_data)
        self.display_image(self.corrupted_image, self.corrupted_image_label)
        self.save_button.setEnabled(True)

    def save_corrupted_image(self):
        """Saves the corrupted image."""
        if self.corrupted_image is None:
            return

        save_path, _ = QFileDialog.getSaveFileName(self, "Save Corrupted Image", "", "PNG Files (*.png);;JPEG Files (*.jpg);;All Files (*)")

        if save_path:
            self.corrupted_image.save(save_path)
            self.process_output.append(f"\n💾 Corrupted image saved at: {save_path}")
            QMessageBox.information(self, "Success", "Corrupted image saved successfully!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageCorruptor()
    window.show()
    sys.exit(app.exec())
