import sys
import base64
import os
import binascii
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLabel, QComboBox, QMessageBox, QLineEdit
)
from PyQt6.QtGui import QTextCursor, QTextCharFormat, QColor
from PyQt6.QtCore import Qt
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad

class EncryptionVisualizer(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Encryption Visualization Tool")
        self.setGeometry(100, 100, 900, 700)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Title
        self.title_label = QLabel("🔐 Encryption Visualization (RSA / AES)", self)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold;")

        # Algorithm Selection
        self.algorithm_label = QLabel("Select Encryption Algorithm:", self)
        self.algorithm_combo = QComboBox(self)
        self.algorithm_combo.addItems(["RSA", "AES"])
        self.algorithm_combo.currentTextChanged.connect(self.toggle_aes_key_input)

        # Input Text Box
        self.input_label = QLabel("Enter Your Message:")
        self.input_text = QTextEdit(self)

        # AES Key Input
        self.aes_key_label = QLabel("Enter a 256-bit AES Key (Optional, Leave Blank to Generate a Key):")
        self.aes_key_input = QLineEdit(self)
        self.aes_key_input.setPlaceholderText("Hex-encoded 32-byte (64 hex characters) key")
        self.aes_key_input.setEnabled(False)  # Disabled until AES is selected

        # Generate AES Key Button
        self.generate_key_button = QPushButton("🔑 Generate AES Key", self)
        self.generate_key_button.setEnabled(False)
        self.generate_key_button.clicked.connect(self.generate_aes_key)

        # Encrypt Button
        self.encrypt_button = QPushButton("🔒 Encrypt", self)
        self.encrypt_button.clicked.connect(self.encrypt_message)

        # Visualization Output
        self.output_label = QLabel("Encryption Process Visualization:")
        self.output_text = QTextEdit(self)
        self.output_text.setReadOnly(True)
        self.output_text.setStyleSheet("background-color: #f0f0f0; font-family: monospace;")

        # Layout Management
        layout.addWidget(self.title_label)
        layout.addWidget(self.algorithm_label)
        layout.addWidget(self.algorithm_combo)
        layout.addWidget(self.input_label)
        layout.addWidget(self.input_text)
        layout.addWidget(self.aes_key_label)
        layout.addWidget(self.aes_key_input)
        layout.addWidget(self.generate_key_button)
        layout.addWidget(self.encrypt_button)
        layout.addWidget(self.output_label)
        layout.addWidget(self.output_text)

        self.setLayout(layout)

    def toggle_aes_key_input(self):
        """Enable or disable AES key input based on selected algorithm."""
        is_aes = self.algorithm_combo.currentText() == "AES"
        self.aes_key_input.setEnabled(is_aes)
        self.generate_key_button.setEnabled(is_aes)

    def generate_aes_key(self):
        """Generates a new AES key and displays it in the input field."""
        key = os.urandom(32)  # Generate a 256-bit key
        key_hex = binascii.hexlify(key).decode()
        self.aes_key_input.setText(key_hex)
        QMessageBox.information(self, "AES Key Generated", "A new AES key has been generated.")

    def encrypt_message(self):
        """Handles encryption visualization based on selected algorithm."""
        message = self.input_text.toPlainText().strip()
        if not message:
            QMessageBox.warning(self, "Input Error", "Please enter a message to encrypt.")
            return

        algorithm = self.algorithm_combo.currentText()
        self.output_text.clear()

        if algorithm == "RSA":
            self.visualize_rsa_encryption(message)
        elif algorithm == "AES":
            self.visualize_aes_encryption(message)

    def visualize_rsa_encryption(self, message):
        """Visualizes RSA encryption process step-by-step."""
        self.append_output("🔑 Generating RSA Key Pair...")
        key = RSA.generate(2048)
        public_key = key.publickey()

        self.append_output("\n📜 Public Key (for Encryption):")
        self.append_output(public_key.export_key().decode(), highlight=True)

        self.append_output("\n🔒 Encrypting Message with Public Key...")
        cipher_rsa = PKCS1_OAEP.new(public_key)
        encrypted_message = cipher_rsa.encrypt(message.encode())

        self.append_output("\n🔐 Encrypted Message (Hex):")
        encrypted_hex = binascii.hexlify(encrypted_message).decode()
        self.append_output(encrypted_hex, highlight=True)

        self.append_output("\n✅ RSA Encryption Complete!")

    def visualize_aes_encryption(self, message):
        """Visualizes AES encryption process step-by-step."""
        user_key_hex = self.aes_key_input.text().strip()

        # Validate user input or generate a new key
        if user_key_hex:
            try:
                key = binascii.unhexlify(user_key_hex)
                if len(key) != 32:
                    raise ValueError
            except (binascii.Error, ValueError):
                QMessageBox.warning(self, "Invalid AES Key", "Please enter a valid 256-bit (64 hex characters) AES key.")
                return
        else:
            key = os.urandom(32)  # Generate 256-bit key

        iv = os.urandom(16)  # AES Initialization Vector

        self.append_output("\n📝 AES Key (Hex):")
        self.append_output(binascii.hexlify(key).decode(), highlight=True)

        self.append_output("\n📍 IV (Initialization Vector):")
        self.append_output(binascii.hexlify(iv).decode(), highlight=True)

        self.append_output("\n🔄 Padding & Encrypting Message...")
        cipher = AES.new(key, AES.MODE_CBC, iv)
        padded_message = pad(message.encode(), AES.block_size)
        encrypted_message = cipher.encrypt(padded_message)

        self.append_output("\n🔐 Encrypted Message (Base64):")
        encrypted_b64 = base64.b64encode(iv + encrypted_message).decode()
        self.append_output(encrypted_b64, highlight=True)

        self.append_output("\n✅ AES Encryption Complete!")

    def append_output(self, text, highlight=False):
        """Appends text to the output box with optional highlighting."""
        self.output_text.moveCursor(QTextCursor.MoveOperation.End)
        fmt = QTextCharFormat()
        if highlight:
            fmt.setForeground(QColor("#d32f2f"))  # Red for encrypted data
            fmt.setFontWeight(75)  # Bold text
        self.output_text.setCurrentCharFormat(fmt)
        self.output_text.append(text)
        self.output_text.setCurrentCharFormat(QTextCharFormat())  # Reset formatting

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EncryptionVisualizer()
    window.show()
    sys.exit(app.exec())