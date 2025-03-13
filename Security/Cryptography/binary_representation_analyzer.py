import sys
import math
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QTextEdit, QLabel
from PyQt6.QtCore import Qt


class BinaryRepresentationApp(QWidget):
    def __init__(self):
        super().__init__()
        
        # Set up the window
        self.setWindowTitle('Binary Representation Details')
        self.setGeometry(100, 100, 800, 600)
        
        # Create layout
        self.layout = QVBoxLayout()

        # Create UI elements
        self.label = QLabel("Enter the binary representation:")
        self.layout.addWidget(self.label)
        
        self.binary_input = QLineEdit()
        self.binary_input.setPlaceholderText("Enter binary string here (e.g., 00101111 00101010)...")
        self.layout.addWidget(self.binary_input)

        self.process_button = QPushButton("Process Binary")
        self.layout.addWidget(self.process_button)

        self.details_output = QTextEdit()
        self.details_output.setReadOnly(True)
        self.layout.addWidget(self.details_output)
        
        # Connect the button click event to process_binary function
        self.process_button.clicked.connect(self.process_binary)

        # Set the layout to the window
        self.setLayout(self.layout)

    def process_binary(self):
        binary_string = self.binary_input.text().strip()

        # Remove spaces and validate the binary string
        binary_string = binary_string.replace(" ", "")

        if not all(char in '01' for char in binary_string):
            self.details_output.setText("Invalid binary input. Please enter a valid binary string.")
            return

        # Process binary string
        details = self.analyze_binary(binary_string)
        
        # Show the result in the QTextEdit
        self.details_output.setText(details)

    def analyze_binary(self, binary_string):
        # Calculate basic details
        num_bits = len(binary_string)
        num_ones = binary_string.count('1')
        num_zeros = num_bits - num_ones
        hex_rep = hex(int(binary_string, 2))
        
        # File size calculation (in bytes and kilobytes)
        file_size_bytes = num_bits // 8
        file_size_kb = file_size_bytes / 1024

        # Breakdown into bytes
        byte_representation = self.get_byte_representation(binary_string)

        # Entropy calculation
        entropy = self.calculate_entropy(binary_string)
        
        # Attempt ASCII or UTF-8 decoding
        decoded_text = self.decode_ascii_or_utf8(binary_string)

        # Constructing the details string
        details = f"Binary Length: {num_bits} bits\n"
        details += f"File Size: {file_size_bytes} bytes ({file_size_kb:.2f} KB)\n"
        details += f"Hexadecimal: {hex_rep}\n"
        details += f"Number of 1s: {num_ones}\n"
        details += f"Number of 0s: {num_zeros}\n"
        details += f"Set Bit Percentage: {100 * num_ones / num_bits:.2f}%\n"
        details += f"Clear Bit Percentage: {100 * num_zeros / num_bits:.2f}%\n"

        # Byte breakdown display
        details += "\nByte Breakdown (Hex, Decimal, Binary):\n"
        details += byte_representation

        # Entropy detail
        details += f"\nEntropy: {entropy:.4f}\n"
        
        # Decoded text if possible
        if decoded_text:
            details += f"\nDecoded Text (ASCII/UTF-8): {decoded_text}\n"
        else:
            details += "\nUnable to decode as ASCII or UTF-8.\n"

        return details

    def get_byte_representation(self, binary_string):
        # Breakdown binary string into bytes (8-bit segments)
        bytes_list = [binary_string[i:i + 8] for i in range(0, len(binary_string), 8)]
        byte_details = ""
        
        for byte in bytes_list:
            if len(byte) == 8:  # Ensure the byte is complete
                hex_val = hex(int(byte, 2))
                dec_val = int(byte, 2)
                byte_details += f"{byte} | {hex_val} | {dec_val}\n"
        return byte_details

    def calculate_entropy(self, binary_string):
        # Calculate entropy for the binary string
        num_bits = len(binary_string)
        prob_0 = binary_string.count('0') / num_bits
        prob_1 = binary_string.count('1') / num_bits
        
        # Entropy formula
        entropy = 0
        if prob_0 > 0:
            entropy -= prob_0 * math.log2(prob_0)
        if prob_1 > 0:
            entropy -= prob_1 * math.log2(prob_1)
        
        return entropy

    def decode_ascii_or_utf8(self, binary_string):
        # Try to interpret the binary string as ASCII or UTF-8
        try:
            # Ensure the binary string is a multiple of 8 for valid byte decoding
            if len(binary_string) % 8 == 0:
                # Convert binary string to bytes
                byte_array = [binary_string[i:i+8] for i in range(0, len(binary_string), 8)]
                byte_list = [int(b, 2) for b in byte_array]
                byte_data = bytes(byte_list)
                
                # Try decoding as ASCII or UTF-8
                try:
                    decoded_text = byte_data.decode('utf-8')
                    return decoded_text
                except UnicodeDecodeError:
                    return None  # If UTF-8 fails, return None
            return None
        except Exception:
            return None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BinaryRepresentationApp()
    window.show()
    sys.exit(app.exec())