import sys
import os
import zipfile
import datetime
import shutil
from pathlib import Path

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel,
    QFileDialog, QCheckBox, QProgressBar
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal


class SnapshotWorker(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(str)

    def __init__(self, folder_path, exclude_risky, exclude_unnecessary):
        super().__init__()
        self.folder_path = folder_path
        self.exclude_risky = exclude_risky
        self.exclude_unnecessary = exclude_unnecessary

    def run(self):
        """Handles snapshot creation in a separate thread."""
        folder = Path(self.folder_path)
        now = datetime.datetime.now().strftime("%m-%d-%Y")
        zip_filename = f"{now}-snapshot.zip"
        zip_path = folder.parent / zip_filename

        risky_files, unnecessary_files = analyze_files(folder)

        files_to_include = list(folder.rglob("*"))
        if self.exclude_risky:
            files_to_include = [f for f in files_to_include if f not in risky_files]
        if self.exclude_unnecessary:
            files_to_include = [f for f in files_to_include if f not in unnecessary_files]

        total_files = len(files_to_include)
        if total_files == 0:
            self.finished.emit("No files to compress!")
            return

        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for i, file in enumerate(files_to_include):
                if file.is_file():
                    arcname = file.relative_to(folder)
                    zipf.write(file, arcname)
                self.progress.emit(int((i + 1) / total_files * 100))

        self.finished.emit(f"Snapshot created: {zip_path}")


def get_folder_size(folder):
    """Calculate total size of a folder (in bytes)."""
    return sum(f.stat().st_size for f in Path(folder).rglob('*') if f.is_file())


def estimate_compressed_size(folder):
    """Estimate compressed size (roughly 50% of the original for testing)."""
    return get_folder_size(folder) * 0.5  # Approximation


def analyze_files(folder):
    """Detect risky and unnecessary files."""
    risky_files = []
    unnecessary_files = []

    for file in folder.rglob('*'):
        if file.is_file():
            # Check for unreadable files (simulated risk analysis)
            try:
                with open(file, 'rb'):
                    pass
            except:
                risky_files.append(file)

            # Identify unnecessary files (logs, cache, tmp)
            if file.suffix in ['.log', '.tmp', '.cache']:
                unnecessary_files.append(file)

    return risky_files, unnecessary_files


class SnapshotCreator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Snapshot Creator")
        self.setGeometry(100, 100, 500, 300)

        self.layout = QVBoxLayout()

        self.label_folder = QLabel("No folder selected.")
        self.label_folder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.label_folder)

        self.btn_select_folder = QPushButton("Select Folder")
        self.btn_select_folder.clicked.connect(self.select_folder)
        self.layout.addWidget(self.btn_select_folder)

        self.label_size = QLabel("Estimated Size: N/A")
        self.layout.addWidget(self.label_size)

        self.label_compressed_size = QLabel("Estimated Compressed Size: N/A")
        self.layout.addWidget(self.label_compressed_size)

        self.label_risk = QLabel("Corruption Risk: N/A")
        self.layout.addWidget(self.label_risk)

        self.label_unnecessary = QLabel("Unnecessary Files: N/A")
        self.layout.addWidget(self.label_unnecessary)

        self.chk_exclude_risky = QCheckBox("Exclude risky files")
        self.layout.addWidget(self.chk_exclude_risky)

        self.chk_exclude_unnecessary = QCheckBox("Exclude unnecessary files")
        self.layout.addWidget(self.chk_exclude_unnecessary)

        self.btn_create_snapshot = QPushButton("Create Snapshot")
        self.btn_create_snapshot.clicked.connect(self.create_snapshot)
        self.layout.addWidget(self.btn_create_snapshot)

        self.progress_bar = QProgressBar()
        self.layout.addWidget(self.progress_bar)

        self.setLayout(self.layout)
        self.folder_path = None

    def select_folder(self):
        """Opens a folder selection dialog."""
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.folder_path = folder
            self.label_folder.setText(f"Selected: {folder}")

            # Calculate and display details
            total_size = get_folder_size(folder)
            compressed_size = estimate_compressed_size(folder)
            risky_files, unnecessary_files = analyze_files(Path(folder))

            self.label_size.setText(f"Estimated Size: {total_size / (1024 ** 2):.2f} MB")
            self.label_compressed_size.setText(f"Compressed Size: {compressed_size / (1024 ** 2):.2f} MB")
            self.label_risk.setText(f"Corruption Risk: {len(risky_files)} files")
            self.label_unnecessary.setText(f"Unnecessary Files: {len(unnecessary_files)} files")

    def create_snapshot(self):
        """Starts the snapshot creation process in a separate thread."""
        if not self.folder_path:
            self.label_folder.setText("Please select a folder first!")
            return

        self.btn_create_snapshot.setEnabled(False)
        self.progress_bar.setValue(0)

        self.worker = SnapshotWorker(
            self.folder_path,
            self.chk_exclude_risky.isChecked(),
            self.chk_exclude_unnecessary.isChecked()
        )

        self.worker.progress.connect(self.progress_bar.setValue)
        self.worker.finished.connect(self.on_snapshot_complete)
        self.worker.start()

    def on_snapshot_complete(self, message):
        """Handles snapshot completion."""
        self.btn_create_snapshot.setEnabled(True)
        self.label_folder.setText(message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SnapshotCreator()
    window.show()
    sys.exit(app.exec())
