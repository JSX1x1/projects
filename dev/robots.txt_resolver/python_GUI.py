import sys
import requests
from urllib.parse import urlparse
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QWidget

def check_robots_txt(url, output_text):
    """Attempts to retrieve robots.txt from multiple variations of the URL."""
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    alt_url = f"https://www.{parsed_url.netloc}" if not parsed_url.netloc.startswith("www.") else f"https://{parsed_url.netloc.replace('www.', '')}"
    robots_urls = [
        f"{base_url}/robots.txt",
        f"{alt_url}/robots.txt"
    ]
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    for robots_url in robots_urls:
        try:
            response = requests.get(robots_url, headers=headers, timeout=5, allow_redirects=True)
            if response.status_code == 200:
                output_text.append(f"robots.txt found at {robots_url}:")
                output_text.append(response.text + "\n")
                return
        except requests.exceptions.RequestException as e:
            output_text.append(f"Error fetching {robots_url}: {e}\n")
    
    output_text.append("No robots.txt found at any tested location.\n")

class RobotsCheckerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Robots.txt Checker - Enhanced")
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet("background-color: black; color: green; font-family: Courier;")
        layout = QVBoxLayout()
        
        title_label = QLabel("Robots.txt Checker", self)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(title_label)

        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText("Enter website URL (e.g., https://example.com)")
        self.url_input.setStyleSheet("background-color: black; color: green; font-size: 14px; padding: 5px;")
        layout.addWidget(self.url_input)

        check_button = QPushButton("Check robots.txt", self)
        check_button.setStyleSheet("background-color: green; color: black; font-size: 14px;")
        check_button.clicked.connect(self.check_robots_txt)
        layout.addWidget(check_button)

        self.output_text = QTextEdit(self)
        self.output_text.setReadOnly(True)
        self.output_text.setStyleSheet("background-color: black; color: green; font-size: 14px; padding: 5px;")
        layout.addWidget(self.output_text)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def check_robots_txt(self):
        url = self.url_input.text().strip()
        if url:
            self.output_text.clear()
            check_robots_txt(url, self.output_text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RobotsCheckerApp()
    window.show()
    sys.exit(app.exec())
