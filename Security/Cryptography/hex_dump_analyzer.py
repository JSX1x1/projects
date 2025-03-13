import sys
import binascii
import os
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QFileDialog, QLabel
from PyQt6.QtCore import Qt
from datetime import datetime


class HexDumpAnalyzerApp(QWidget):
    def __init__(self):
        super().__init__()
        
        # Set up the window
        self.setWindowTitle('Hex Dump Analyzer')
        self.setGeometry(100, 100, 900, 700)
        
        # Create layout
        self.layout = QVBoxLayout()

        # Create UI elements
        self.label = QLabel("Upload a file to analyze its Hex Dump:")
        self.layout.addWidget(self.label)
        
        self.upload_button = QPushButton("Upload File")
        self.layout.addWidget(self.upload_button)

        self.hex_output = QTextEdit()
        self.hex_output.setReadOnly(True)
        self.layout.addWidget(self.hex_output)

        self.ethical_guidelines = QTextEdit()
        self.ethical_guidelines.setReadOnly(True)
        self.layout.addWidget(self.ethical_guidelines)

        # Connect the upload button to the upload function
        self.upload_button.clicked.connect(self.upload_file)

        # Set the layout to the window
        self.setLayout(self.layout)

        # Display ethical guidelines
        ethical_guidelines = self.provide_ethical_guidelines()
        self.ethical_guidelines.setText(ethical_guidelines) 

    def upload_file(self):
        # Open file dialog to select a file
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File")
        
        if file_path:
            self.display_hex_dump(file_path)
            
    def display_hex_dump(self, file_path):
        try:
            # Open and read the file
            with open(file_path, 'rb') as file:
                file_content = file.read()

            # Get the hex dump of the file
            hex_dump = binascii.hexlify(file_content).decode('utf-8')

            # Format the hex dump for display (group by 16 bytes per line)
            hex_display = self.format_hex_dump(hex_dump)

            # Display the hex dump
            self.hex_output.setText(hex_display)

            # Perform analysis of the hex dump
            analysis = self.analyze_hex_dump(file_content)
            self.hex_output.append("\n" + analysis)

        except Exception as e:
            self.hex_output.setText(f"Error reading file: {str(e)}")

    def format_hex_dump(self, hex_string):
        # Format the hex string into a human-readable hex dump (16 bytes per line)
        hex_lines = []
        byte_groups = []
        for i in range(0, len(hex_string), 32):  # 32 hex chars = 16 bytes
            hex_chunk = hex_string[i:i + 32]
            offset = f"{i // 2:08X}"
            hex_representation = ' '.join([hex_chunk[j:j + 2] for j in range(0, len(hex_chunk), 2)])

            # Enhance ASCII representation: if printable, show it; if not, show '.'
            ascii_representation = ''.join([chr(int(hex_chunk[j:j + 2], 16)) if 32 <= int(hex_chunk[j:j + 2], 16) <= 126 else '.' for j in range(0, len(hex_chunk), 2)])
            
            # Group bytes for better readability
            byte_groups.append(f"{offset}  {hex_representation:<48}  |{ascii_representation}|")
        
        # Add a byte group legend
        byte_groups.insert(0, "Offset    Hex Dump (16 bytes per line)                       ASCII Representation")
        
        return '\n'.join(byte_groups)

    def analyze_hex_dump(self, file_content):
        # Initialize the analysis list
        analysis = []

        # File signatures dictionary
        file_signatures = {
            # Image formats
            'PDF': b'%PDF',
            'PNG': b'\x89PNG\r\n\x1a\n',
            'JPEG': b'\xFF\xD8\xFF',
            'JPEG (SOI)': b'\xFF\xD8\xFF\xE0',
            'GIF': b'GIF89a',
            'BMP': b'42 4D',  # BMP files start with "BM"
            'TIFF (Little Endian)': b'49 49 2A 00',  # Little Endian TIFF
            'TIFF (Big Endian)': b'4D 4D 00 2A',  # Big Endian TIFF
            'WEBP': b'52 49 46 46',  # WebP files start with "RIFF"
            
            # Audio formats
            'MP3': b'49 44 33',  # MP3 files start with "ID3"
            'WAV': b'52 49 46 46',  # WAV files start with "RIFF"
            'FLAC': b'fLAC',  # FLAC files start with "fLaC"
            'OGG': b'4F 67 67 53',  # OGG files start with "OggS"
            
            # Video formats
            'MP4': b'00 00 00 18 66 74 79 70',  # MP4 files start with "ftyp"
            'AVI': b'52 49 46 46',  # AVI files start with "RIFF"
            'MKV': b'1A 45 DF A3',  # MKV files start with the Matroska header
            'MOV': b'00 00 00 18 66 74 79 70',  # MOV files start with "ftyp"

            # Archive formats
            'ZIP': b'50 4B 03 04',  # ZIP files start with "PK\x03\x04"
            'RAR': b'52 61 72 21 1A 07 00',  # RAR files start with "Rar!"
            '7z': b'37 7A BC AF 27 1C',  # 7z files start with "7z"
            
            # Executable formats
            'EXE': b'MZ',  # Windows executable files start with "MZ"
            'ELF': b'\x7F\x45\x4C\x46',  # ELF files start with the magic bytes "\x7F\x45\x4C\x46"
            'Mach-O': b'\xCF\xFA\xED\xFE',  # Mach-O files (macOS) start with the magic bytes "\xCF\xFA\xED\xFE"

            # Document formats
            'DOCX': b'50 4B 03 04',  # DOCX files are essentially ZIP files starting with "PK\x03\x04"
            'XLSX': b'50 4B 03 04',  # XLSX files are also ZIP files starting with "PK\x03\x04"
            'PPTX': b'50 4B 03 04',  # PPTX files are also ZIP files starting with "PK\x03\x04"
            'ODT': b'50 4B 03 04',  # ODT files are ZIP files starting with "PK\x03\x04"
            'PDF': b'%PDF',  # PDF files start with "%PDF"

            # System files
            'ISO': b'43 44 30 30 31',  # ISO files start with "CD001"
            'DMG': b'78 01 73 0D 62 62 60 62',  # DMG (macOS disk image) starts with a specific sequence
            'Apple Disk Image': b'58 42 43 48 44 44',  # Disk image format for Apple

            # Text files (common text formats)
            'TXT': b'EF BB BF',  # UTF-8 with BOM (Byte Order Mark) for text files
            'CSV': b'EF BB BF',  # CSV files often use UTF-8 with BOM
            'LOG': b'EF BB BF',  # Log files, if saved with UTF-8 BOM
            'XML': b'3C 3F 78 6D 6C',  # XML files often start with "<?xml"
            'HTML': b'3C 21 44 4F 43 54',  # HTML files start with "<!DOCTYPE"
            'JSON': b'{',  # JSON files often start with '{'
            'YAML': b'%YAML',  # YAML files often start with "%YAML"
            'Markdown': b'#',  # Markdown files typically start with '#' for headers
            'RTF': b'{\\rtf',  # RTF files often start with "{\\rtf"
            'INI': b';',  # INI files often begin with a semicolon
            'UTF-16': b'\xFF\xFE',  # UTF-16 encoded text files with BOM
            'UTF-32': b'\xFF\xFE\x00\x00',  # UTF-32 encoded text files with BOM
            
            # Others (miscellaneous)
            'SQLite': b'SQLite format 3\0',  # SQLite database files start with this string
            'Font': b'\x00\x01\x00\x00',  # TrueType font files start with this header
            'WOFF': b'\x77\x4F\x46\x46',  # WOFF (Web Open Font Format) files start with "wOFF"
            'EPS': b'25 50 44 46 2D',  # Encapsulated PostScript files start with "%!PS"
        }

        detected_types = []
        for file_type, signature in file_signatures.items():
            if file_content.startswith(signature):
                detected_types.append(file_type)

        if detected_types:
            analysis.append(f"Detected File Types: {', '.join(detected_types)}")
        else:
            analysis.append("No known file signature detected.")

        # Ethical Guidelines: Analyze how the user should interpret sensitive data
        ethical_notes = self.provide_ethical_guidelines()

        return '\n'.join(analysis) + "\n\n" + ethical_notes

    def provide_ethical_guidelines(self):
        ethical_guidelines = (
            "Ethical Guidelines for Hex Dump Analysis:\n"
            "--------------------------------------------------------\n"
            "1. **Sensitive Data**: Hex dumps can contain sensitive or private information. Never analyze or distribute hex dumps of files that contain personal data, passwords, or confidential information without consent.\n"
            "2. **Legal Compliance**: Always ensure that the file being analyzed was obtained legally. Analyzing pirated or stolen files is unethical and potentially illegal.\n"
            "3. **Avoid Malicious Files**: Be aware that hex dumps can represent malware or harmful content. If you're analyzing a file that might be suspicious, use a secure environment (e.g., a sandbox).\n"
            "4. **Respect Privacy**: If you find personal or private information in the hex dump, ensure that it is not misused or shared. Protect the privacy and integrity of individuals.\n"
            "5. **Ethical Usage**: Use this tool for ethical purposes only, such as educational purposes, security analysis, and learning. Misusing this tool to extract sensitive information from files without permission is unethical.\n"
            "--------------------------------------------------------\n"
            "This tool is designed to help understand file structures and data encoding patterns but should not be used to violate privacy or extract unauthorized data.\n"
        )
        return ethical_guidelines


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HexDumpAnalyzerApp()
    window.show()
    sys.exit(app.exec())
