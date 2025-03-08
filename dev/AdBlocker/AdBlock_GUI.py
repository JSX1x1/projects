import sys
from PyQt6.QtCore import QUrl, QTimer
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QListWidget, QLineEdit, QLabel


class BrowserIntegrationManager(QMainWindow):
    def __init__(self):
        super().__init__()

        # Store blocked URLs
        self.blocked_prefixes = []

        self.setWindowTitle("Browser Redirect and Popup Blocker Manager")
        self.setGeometry(100, 100, 600, 400)

        # Main widget and layout
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout(self.main_widget)

        # Display blocked URLs
        self.url_list_label = QLabel("Blocked URLs:")
        self.layout.addWidget(self.url_list_label)

        self.url_list = QListWidget()
        self.layout.addWidget(self.url_list)

        # Input field for adding new blocked URLs
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter URL prefix to block (e.g., https://malicious-site.com)")
        self.layout.addWidget(self.url_input)

        # Add/Remove buttons
        self.add_button = QPushButton("Add URL")
        self.add_button.clicked.connect(self.add_url)
        self.layout.addWidget(self.add_button)

        self.remove_button = QPushButton("Remove Selected URL")
        self.remove_button.clicked.connect(self.remove_url)
        self.layout.addWidget(self.remove_button)

        # Save button
        self.save_button = QPushButton("Save Block List")
        self.save_button.clicked.connect(self.save_to_file)
        self.layout.addWidget(self.save_button)

        # Status label
        self.status_label = QLabel("")
        self.layout.addWidget(self.status_label)

        # Load existing blocked URLs
        self.load_from_file()

    def add_url(self):
        url = self.url_input.text().strip()
        if url and url not in self.blocked_prefixes:
            self.blocked_prefixes.append(url)
            self.url_list.addItem(url)
            self.url_input.clear()
            self.status_label.setText(f"Added: {url}")

    def remove_url(self):
        selected_items = self.url_list.selectedItems()
        if selected_items:
            for item in selected_items:
                self.blocked_prefixes.remove(item.text())
                self.url_list.takeItem(self.url_list.row(item))
            self.status_label.setText("Removed selected URLs")
        else:
            self.status_label.setText("No URL selected")

    def save_to_file(self):
        with open("blocked_urls.txt", "w") as f:
            for url in self.blocked_prefixes:
                f.write(url + "\n")
        self.status_label.setText("Blocked URLs saved to file")

    def load_from_file(self):
        try:
            with open("blocked_urls.txt", "r") as f:
                self.blocked_prefixes = [line.strip() for line in f.readlines()]
                self.url_list.addItems(self.blocked_prefixes)
        except FileNotFoundError:
            pass  # No existing file, continue


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BrowserIntegrationManager()
    window.show()
    sys.exit(app.exec())
