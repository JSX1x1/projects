# Terminal Tools: GUI & CLI Versions

Welcome to **Terminal Tools**, a collection of terminal-based utilities that provide a command-line interface (CLI) as well as a graphical user interface (GUI). These tools allow users to perform common file system operations such as creating directories, removing directories, creating files, navigating the file system, and more.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Setup](#setup)
  - [GUI Version (`program_GUI.py`)](#gui-version-programguipy)
  - [CLI Version (`console_CLI.cs`)](#cli-version-consoleclics)
- [How to Use](#how-to-use)
  - [GUI Version](#gui-version)
  - [CLI Version](#cli-version)
- [Commands Supported](#commands-supported)
- [Additional Information](#additional-information)
- [License](#license)

---

## Overview

**Terminal Tools** consists of two versions:

1. **GUI Version (`program_GUI.py`)**: A Python-based graphical terminal with a GUI built using PyQt6. It provides a windowed interface where users can interact with the terminal, execute commands, and view results in real-time.
2. **CLI Version (`console_CLI.cs`)**: A C#-based command-line terminal that runs directly in the terminal/console. This version mimics a terminal-like experience within a text-based interface.

Both versions provide similar functionality but differ in their interface and interaction style.

---

## Features

- **Cross-Platform Support**: Both versions are designed to work on multiple platforms.
  - **GUI Version**: Works on Windows, macOS, and Linux.
  - **CLI Version**: Primarily for Windows (C#). For Linux/macOS, you may need some adjustments.
  
- **Basic File System Operations**: Both versions provide the ability to:
  - **Create and remove directories** (`mkdir`, `rmdir`)
  - **Create files** (`touch`)
  - **Edit files** (`edit`)
  - **Navigate the file system** (`cd`)
  - **List directory contents** (`ls`)
  - **Display directory tree structure** (`tree`)
  
- **Command History and Error Handling**: Both versions include basic error handling for invalid commands and provide useful feedback.

---

## Setup

### GUI Version (`program_GUI.py`)

#### Prerequisites:
- **Python 3.x** installed on your system. You can download it from [here](https://www.python.org/downloads/).
- **PyQt6** installed. You can install it via pip:
  ```bash
  pip install PyQt6
  ```

#### Setup Steps:
1. **Clone the repository** or download the `program_GUI.py` file.
   - If cloning via Git:
     ```bash
     git clone <repository_url>
     cd <repository_directory>
     ```

2. **Install required Python packages**:
   - Open a terminal/command prompt and run:
     ```bash
     pip install -r requirements.txt
     ```
     This will install all necessary Python libraries, including PyQt6.

3. **Run the program**:
   - After installing dependencies, navigate to the directory containing `program_GUI.py` and execute the script:
     ```bash
     python program_GUI.py
     ```

---

### CLI Version (`console_CLI.cs`)

#### Prerequisites:
- **Visual Studio** or **.NET SDK** installed. You can download Visual Studio (Community edition) from [here](https://visualstudio.microsoft.com/downloads/) or install the **.NET SDK** from [here](https://dotnet.microsoft.com/download).

#### Setup Steps:
1. **Clone the repository** or download the `console_CLI.cs` file.
   - If cloning via Git:
     ```bash
     git clone <repository_url>
     cd <repository_directory>
     ```

2. **Open the project**:
   - Open **Visual Studio** or a compatible IDE and open the `console_CLI.cs` file.

3. **Build and Run**:
   - Press **F5** or **Ctrl + F5** to build and run the program. Alternatively, you can run the following command in the terminal:
     ```bash
     dotnet run
     ```

---

## How to Use

### GUI Version

1. **Launch the application** by running `program_GUI.py`.
2. **Interact with the terminal**:
   - Type your desired command in the input field at the bottom of the window.
   - Press **Enter** to execute the command.
   - Results and any errors will appear in the output area above.
3. **Commands**:
   - Use the following commands in the terminal (see "Commands Supported" section for detailed descriptions).

### CLI Version

1. **Launch the application** by running the compiled `console_CLI.cs` executable in your terminal/command prompt.
2. **Interact with the terminal**:
   - Type your desired command and press **Enter** to execute it.
   - Results will be displayed directly in the console window.
3. **Commands**:
   - Use the following commands in the terminal (see "Commands Supported" section for detailed descriptions).

---

## Commands Supported

Both the **GUI Version** and **CLI Version** support the following commands:

1. **`mkdir <directory>`**:
   - Creates a new directory.
   - Example: `mkdir new_folder`
   
2. **`rmdir <directory>`**:
   - Removes an existing directory.
   - Example: `rmdir old_folder`
   
3. **`touch <filename>`**:
   - Creates a new empty file with the specified filename.
   - Example: `touch example.txt`
   
4. **`edit <filename>`**:
   - Opens the specified file in the default editor (Notepad for Windows).
   - Example: `edit example.txt`
   
5. **`cd <path>`**:
   - Changes the current working directory.
   - Example: `cd /path/to/directory`
   
6. **`ls`**:
   - Lists the contents of the current directory.
   
7. **`tree`**:
   - Displays a directory tree of the current directory.
   
8. **`help`**:
   - Displays a help message showing available commands.

---

## Additional Information

### Error Handling

- **Invalid Command**: If an unsupported or invalid command is entered, both the GUI and CLI versions will display an error message indicating the issue.
- **Invalid Directory/File**: If the user tries to perform an operation on a non-existent directory or file, an error message will be shown explaining the issue.

### Platform Compatibility

- The **GUI Version** is cross-platform and should work on Windows, macOS, and Linux with minimal configuration.
- The **CLI Version** is designed for **Windows**. To run it on Linux or macOS, you may need to adjust file paths or adapt the `edit` functionality (e.g., use `nano` or `vim` for Linux/macOS instead of Notepad).

### Default Text Editor for `edit`

- In the **CLI Version**, `edit` opens the file using **Notepad** (on Windows). On **Linux/macOS**, you may want to replace `notepad.exe` with a system-specific text editor like `nano` or `vim`.