import sys
import os
import re
import base64
import zlib
import hashlib
import math
import pefile
from capstone import *
from argparse import ArgumentParser

class ReverseEngineeringTool:
    def __init__(self):
        self.selected_file = None

    def select_file(self, file_path):
        self.selected_file = file_path

    def start_analysis(self, analysis_type):
        if not self.selected_file:
            print("[!] No file selected!")
            return

        print(f"[Scanning] Analyzing {self.selected_file}...")
        
        if analysis_type == "disassemble":
            self.disassemble_binary(self.selected_file)
        elif analysis_type == "analyze":
            self.analyze_binary(self.selected_file)
        elif analysis_type == "deobfuscate":
            self.deobfuscate_file(self.selected_file)
        else:
            print("[!] Invalid analysis type specified.")

    def disassemble_binary(self, file_path):
        try:
            with open(file_path, "rb") as f:
                code = f.read()

            md = Cs(CS_ARCH_X86, CS_MODE_64)
            disassembly = ""
            for i in md.disasm(code, 0x1000):
                disassembly += f"{i.address}: {i.mnemonic} {i.op_str}\n"
            
            print(disassembly)
        except Exception as e:
            print(f"[Error] {str(e)}")

    def analyze_binary(self, file_path):
        try:
            # PE file analysis (for Windows binaries)
            if file_path.lower().endswith(".exe"):
                self.analyze_pe(file_path)
            else:
                print("[⚠] Unsupported binary format!")
        except Exception as e:
            print(f"[Error] {str(e)}")

    def analyze_pe(self, file_path):
        try:
            pe = pefile.PE(file_path)

            # Get sections information
            sections = pe.sections
            print(f"Sections: {len(sections)}\n")
            for section in sections:
                print(f"Section: {section.Name.decode('utf-8').strip()}")
                print(f"Virtual Size: {section.Misc_VirtualSize}")
                print(f"Raw Data Size: {section.SizeOfRawData}")
                print(f"Entropy: {self.calculate_entropy(section.get_data())}")

            # Detecting suspicious patterns like executable sections with high entropy (packed binaries)
            for section in sections:
                if self.is_suspicious_section(section):
                    print(f"[⚠] Suspicious Section: {section.Name.decode('utf-8').strip()}")

            self.check_strings_in_binary(file_path)

        except Exception as e:
            print(f"[Error] PE Analysis failed: {str(e)}")

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
                        print(f"[⚠] Suspicious string detected: {string}")
                print(f"[✓] Strings check complete.")
        except Exception as e:
            print(f"[Error] String check failed: {str(e)}")

    def deobfuscate_file(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            deobfuscated = None
            try:
                # Check if content is Base64 encoded
                deobfuscated = base64.b64decode(content)
                print(f"Deobfuscated Content (Base64 decoded):\n{deobfuscated.decode('utf-8', 'ignore')}")
            except Exception:
                print("[Error] Deobfuscation failed. Content might not be base64 encoded.")
            
            # Example heuristic: Try to decode zlib-compressed strings (common in obfuscation)
            try:
                decompressed = zlib.decompress(content.encode())
                print(f"Decompressed Content (zlib):\n{decompressed.decode('utf-8', 'ignore')}")
            except Exception:
                print("[Error] Decompression failed. Content might not be zlib compressed.")
        except Exception as e:
            print(f"[Error] {str(e)}")

def main():
    parser = ArgumentParser(description="Reverse Engineering Tool - CLI Version")
    parser.add_argument("file", help="Path to the binary or script file")
    parser.add_argument("analysis", choices=["disassemble", "analyze", "deobfuscate"], help="Type of analysis to perform")

    args = parser.parse_args()

    tool = ReverseEngineeringTool()
    tool.select_file(args.file)
    tool.start_analysis(args.analysis)

if __name__ == "__main__":
    main()
