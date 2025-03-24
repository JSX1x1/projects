import sys
import subprocess
import os
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton
from PyQt6.QtCore import Qt

class TerminalApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("File Management Terminal")
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()

        # Text area for terminal output
        self.output_area = QTextEdit(self)
        self.output_area.setReadOnly(True)  # Set to read-only for output display
        self.output_area.setStyleSheet("""
            background-color: #e6f7ff;  /* Light blue background */
            color: #333333;  /* Dark text color */
            font-family: Consolas, 'Courier New', monospace;  /* Monospaced font */
            font-size: 12pt;
            border: none;
            padding: 10px;
        """)
        self.layout.addWidget(self.output_area)

        # Input field for commands
        self.command_input = QLineEdit(self)
        self.command_input.setPlaceholderText("Enter a command...")
        self.command_input.returnPressed.connect(self.execute_command)
        self.command_input.setStyleSheet("""
            background-color: #cce0ff;  /* Lighter blue background for input */
            color: #333333;  /* Dark text */
            font-family: Consolas, 'Courier New', monospace;  /* Monospaced font */
            font-size: 12pt;
            border: 1px solid #b3c6e6;
            padding: 5px;
        """)
        self.layout.addWidget(self.command_input)

        # Execute button (optional, can also press Enter)
        self.execute_button = QPushButton("Execute", self)
        self.execute_button.clicked.connect(self.execute_command)
        self.execute_button.setStyleSheet("""
            background-color: #66b3ff;  /* Light blue button */
            color: white;  /* White text */
            font-family: Consolas, 'Courier New', monospace;
            font-size: 12pt;
            border: none;
            padding: 10px;
        """)
        self.layout.addWidget(self.execute_button)

        self.setLayout(self.layout)

        # Current working directory (initially set to the current directory)
        self.current_directory = os.getcwd()

    def execute_command(self):
        command = self.command_input.text()

        if command:
            # Append the command to the output area
            self.output_area.append(f"$ {command}")

            # Check the command and handle it
            if command.startswith("mkdir "):
                self.create_directory(command)
            elif command.startswith("rmdir "):
                self.remove_directory(command)
            elif command.startswith("touch "):
                self.create_file(command)
            elif command.startswith("edit "):
                self.edit_file(command)
            elif command == "help":
                self.show_help()
            elif command.startswith("tree"):
                self.show_tree(command)
            elif command.startswith("cd "):
                self.change_directory(command)
            elif command == "ls":
                self.list_directory()
            else:
                # Run general commands using subprocess
                self.run_system_command(command)

            # Clear the input field
            self.command_input.clear()

    def create_directory(self, command):
        directory_name = command[len("mkdir "):].strip()

        if directory_name:
            try:
                os.makedirs(directory_name)
                self.output_area.append(f"Directory '{directory_name}' created.")
            except Exception as e:
                self.output_area.append(f"Error creating directory: {str(e)}")
        else:
            self.output_area.append("Error: No directory name specified.")

    def remove_directory(self, command):
        directory_name = command[len("rmdir "):].strip()

        if directory_name:
            try:
                os.rmdir(directory_name)
                self.output_area.append(f"Directory '{directory_name}' removed.")
            except Exception as e:
                self.output_area.append(f"Error removing directory: {str(e)}")
        else:
            self.output_area.append("Error: No directory name specified.")

    def create_file(self, command):
        filename = command[len("touch "):].strip()

        if filename:
            try:
                # Create an empty file with the given filename
                with open(filename, 'w') as f:
                    pass
                self.output_area.append(f"File '{filename}' created.")
            except Exception as e:
                self.output_area.append(f"Error creating file: {str(e)}")
        else:
            self.output_area.append("Error: No filename specified.")

    def edit_file(self, command):
        filename = command[len("edit "):].strip()

        if filename:
            try:
                # Attempt to open the file using a text editor
                if sys.platform == "win32":
                    subprocess.run(["notepad", filename])
                else:
                    subprocess.run(["nano", filename])
                self.output_area.append(f"Editing file: {filename}")
            except Exception as e:
                self.output_area.append(f"Error editing file: {str(e)}")
        else:
            self.output_area.append("Error: No filename specified.")

    def show_help(self):
        help_text = """
        Supported commands:
        
        mkdir <directory>     - Create a new directory.
        rmdir <directory>     - Remove an existing directory.
        touch <filename>      - Create an empty file with the given filename.
        edit <filename>       - Edit the specified file with the default editor (Notepad or nano).
        tree                  - Display the directory tree structure.
        cd <path>             - Change the current directory.
        ls                    - List the contents of the current directory.
        help                  - Display this help message.
        """
        self.output_area.append(help_text)

    def show_tree(self, command):
        try:
            # Check if `tree` command is available on the system
            if sys.platform == "win32":
                # Windows does not have a native `tree` command in Python, but it has `tree` in cmd
                result = subprocess.run(["tree"], capture_output=True, text=True, shell=True)
            else:
                # On Linux/macOS, `tree` is usually available
                result = subprocess.run(["tree"], capture_output=True, text=True)

            if result.stdout:
                self.output_area.append(result.stdout)
            if result.stderr:
                self.output_area.append(f"Error: {result.stderr}")
        except Exception as e:
            self.output_area.append(f"Error displaying tree: {str(e)}")

    def change_directory(self, command):
        new_dir = command[len("cd "):].strip()

        if new_dir:
            try:
                # Change the current working directory
                os.chdir(new_dir)
                self.current_directory = os.getcwd()
                self.output_area.append(f"Changed directory to {self.current_directory}")
            except FileNotFoundError:
                self.output_area.append(f"Error: The directory '{new_dir}' does not exist.")
            except PermissionError:
                self.output_area.append(f"Error: You do not have permission to access '{new_dir}'.")
            except Exception as e:
                self.output_area.append(f"Error: {str(e)}")
        else:
            self.output_area.append("Error: No directory path specified.")

    def list_directory(self):
        try:
            # List the files and directories in the current directory
            files = os.listdir(self.current_directory)
            if files:
                for file in files:
                    self.output_area.append(file)
            else:
                self.output_area.append("The directory is empty.")
        except Exception as e:
            self.output_area.append(f"Error listing directory: {str(e)}")

    def run_system_command(self, command):
        try:
            # Run general system commands using subprocess
            result = subprocess.run(command, shell=True, capture_output=True, text=True)

            # Display standard output
            if result.stdout:
                self.output_area.append(result.stdout)

            # Display standard error if any
            if result.stderr:
                self.output_area.append(f"Error: {result.stderr}")
        except Exception as e:
            self.output_area.append(f"Error executing command: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TerminalApp()
    window.show()
    sys.exit(app.exec())
