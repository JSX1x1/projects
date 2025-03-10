import sys
import requests
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QWidget

# Function to check robots.txt
def check_robots_txt(url, output_text):
    """Checks the robots.txt file for the given URL and outputs the scraping rules."""
    robots_url = url.rstrip('/') + '/robots.txt'
    
    try:
        # Send request to robots.txt
        response = requests.get(robots_url)
        
        if response.status_code == 200:
            output_text.append(f"robots.txt found for {url}:\n\n")
            output_text.append(response.text + "\n")
            output_text.append("\n\n# Hacker Style: The Rules of the Website! #\n")
            output_text.append("Explanation:\n")
            output_text.append("User-agent: * -> All bots are affected.\n")
            output_text.append("Disallow: / -> Access to the entire content is blocked.\n")
            output_text.append("Allow: / -> Access to the content is allowed.\n")
        else:
            output_text.append(f"robots.txt not found for {url} (Status code {response.status_code}).\n")
    
    except requests.exceptions.RequestException as e:
        output_text.append(f"Error fetching robots.txt: {e}\n")

# PyQt6 Window class
class RobotsCheckerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the main window
        self.setWindowTitle("Robots.txt Checker - Hacker Style")
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet("background-color: black; color: green; font-family: Courier;")

        # Layout and widgets
        layout = QVBoxLayout()

        # Title label
        title_label = QLabel("Robots.txt Checker", self)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(title_label)

        # URL input field
        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText("Enter website URL (e.g., https://example.com)")
        self.url_input.setStyleSheet("background-color: black; color: green; font-size: 14px; padding: 5px;")
        layout.addWidget(self.url_input)

        # Button to check robots.txt
        check_button = QPushButton("Check robots.txt", self)
        check_button.setStyleSheet("background-color: green; color: black; font-size: 14px;")
        check_button.clicked.connect(self.check_robots_txt)
        layout.addWidget(check_button)

        # Output text area
        self.output_text = QTextEdit(self)
        self.output_text.setReadOnly(True)
        self.output_text.setStyleSheet("background-color: black; color: green; font-size: 14px; padding: 5px;")
        layout.addWidget(self.output_text)

        # Set the main layout
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def check_robots_txt(self):
        url = self.url_input.text()
        if url:
            self.output_text.clear()  # Clear previous output
            check_robots_txt(url, self.output_text)

# Main execution
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create the application window
    window = RobotsCheckerApp()
    window.show()

    # Run the application
    sys.exit(app.exec())
