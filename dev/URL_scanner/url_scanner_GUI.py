import sys
import requests
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QLineEdit, QTextEdit, QVBoxLayout
)

# OPTIONAL: Use VirusTotal API (Get API Key from virustotal.com)
API_KEY = "YOUR_VIRUSTOTAL_API_KEY"

class URLScannerGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("URL Scanner & Security Checker")
        self.setGeometry(300, 200, 600, 400)
        self.setStyleSheet("background-color: #121212; color: white;")

        layout = QVBoxLayout()

        self.url_label = QLabel("Enter URL to Scan:")
        layout.addWidget(self.url_label)
        
        self.url_input = QLineEdit()
        layout.addWidget(self.url_input)

        self.scan_button = QPushButton("Scan URL")
        self.scan_button.clicked.connect(self.scan_url)
        layout.addWidget(self.scan_button)

        self.result_output = QTextEdit()
        self.result_output.setReadOnly(True)
        self.result_output.setStyleSheet("background-color: #1e1e1e; color: #00ff00;")
        layout.addWidget(self.result_output)

        self.setLayout(layout)

    def scan_url(self):
        """Scans the entered URL using VirusTotal API or a local blacklist."""
        url = self.url_input.text().strip()
        if not url:
            self.result_output.setText("❌ Please enter a valid URL!")
            return

        self.result_output.setText(f"🔍 Scanning {url}...\n")

        # Check VirusTotal API
        if API_KEY:
            headers = {"x-apikey": API_KEY}
            response = requests.get(f"https://www.virustotal.com/api/v3/urls/{url}", headers=headers)

            if response.status_code == 200:
                result = response.json()
                score = result["data"]["attributes"]["last_analysis_stats"]["malicious"]
                if score > 0:
                    self.result_output.append(f"🚨 Warning! This URL is flagged as MALICIOUS by {score} sources!")
                else:
                    self.result_output.append("✅ This URL appears to be safe.")
            else:
                self.result_output.append(f"⚠️ VirusTotal API Error: {response.status_code}")

        else:
            # Local Blacklist Check (for offline mode)
            blacklist = ["malicious.com", "phishingsite.net"]
            if any(blocked in url for blocked in blacklist):
                self.result_output.append("🚨 Warning! This URL is in the local blacklist.")
            else:
                self.result_output.append("✅ No issues found in local blacklist.")

# Run Application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = URLScannerGUI()
    window.show()
    sys.exit(app.exec())
