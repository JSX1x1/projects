import os
import sys
import hashlib
import stat
import time
import magic
import argparse
from pathlib import Path
from tqdm import tqdm


class FileIntegrityChecker:
    def __init__(self, path, is_directory, output_file=None):
        self.path = Path(path)
        self.is_directory = is_directory
        self.output_file = output_file
        self.results = []

    def run(self):
        """Runs the integrity checks."""
        files = list(self.path.rglob("*")) if self.is_directory else [self.path]
        total_files = len(files)

        if total_files == 0:
            print("No valid files found.")
            return

        for file in tqdm(files, desc="Processing Files", unit="file"):
            if file.is_file():
                self.results.append(self.analyze_file(file))

        self.display_results()
        if self.output_file:
            self.save_results()

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

            return file_info + "-" * 60 + "\n"

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

    def display_results(self):
        """Displays the results on the console."""
        print("\n=== Integrity Check Results ===")
        for result in self.results:
            print(result)

    def save_results(self):
        """Saves results to a specified file."""
        try:
            with open(self.output_file, "w") as f:
                f.writelines(self.results)
            print(f"\nResults saved to: {self.output_file}")
        except Exception as e:
            print(f"Error saving results: {e}")


def parse_arguments():
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(description="File Integrity Checker")
    parser.add_argument("path", help="Path to the file or directory")
    parser.add_argument("-d", "--directory", action="store_true", help="Indicates if the path is a directory")
    parser.add_argument("-o", "--output", help="Save results to a file (e.g., results.txt)")

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()

    if not os.path.exists(args.path):
        print(f"Error: Path '{args.path}' does not exist.")
        sys.exit(1)

    checker = FileIntegrityChecker(args.path, args.directory, args.output)
    checker.run()
