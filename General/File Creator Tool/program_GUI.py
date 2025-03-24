import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QComboBox, QPushButton, QLabel, QSpinBox, QTextEdit
from PyQt6.QtCore import Qt

MAX_FILE_SIZE_MB = 50  # Maximum file size in MB (you can change this as needed)

class FileCreatorTool(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Creator Tool")
        self.setGeometry(100, 100, 500, 400)
        self.init_ui()

    def init_ui(self):
        # Set layout
        layout = QVBoxLayout()

        # File name input
        self.file_name_label = QLabel("File Name:")
        self.file_name_input = QLineEdit(self)
        self.file_name_input.setPlaceholderText("Enter file name")

        # File extension input
        self.extension_label = QLabel("File Extension:")
        self.extension_combo = QComboBox(self)
        # Add common extensions to the combo box
        self.extension_combo.addItems([
            ".txt", ".md", ".html", ".json", ".csv", ".log", ".py", ".yaml", ".cpp", ".css", ".js", ".xml", ".bat"
        ])

        # Custom extension input (optional, next to dropdown)
        self.custom_extension_input = QLineEdit(self)
        self.custom_extension_input.setPlaceholderText("Or enter custom extension")
        
        # File size input (if dummy file)
        self.size_label = QLabel("File Size (KB, for dummy file):")
        self.size_input = QSpinBox(self)
        self.size_input.setRange(1, 10000)  # User can input size between 1KB to 10MB
        self.size_input.setValue(1)

        # Custom content input (optional)
        self.content_label = QLabel("Custom Content (Optional):")
        self.content_input = QTextEdit(self)
        self.content_input.setPlaceholderText("Enter custom content if you want...")

        # Create File button
        self.create_button = QPushButton("Create File", self)
        self.create_button.clicked.connect(self.create_file)

        # Dark/Light mode toggle button
        self.mode_toggle_button = QPushButton("Toggle Dark/Light Mode", self)
        self.mode_toggle_button.clicked.connect(self.toggle_mode)

        # Status message
        self.status_label = QLabel("")
        
        # Add widgets to layout
        layout.addWidget(self.file_name_label)
        layout.addWidget(self.file_name_input)
        layout.addWidget(self.extension_label)
        layout.addWidget(self.extension_combo)
        layout.addWidget(self.custom_extension_input)
        layout.addWidget(self.size_label)
        layout.addWidget(self.size_input)
        layout.addWidget(self.content_label)
        layout.addWidget(self.content_input)
        layout.addWidget(self.create_button)
        layout.addWidget(self.mode_toggle_button)
        layout.addWidget(self.status_label)

        self.setLayout(layout)

        # Default to light mode
        self.is_dark_mode = False
        self.apply_styles()

    def apply_styles(self):
        if self.is_dark_mode:
            dark_style = """
                QWidget {
                    background-color: #2b2b2b;
                    color: #f0f0f0;
                }
                QPushButton {
                    background-color: #555555;
                    color: #ffffff;
                    border: none;
                    padding: 5px 10px;
                }
                QLabel {
                    color: #ffffff;
                }
                QLineEdit, QTextEdit {
                    background-color: #3b3b3b;
                    color: #ffffff;
                    border: 1px solid #555555;
                    padding: 5px;
                }
                QComboBox {
                    background-color: #3b3b3b;
                    color: #ffffff;
                    border: 1px solid #555555;
                    padding: 5px;
                }
            """
            self.setStyleSheet(dark_style)
        else:
            light_style = """
                QWidget {
                    background-color: #f0f0f0;
                    color: #000000;
                }
                QPushButton {
                    background-color: #4CAF50;
                    color: #ffffff;
                    border: none;
                    padding: 5px 10px;
                }
                QLabel {
                    color: #000000;
                }
                QLineEdit, QTextEdit {
                    background-color: #ffffff;
                    color: #000000;
                    border: 1px solid #CCCCCC;
                    padding: 5px;
                }
                QComboBox {
                    background-color: #ffffff;
                    color: #000000;
                    border: 1px solid #CCCCCC;
                    padding: 5px;
                }
            """
            self.setStyleSheet(light_style)

    def toggle_mode(self):
        """Toggle between dark and light mode."""
        self.is_dark_mode = not self.is_dark_mode
        self.apply_styles()

    def create_file(self):
        # Get user inputs
        file_name = self.file_name_input.text().strip()
        extension = self.extension_combo.currentText()
        
        # Check if the user has entered a custom extension
        custom_extension = self.custom_extension_input.text().strip()
        if custom_extension:
            # Validate custom extension
            if not custom_extension.startswith("."):
                custom_extension = "." + custom_extension  # Add dot if missing
            extension = custom_extension

        file_size_kb = self.size_input.value()
        custom_content = self.content_input.toPlainText().strip()

        # Validate file name
        if not file_name:
            self.status_label.setText("Error: File name cannot be empty!")
            return

        # Add extension to the file name if not already included
        if not file_name.endswith(extension):
            file_name += extension

        # Validate file size (limit the file size to MAX_FILE_SIZE_MB)
        if file_size_kb > MAX_FILE_SIZE_MB * 1024:  # Convert MB to KB for comparison
            self.status_label.setText(f"Error: File size cannot exceed {MAX_FILE_SIZE_MB} MB!")
            return

        # Check if the user wants to create a dummy file or a custom content file
        if custom_content:
            # Create a file with custom content
            self.create_with_custom_content(file_name, custom_content)
        else:
            # Create a dummy file of specified size
            self.create_dummy_file(file_name, file_size_kb)

    def create_with_custom_content(self, file_name, content):
        # Create file with the custom content
        try:
            with open(file_name, 'w') as f:
                f.write(content)
            self.status_label.setText(f"File '{file_name}' created successfully with custom content.")
        except Exception as e:
            self.status_label.setText(f"Error: {e}")

    def create_dummy_file(self, file_name, size_kb):
        # Create a dummy file of the specified size
        try:
            with open(file_name, 'wb') as f:
                # Write dummy content to file
                f.write(os.urandom(size_kb * 1024))  # Random bytes to fill the file
            self.status_label.setText(f"Dummy file '{file_name}' of size {size_kb} KB created.")
        except Exception as e:
            self.status_label.setText(f"Error: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileCreatorTool()
    window.show()
    sys.exit(app.exec())
