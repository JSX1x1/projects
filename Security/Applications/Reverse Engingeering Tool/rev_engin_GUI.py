import sys
import os
import re
import base64
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QFileDialog, QTextEdit, QComboBox, QProgressBar, QRadioButton, QGroupBox
)
from PyQt6.QtCore import Qt
from capstone import *
import pefile  # To handle PE files and extract headers, sections
import hashlib
import zlib
import math

class ReverseEngineeringTool(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Reverse Engineering Tool")
        self.setGeometry(300, 300, 800, 600)

        layout = QVBoxLayout()

        self.label = QLabel("Select a binary or script file:")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # File Selection Button
        self.select_file_btn = QPushButton("Select File")
        self.select_file_btn.clicked.connect(self.select_file)
        
        # File Type Analysis Options
        self.analysis_group = QGroupBox("Choose Analysis Type")
        self.analysis_layout = QVBoxLayout()
        
        self.disassemble_btn = QRadioButton("Disassemble Binary")
        self.analyze_binary_btn = QRadioButton("Analyze Binary")
        self.deobfuscate_btn = QRadioButton("Deobfuscate Malware")
        
        self.analysis_layout.addWidget(self.disassemble_btn)
        self.analysis_layout.addWidget(self.analyze_binary_btn)
        self.analysis_layout.addWidget(self.deobfuscate_btn)
        self.analysis_group.setLayout(self.analysis_layout)
        
        self.analysis_type = "disassemble"  # Default analysis type

        # Results area
        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)

        # Progress bar
        self.progress_bar = QProgressBar()
        
        # Action buttons
        self.scan_btn = QPushButton("Start Analysis")
        self.scan_btn.clicked.connect(self.start_analysis)

        # Add widgets to layout
        layout.addWidget(self.label)
        layout.addWidget(self.select_file_btn)
        layout.addWidget(self.analysis_group)
        layout.addWidget(self.scan_btn)
        layout.addWidget(self.result_area)
        layout.addWidget(self.progress_bar)
        
        self.setLayout(layout)
        self.selected_file = None

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File")
        if file_path:
            self.selected_file = file_path
            self.label.setText(f"Selected File: {file_path}")

    def start_analysis(self):
        if not self.selected_file:
            self.result_area.append("[!] No file selected!")
            return
        
        # Reset the result area
        self.result_area.clear()
        self.progress_bar.setValue(0)

        if self.disassemble_btn.isChecked():
            self.analysis_type = "disassemble"
            self.result_area.append(f"[Scanning] Disassembling {self.selected_file}...")
            self.disassemble_binary(self.selected_file)
        
        elif self.analyze_binary_btn.isChecked():
            self.analysis_type = "analyze"
            self.result_area.append(f"[Scanning] Analyzing Binary {self.selected_file}...")
            self.analyze_binary(self.selected_file)
        
        elif self.deobfuscate_btn.isChecked():
            self.analysis_type = "deobfuscate"
            self.result_area.append(f"[Scanning] Deobfuscating {self.selected_file}...")
            self.deobfuscate_file(self.selected_file)
        
        else:
            self.result_area.append("[!] Please select an analysis type!")

    def disassemble_binary(self, file_path):
        try:
            with open(file_path, "rb") as f:
                code = f.read()

            md = Cs(CS_ARCH_X86, CS_MODE_64)
            disassembly = ""
            for i in md.disasm(code, 0x1000):
                disassembly += f"{i.address}: {i.mnemonic} {i.op_str}\n"
            
            self.result_area.append(disassembly)
            self.progress_bar.setValue(100)
        except Exception as e:
            self.result_area.append(f"[Error] {str(e)}")
            self.progress_bar.setValue(0)

    def analyze_binary(self, file_path):
        try:
            # PE file analysis (for Windows binaries)
            if file_path.lower().endswith(".exe"):
                self.analyze_pe(file_path)
            else:
                # Placeholder for analysis of other binary formats
                self.result_area.append("[⚠] Unsupported binary format!")
            
            self.progress_bar.setValue(100)
        except Exception as e:
            self.result_area.append(f"[Error] {str(e)}")
            self.progress_bar.setValue(0)

    def analyze_pe(self, file_path):
        try:
            pe = pefile.PE(file_path)

            # Get sections information
            sections = pe.sections
            self.result_area.append(f"Sections: {len(sections)}\n")
            for section in sections:
                self.result_area.append(f"Section: {section.Name.decode('utf-8').strip()}")
                self.result_area.append(f"Virtual Size: {section.Misc_VirtualSize}")
                self.result_area.append(f"Raw Data Size: {section.SizeOfRawData}")
                self.result_area.append(f"Entropy: {self.calculate_entropy(section.get_data())}")

            # Detecting suspicious patterns like executable sections with high entropy (packed binaries)
            for section in sections:
                if self.is_suspicious_section(section):
                    self.result_area.append(f"[⚠] Suspicious Section: {section.Name.decode('utf-8').strip()}")

            self.check_strings_in_binary(file_path)

        except Exception as e:
            self.result_area.append(f"[Error] PE Analysis failed: {str(e)}")
    
    def calculate_entropy(self, data):
        return -sum([(data.count(chr(i)) / len(data)) * (math.log2(data.count(chr(i)) / len(data)) if data.count(chr(i)) > 0 else 0) for i in range(256)])

    def is_suspicious_section(self, section):
        """Check if section is suspicious (high entropy, no readable strings, etc.)"""
        entropy = self.calculate_entropy(section.get_data())
        if entropy > 7.5:  # Common threshold for packed sections
            return True
        return False

    def check_strings_in_binary(self, file_path):
        try:
            suspicious_strings = [
                "http", "ftp", "https", "cmd.exe", "powershell", "regsvr32", "mshta"
            ]
            with open(file_path, "rb") as f:
                content = f.read()
                for string in suspicious_strings:
                    if string.encode() in content:
                        self.result_area.append(f"[⚠] Suspicious string detected: {string}")
                self.result_area.append(f"[✓] Strings check complete.")
        except Exception as e:
            self.result_area.append(f"[Error] String check failed: {str(e)}")

    def deobfuscate_file(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            deobfuscated = None
            try:
                # Check if content is Base64 encoded
                deobfuscated = base64.b64decode(content)
                self.result_area.append(f"Deobfuscated Content (Base64 decoded):\n{deobfuscated.decode('utf-8', 'ignore')}")
            except Exception:
                self.result_area.append("[Error] Deobfuscation failed. Content might not be base64 encoded.")
            
            # Example heuristic: Try to decode zlib-compressed strings (common in obfuscation)
            try:
                decompressed = zlib.decompress(content.encode())
                self.result_area.append(f"Decompressed Content (zlib):\n{decompressed.decode('utf-8', 'ignore')}")
            except Exception:
                self.result_area.append("[Error] Decompression failed. Content might not be zlib compressed.")
            
            self.progress_bar.setValue(100)
        except Exception as e:
            self.result_area.append(f"[Error] {str(e)}")
            self.progress_bar.setValue(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ReverseEngineeringTool()
    window.show()
    sys.exit(app.exec())
