import sys
import time
import itertools
import string
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QProgressBar
from PyQt6.QtCore import QThread, pyqtSignal, Qt


# 🔹 Brute Force Simulation Thread
class BruteForceThread(QThread):
    update_signal = pyqtSignal(str, int)  # Signal for updating UI (current guess, attempts)

    def __init__(self, target_password, rate_limit=0.01):
        super().__init__()
        self.target_password = target_password
        self.rate_limit = rate_limit  # Simulated delay per attempt
        self.running = True  # Control flag

    def run(self):
        charset = string.ascii_letters + string.digits  # Character set for brute force
        attempts = 0

        for length in range(1, len(self.target_password) + 1):
            for guess in itertools.product(charset, repeat=length):
                if not self.running:
                    return

                attempts += 1
                guessed_password = ''.join(guess)

                # Emit signal to update the GUI
                self.update_signal.emit(guessed_password, attempts)

                if guessed_password == self.target_password:
                    return

                time.sleep(self.rate_limit)  # Simulated rate limit delay

    def stop(self):
        self.running = False


# 🔹 Main PyQt6 GUI Window
class BruteForceGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Brute Force Attack Emulator")
        self.setFixedSize(500, 400)
        self.setStyleSheet(self.load_stylesheet())  # Load QSS style

        layout = QVBoxLayout()

        # Title Label
        self.title_label = QLabel("🔐 Brute Force Password Emulator")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title_label)

        # Password Input Field
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password to simulate attack...")
        layout.addWidget(self.password_input)

        # Start Button
        self.start_button = QPushButton("Start Attack")
        self.start_button.clicked.connect(self.start_attack)
        layout.addWidget(self.start_button)

        # Status Label
        self.status_label = QLabel("Status: Waiting for input...")
        layout.addWidget(self.status_label)

        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        layout.addWidget(self.progress_bar)

        # Attempts Counter
        self.attempts_label = QLabel("Attempts: 0")
        layout.addWidget(self.attempts_label)

        self.setLayout(layout)
        self.brute_force_thread = None  # Placeholder for the thread

    def start_attack(self):
        target_password = self.password_input.text()
        if not target_password:
            self.status_label.setText("❌ Enter a password first!")
            return

        self.status_label.setText("🔄 Brute-force attack in progress...")
        self.progress_bar.setValue(0)
        self.attempts_label.setText("Attempts: 0")

        # Start brute-force simulation in a separate thread
        self.brute_force_thread = BruteForceThread(target_password)
        self.brute_force_thread.update_signal.connect(self.update_gui)
        self.brute_force_thread.start()

    def update_gui(self, guessed_password, attempts):
        self.status_label.setText(f"Trying: {guessed_password}")
        self.attempts_label.setText(f"Attempts: {attempts}")

        progress = min((attempts / 10000) * 100, 100)  # Fake progress bar update
        self.progress_bar.setValue(int(progress))

        if guessed_password == self.password_input.text():
            self.status_label.setText("✅ Password Cracked!")
            self.brute_force_thread.stop()

    def load_stylesheet(self):
        return """
        QWidget {
            background-color: #1e1e2e;
            color: #ffffff;
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 14px;
        }

        QPushButton {
            background-color: #4a4a9c;
            border: 2px solid #5a5abe;
            border-radius: 5px;
            padding: 8px;
            color: white;
            font-weight: bold;
        }

        QPushButton:hover {
            background-color: #5a5abe;
        }

        QLineEdit {
            background-color: #29293d;
            border: 1px solid #5a5abe;
            color: #ffffff;
            padding: 6px;
            border-radius: 5px;
        }

        QLabel {
            font-size: 16px;
            color: #cfcfcf;
        }

        QProgressBar {
            border: 1px solid #5a5abe;
            border-radius: 5px;
            background-color: #29293d;
            text-align: center;
        }

        QProgressBar::chunk {
            background-color: #5a5abe;
            width: 10px;
        }
        """


# 🔹 Run the Application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BruteForceGUI()
    window.show()
    sys.exit(app.exec())
