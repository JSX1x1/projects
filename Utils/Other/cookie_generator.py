import sys
import random
import string
import csv
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QSpinBox, QCheckBox, QPushButton


"""
Advanced Cookie Generator (PyQt6)
----------------------------------

Usage:
- This tool generates random HTTP cookies with customizable attributes.
- Users can specify parameters such as domain, path, expiry, security flags (Secure, HttpOnly, SameSite), and more.
- The generated cookies are saved in a CSV file (`cookies.csv`) for further analysis.

Use Cases:
1. **Web Development & Testing**  
   - Simulate different cookies for authentication, tracking, or session management.  
   - Test how web applications handle various cookie attributes (e.g., HttpOnly, Secure, SameSite).  

2. **Security & Penetration Testing**  
   - Evaluate the impact of improperly configured cookies.  
   - Analyze how websites handle expired or tampered cookies.  

3. **Automated Testing & Load Simulation**  
   - Generate large sets of cookies to stress-test backend session management.  
   - Use in automation scripts to mimic user sessions.  

4. **Education & Research**  
   - Learn about cookies and web security by experimenting with different configurations.  
   - Demonstrate how cookie policies affect browser behavior.  

This tool is designed for developers, security researchers, and testers who need a flexible way to generate and analyze cookies.
"""


class CookieGenerator(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize the window
        self.setWindowTitle("Advanced Cookie Generator")
        self.setGeometry(100, 100, 400, 400)

        # Create layout
        self.layout = QVBoxLayout()

        # Add components to the layout
        self._create_widgets()

        # Set the layout
        self.setLayout(self.layout)

    def _create_widgets(self):
        # Input for number of cookies
        self.num_cookies_label = QLabel("Number of Cookies:")
        self.num_cookies_spinbox = QSpinBox()
        self.num_cookies_spinbox.setRange(1, 100)
        self.num_cookies_spinbox.setValue(5)

        # Input for username format
        self.username_label = QLabel("Username Prefix:")
        self.username_input = QLineEdit("user_")

        # Input for domain
        self.domain_label = QLabel("Domain:")
        self.domain_input = QLineEdit("example.com")

        # Path input
        self.path_label = QLabel("Path:")
        self.path_input = QLineEdit("/")

        # Expiry options
        self.expiry_label = QLabel("Cookie Expiry (in days):")
        self.expiry_spinbox = QSpinBox()
        self.expiry_spinbox.setRange(1, 365)
        self.expiry_spinbox.setValue(30)

        # Cookie Name
        self.name_label = QLabel("Cookie Name:")
        self.name_input = QLineEdit("session")

        # Comment for the cookie
        self.comment_label = QLabel("Comment (Optional):")
        self.comment_input = QLineEdit("No comment")

        # Version for the cookie
        self.version_label = QLabel("Version (Optional):")
        self.version_input = QLineEdit("1")

        # Checkbox for secure cookie
        self.secure_checkbox = QCheckBox("Secure Cookie (HTTPS Only)")

        # Checkbox for HttpOnly cookie
        self.httponly_checkbox = QCheckBox("HttpOnly (Can't be accessed by JavaScript)")

        # Checkbox for SameSite cookie
        self.samesite_checkbox = QCheckBox("SameSite (Strict)")

        # Generate button
        self.generate_button = QPushButton("Generate Cookies")
        self.generate_button.clicked.connect(self.generate_cookies)

        # Adding widgets to the layout
        self.layout.addWidget(self.num_cookies_label)
        self.layout.addWidget(self.num_cookies_spinbox)
        self.layout.addWidget(self.username_label)
        self.layout.addWidget(self.username_input)
        self.layout.addWidget(self.domain_label)
        self.layout.addWidget(self.domain_input)
        self.layout.addWidget(self.path_label)
        self.layout.addWidget(self.path_input)
        self.layout.addWidget(self.expiry_label)
        self.layout.addWidget(self.expiry_spinbox)
        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.name_input)
        self.layout.addWidget(self.comment_label)
        self.layout.addWidget(self.comment_input)
        self.layout.addWidget(self.version_label)
        self.layout.addWidget(self.version_input)
        self.layout.addWidget(self.secure_checkbox)
        self.layout.addWidget(self.httponly_checkbox)
        self.layout.addWidget(self.samesite_checkbox)
        self.layout.addWidget(self.generate_button)

    def generate_cookies(self):
        # Get input values
        num_cookies = self.num_cookies_spinbox.value()
        username_prefix = self.username_input.text()
        domain = self.domain_input.text()
        path = self.path_input.text()
        expiry_days = self.expiry_spinbox.value()
        cookie_name = self.name_input.text()
        comment = self.comment_input.text()
        version = self.version_input.text()
        is_secure = self.secure_checkbox.isChecked()
        is_httponly = self.httponly_checkbox.isChecked()
        is_samesite = self.samesite_checkbox.isChecked()

        # Generate cookies
        cookies = []
        for _ in range(num_cookies):
            username = username_prefix + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
            session_id = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
            expiry = f"Max-Age={expiry_days * 86400}"

            # Add cookie details to list for saving
            cookies.append([
                cookie_name,
                session_id,
                domain,
                path,
                expiry,
                comment,
                version,
                "Secure" if is_secure else "",
                "HttpOnly" if is_httponly else "",
                "SameSite" if is_samesite else ""
            ])

        # Save cookies to CSV
        with open("cookies.csv", mode="a", newline="") as file:
            writer = csv.writer(file)
            for cookie in cookies:
                writer.writerow(cookie)

        # Display a message box confirming save (optional)
        print(f"Generated {num_cookies} cookies and saved them to 'cookies.csv'.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CookieGenerator()
    window.show()
    sys.exit(app.exec())
