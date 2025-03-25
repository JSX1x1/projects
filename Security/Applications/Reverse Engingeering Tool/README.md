# Reverse Engineering Tool

## Overview

The Reverse Engineering Tool is designed for professionals in cybersecurity, malware analysis, and reverse engineering. This tool allows you to analyze binary files, disassemble code, analyze PE files (for Windows executables), and deobfuscate potentially malicious files. The tool is available in both a GUI version (`rev_engin_GUI`) and a CLI version (`rev_engin_CLI`).

### Features:
- **Disassemble Binary**: Disassembles binary files into human-readable assembly code.
- **Analyze PE Files**: Performs analysis of PE (Portable Executable) files, extracts section information, and detects suspicious patterns.
- **Deobfuscate Malware**: Attempts to deobfuscate files, including Base64 decoding and zlib decompression.
- **PE File Section Analysis**: Detects suspicious sections in PE files, including packed code using entropy analysis.
- **String Checking**: Searches for common suspicious strings (e.g., URLs, cmd.exe) in binaries.

## Table of Contents
- [Getting Started](#getting-started)
- [Installation](#installation)
  - [GUI Version](#gui-version)
  - [CLI Version](#cli-version)
- [Usage](#usage)
  - [GUI Version](#usage-gui-version)
  - [CLI Version](#usage-cli-version)
- [Features and Analysis Types](#features-and-analysis-types)
- [Disclaimer](#Legal-Disclaimer)

## Getting Started

These instructions will help you get the tool up and running on your machine.

### Prerequisites

- Python 3.6 or higher
- Required dependencies (see below for installation instructions)

## Installation

### GUI Version (`rev_engin_GUI`)

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/rev_engin_GUI.git
   cd rev_engin_GUI
   ```

2. Install the necessary dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the tool:
   ```bash
   python main_gui.py
   ```

   This will launch the graphical user interface (GUI) for the reverse engineering tool.

### CLI Version (`rev_engin_CLI`)

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/rev_engin_CLI.git
   cd rev_engin_CLI
   ```

2. Install the necessary dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the tool:
   ```bash
   python main_cli.py
   ```

   This will launch the command-line interface (CLI) version of the reverse engineering tool.

## Usage

### GUI Version

1. **Select a File**: Click on the "Select File" button to choose a binary or script file for analysis.
2. **Choose Analysis Type**: Choose from the following analysis types:
   - **Disassemble Binary**: Disassembles a binary file into assembly code.
   - **Analyze Binary**: Analyzes a binary, including PE file structure and sections.
   - **Deobfuscate Malware**: Attempts to deobfuscate potentially obfuscated or packed malware.
3. **Start Analysis**: Click on the "Start Analysis" button to begin the selected analysis. The progress and results will be displayed in the result area.
4. **View Results**: Once the analysis is complete, results will be shown in the result area, including disassembly, PE analysis, suspicious string detection, etc.

### CLI Version

1. **Select a File**: Use the `-f` flag to specify the path to the file you want to analyze:
   ```bash
   python main_cli.py -f path/to/file
   ```

2. **Choose Analysis Type**: Use the `-a` flag to specify the type of analysis:
   - `disassemble`: Disassemble the binary file into assembly code.
   - `analyze`: Analyze the binary file (PE file analysis).
   - `deobfuscate`: Attempt to deobfuscate the file.

   Example usage:
   ```bash
   python main_cli.py -f path/to/file -a disassemble
   python main_cli.py -f path/to/file -a analyze
   python main_cli.py -f path/to/file -a deobfuscate
   ```

3. **View Results**: After the analysis completes, results will be displayed in the terminal, showing disassembly, analysis, or deobfuscation results.

## Features and Analysis Types

### 1. Disassemble Binary
Disassembles a binary file and presents it in a human-readable assembly format. This feature uses `capstone` for disassembly.

### 2. Analyze Binary (PE Files)
For Windows executables (.exe), this feature extracts and analyzes the PE (Portable Executable) file structure. It provides information about the sections, including:
- Section Name
- Virtual Size
- Raw Data Size
- Entropy (useful for detecting packed or encrypted code)

Additionally, it searches for common suspicious strings, such as URLs or system commands like `cmd.exe` and `powershell`.

### 3. Deobfuscate Malware
This feature attempts to deobfuscate files by:
- **Base64 Decoding**: Checks if the file content is Base64-encoded and decodes it.
- **Zlib Decompression**: Attempts to decompress any zlib-compressed data, which is commonly used in obfuscation.

### 4. PE File Section Analysis
- **Entropy Analysis**: Identifies sections with high entropy (which may indicate packed or encrypted code).
- **String Checking**: Detects suspicious strings, such as network protocols, executable commands, or other indicators of malicious behavior.

---

### Notes:

1. **Dependencies**:
   - `pyqt6` for GUI creation.
   - `capstone` for disassembling binary files.
   - `pefile` for analyzing PE files.
   - `hashlib`, `zlib`, `math` for auxiliary tasks like hashing, compression, and entropy calculation.
   - Make sure to install all dependencies from the `requirements.txt` file to ensure smooth functionality.

2. **Compatibility**:
   - The GUI version uses `PyQt6` and is suitable for platforms that support Qt applications.
   - The CLI version can be used on any platform with a terminal and Python 3.6+.

3. **Contributions**:
   Contributions are welcome! Please fork this repository and submit a pull request with your improvements or fixes.

---

## Legal Disclaimer

### Usage and Responsibility

By using this tool, you agree to the following terms and conditions. The Reverse Engineering Tool is intended solely for educational, research, and legitimate cybersecurity purposes. It is **not** intended for illegal or unauthorized activities, including but not limited to:

- **Malicious Hacking**: Any attempt to reverse engineer software for malicious purposes is strictly prohibited.
- **Unauthorized Access**: The tool should not be used to access or analyze software or systems that you do not have explicit permission to analyze.
- **Copyright Infringement**: The tool is not intended for bypassing licensing protections or reverse engineering proprietary software without consent.

### Legal Use Cases

This tool is designed to aid security researchers, malware analysts, and developers in legitimate activities, such as:

- **Analyzing Malware**: The tool can be used for the analysis and study of malware to understand its behavior and improve security practices.
- **Security Audits**: The tool can be used to perform security audits on software that you own or have explicit permission to analyze.
- **Educational Purposes**: The tool may be used in training, coursework, or research related to reverse engineering and cybersecurity.

### No Warranty

This tool is provided "as-is" without any warranty of any kind, either express or implied, including but not limited to the warranties of merchantability or fitness for a particular purpose. The authors are not responsible for any damage, loss of data, or other adverse consequences resulting from the use or misuse of this tool.

### Compliance with Laws

It is the user's responsibility to comply with all applicable laws and regulations in their jurisdiction regarding reverse engineering, software analysis, and intellectual property. Users are encouraged to obtain permission before performing any reverse engineering on proprietary or third-party software.

### Liability

Under no circumstances will the authors or contributors be held liable for any direct, indirect, incidental, special, exemplary, or consequential damages (including, but not limited to, procurement of substitute goods or services; loss of use, data, or profits; or business interruption) arising in any way out of the use of this tool, even if advised of the possibility of such damage.