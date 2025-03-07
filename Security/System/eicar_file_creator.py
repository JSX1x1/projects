import os
import sys
from PyQt6.QtWidgets import QApplication, QMessageBox

"""
Only run this if you want to test your antivirus.
Do not use this on a system where antivirus alerts are disruptive.
This test file is safe and widely recognized, but antivirus programs will treat it as malware.
"""


EICAR_TEST_STRING = """X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*"""

def create_eicar_file():
    """Creates an EICAR test file to trigger antivirus detection."""
    try:
        with open("eicar_test.txt", "w") as file:
            file.write(EICAR_TEST_STRING)
        QMessageBox.information(None, "Success", "EICAR test file created successfully.")
    except Exception as e:
        QMessageBox.critical(None, "Error", f"Failed to create EICAR file: {e}")

def main():
    """Main function to display confirmation dialog."""
    app = QApplication(sys.argv)

    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Icon.Warning)
    msg_box.setWindowTitle("Windows Defender Test")
    msg_box.setText("This tool will create an EICAR test file to test Windows Defender.\n\n"
                    "This is a harmless test file, but it WILL trigger antivirus detection.\n\n"
                    "Do you want to continue?")
    msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

    response = msg_box.exec()

    if response == QMessageBox.StandardButton.Yes:
        create_eicar_file()
    else:
        QMessageBox.information(None, "Cancelled", "Operation cancelled by user.")

if __name__ == "__main__":
    main()
