# **Simple File Creation Tool**

This project contains two terminal tools with different interfaces for file and directory operations:
1. **`program_GUI.py`** - A **Graphical User Interface (GUI)** Python application built with **PyQt6**.
2. **`console_CLI.cs`** - A **Command Line Interface (CLI)** C# application designed for console-based file management.

Both programs allow the user to interact with the filesystem and manage files and directories with several built-in features.

---

## **1. `program_GUI.py` (PyQt6 GUI Tool)**

### **Description**
`program_GUI.py` is a **GUI tool** built with **PyQt6** that allows users to interactively create files with custom extensions, sizes, and content. It features **Light/Dark Mode** toggling and additional safety measures like file size limitations to prevent storage bombing.

### **Features**
- **File Creation**: Create files with custom extensions, file sizes, or specific content.
- **File Size Control**: Set a maximum file size limit to avoid unintentional storage issues.
- **Dark and Light Mode**: Toggle between dark and light modes.
- **Custom File Extensions**: Choose or create a custom extension for the file.
- **Safety Measures**: Size limits to prevent unintentional large file creation.

### **Dependencies**
- Python 3.x
- PyQt6 (Install using `pip install PyQt6`)

### **Installation**
1. **Install Python** (if not already installed):  
   Download and install Python 3.x from [https://www.python.org/downloads/](https://www.python.org/downloads/).

2. **Install PyQt6**:  
   Run the following command in your terminal/command prompt to install PyQt6:
   ```bash
   pip install PyQt6
   ```

3. **Download the Project**:  
   Clone this repository or download the `program_GUI.py` file.

4. **Run the Application**:
   To run the PyQt6 GUI tool, execute the following command in your terminal:
   ```bash
   python program_GUI.py
   ```

### **How to Use**
1. **Choose File Name**: Enter a name for the file (without extension).
2. **Choose Extension**: Either select a predefined extension or enter a custom one.
3. **Set File Size**: Specify a file size or leave it empty to create a custom content file.
4. **Toggle Mode**: Use the "Dark Mode" button to toggle between Light and Dark modes.
5. **Create File**: Click the "Create File" button to create the file with the specified properties.
6. **Safety Alert**: If the file size exceeds the specified safety limit, an alert will warn you.

### **Features in Detail**
1. **File Creation**:  
   - After entering the name and extension, the program creates the file either with custom content or a specified size. 
   - You can set custom content if you choose not to use the dummy file size.
  
2. **Safety Measures**:  
   - If the file exceeds a pre-set maximum size limit (e.g., 1 GB), the program will show a warning message and prevent file creation.

3. **Dark/Light Mode Toggle**:  
   - The application has a light mode by default. You can toggle it to dark mode for a more visually comfortable interface.

4. **Custom Extensions**:  
   - The program supports custom file extensions in addition to predefined options.

---

## **2. `console_CLI.cs` (C# Console CLI Tool)**

### **Description**
`console_CLI.cs` is a **Command Line Interface (CLI)** tool written in **C#**. It offers advanced file and directory operations, including creating files, directories, deleting files, listing files, and previewing file contents. It operates in a **Dark Mode-only** theme.

### **Features**
- **Create File**: Create a file with user-provided content.
- **Delete File**: Delete a specified file.
- **Create Directory**: Create a new directory.
- **List Files**: List all files in the current directory.
- **Show File Content**: View the content of a specified file.
- **Help Command**: Displays available commands and instructions.
- **Exit**: Cleanly exits the program.

### **Dependencies**
- .NET SDK (Install from [https://dotnet.microsoft.com/download](https://dotnet.microsoft.com/download)).

### **Installation**
1. **Install .NET SDK**:  
   If you don’t have the .NET SDK installed, download and install it from [here](https://dotnet.microsoft.com/download).

2. **Download the Project**:  
   Clone this repository or download the `console_CLI.cs` file.

3. **Build the Project**:
   Open your terminal/command prompt and run:
   ```bash
   dotnet new console -n ConsoleCLI
   ```
   Replace the content of `Program.cs` with the `console_CLI.cs` file.

4. **Run the Application**:
   To run the C# console tool, navigate to the project folder and use:
   ```bash
   dotnet run
   ```

### **How to Use**
1. **Create a File**:  
   Type `create file filename.txt` and provide the content for the file. If content is omitted, a basic file is created.

2. **Delete a File**:  
   Type `delete file filename.txt` to delete the specified file.

3. **Create a Directory**:  
   Type `create dir mydirectory` to create a directory.

4. **List Files**:  
   Type `list files` to list all files in the current directory.

5. **Show File Content**:  
   Type `show file filename.txt` to view the content of the specified file.

6. **Exit**:  
   Type `exit` to quit the program.

7. **Help**:  
   Type `help` to display a list of available commands and descriptions.

### **Features in Detail**
1. **File Operations**:  
   - **Create File**:  
     Prompts for content and creates a file with the specified name. If content is not specified, a simple empty file is created.
   - **Delete File**:  
     Removes the file with the provided filename.
  
2. **Directory Operations**:  
   - **Create Directory**:  
     Creates a new directory with the specified name.
   - **List Files**:  
     Lists all files in the current working directory.
  
3. **Show File Content**:  
   - Allows users to view the content of a file without opening it externally.

4. **Dark Mode-only**:  
   - The entire application operates in dark mode with black backgrounds and white text for a visually comfortable experience.

5. **Help and Instructions**:  
   - Use the `help` command to display available actions and their syntax.

---

## **Safety and Ethical Compliance**

### **File Size Limit (Program GUI)**
To ensure responsible file creation and prevent storage bombing, the **file size** is capped at a **maximum limit** (e.g., 1 GB). The application will notify the user if they attempt to create a file that exceeds this limit.

### **File Deletion (CLI)**  
In the console CLI, users can delete files by specifying their names. Deleting files is a permanent action; therefore, a warning will be displayed before confirming deletion.

---

## **Contributing**

We welcome contributions! If you have ideas for improvements, bug fixes, or features, feel free to submit a pull request.

---

## **Support**

For support, open an issue in the **Issues** section of this repository. We'll be happy to assist you!