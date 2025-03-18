import os
import sys
import hashlib
import chardet
import zipfile
import subprocess
import json
from PyPDF2 import PdfReader
from PIL import Image
import argparse
from termcolor import colored

SUPPORTED_SOURCE_FILES = [".py", ".cpp", ".java", ".js", ".html", ".css", ".php", ".sh"]

def log(message, severity="info"):
    """Log messages with color coding for CLI output."""
    colors = {"info": "green", "warning": "yellow", "error": "red"}
    print(colored(message, colors.get(severity, "white")))

def get_all_files(folder_path):
    """Recursively fetch all files in a folder."""
    file_list = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_list.append(os.path.join(root, file))
    return file_list

def check_file(file_path):
    """Check file corruption based on type."""
    ext = os.path.splitext(file_path)[-1].lower()
    try:
        if ext in SUPPORTED_SOURCE_FILES:
            return check_source_code_file(file_path)
        elif ext in [".txt", ".csv", ".json", ".xml"]:
            return check_text_file(file_path)
        else:
            log(f"Skipping unsupported file type: {ext}", "warning")
            return False
    except Exception as e:
        log(f"Error checking {file_path}: {str(e)}", "error")
        return True

def check_source_code_file(file_path):
    """Check for syntax errors in source code files."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()

        if not code.strip():
            log(f"Empty source code file: {file_path}", "warning")
            return True

        # Syntax check for Python files
        if file_path.endswith(".py"):
            result = subprocess.run(["python", "-m", "py_compile", file_path],
                                    capture_output=True, text=True)
            if result.returncode != 0:
                log(f"Syntax error in Python file: {file_path}", "error")
                attempt_recovery(file_path)
                return True

        # Syntax check for Java files
        if file_path.endswith(".java"):
            result = subprocess.run(["javac", file_path],
                                    capture_output=True, text=True)
            if result.returncode != 0:
                log(f"Syntax error in Java file: {file_path}", "error")
                attempt_recovery(file_path)
                return True

        # Syntax check for C++ files
        if file_path.endswith(".cpp"):
            result = subprocess.run(["g++", "-fsyntax-only", file_path],
                                    capture_output=True, text=True)
            if result.returncode != 0:
                log(f"Syntax error in C++ file: {file_path}", "error")
                attempt_recovery(file_path)
                return True

        return False
    except Exception:
        log(f"Corrupt source code file: {file_path}", "error")
        attempt_recovery(file_path)
        return True

def check_text_file(file_path):
    """Check for encoding issues in text files."""
    try:
        with open(file_path, "rb") as f:
            raw_data = f.read()
            result = chardet.detect(raw_data)
            encoding = result["encoding"]
            if encoding is None:
                log(f"Unknown Encoding (Possible corruption): {file_path}", "warning")
                attempt_recovery(file_path)
                return True
        return False
    except Exception:
        log(f"Corrupt text file: {file_path}", "error")
        attempt_recovery(file_path)
        return True

def attempt_recovery(file_path):
    """Try to recover corrupted files by creating a backup and cleaning up."""
    try:
        backup_path = file_path + ".bak"
        if not os.path.exists(backup_path):
            os.rename(file_path, backup_path)
            log(f"Backup created: {backup_path}", "info")

        # If it's a text file, try to recover usable lines
        if file_path.endswith((".txt", ".csv", ".json", ".xml", ".py", ".cpp", ".java")):
            with open(backup_path, "r", encoding="utf-8", errors="ignore") as old_f:
                lines = old_f.readlines()

            with open(file_path, "w", encoding="utf-8") as new_f:
                for line in lines:
                    if "\x00" not in line:  # Ignore null-byte corruption
                        new_f.write(line)

            log(f"Recovered file: {file_path}", "success")
            return True

        return False
    except Exception as e:
        log(f"Auto-recovery failed for {file_path}: {str(e)}", "error")
        return False

def check_files(files):
    """Check a list of files for corruption."""
    total_files = len(files)
    if total_files == 0:
        log("No files found.", "warning")
        return

    corrupted_files = 0

    for index, file in enumerate(files):
        log(f"Checking: {file}")
        if not os.path.isfile(file):
            log(f"Skipping (Not a file): {file}", "warning")
            continue

        corruption_status = check_file(file)
        if corruption_status:
            corrupted_files += 1

        progress = int((index + 1) / total_files * 100)
        log(f"Progress: {progress}% completed", "info")

    corruption_ratio = (corrupted_files / total_files) * 100
    log(f"Total Files Scanned: {total_files}", "info")
    log(f"Corruption Ratio: {corruption_ratio:.2f}%", "warning" if corruption_ratio > 0 else "info")

def main():
    """Main function to handle CLI arguments."""
    parser = argparse.ArgumentParser(description="CLI-Based File Corruption Checker")
    parser.add_argument("-f", "--file", help="Check a single file for corruption")
    parser.add_argument("-d", "--directory", help="Check all files in a folder for corruption")
    args = parser.parse_args()

    if args.file:
        if os.path.exists(args.file):
            check_files([args.file])
        else:
            log(f"File not found: {args.file}", "error")

    elif args.directory:
        if os.path.exists(args.directory):
            files = get_all_files(args.directory)
            check_files(files)
        else:
            log(f"Directory not found: {args.directory}", "error")

    else:
        log("Usage: python corruption_checker.py -f <file> OR -d <directory>", "warning")

if __name__ == "__main__":
    main()
