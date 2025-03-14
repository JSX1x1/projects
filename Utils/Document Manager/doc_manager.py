import sys
import os
import json
import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QTextEdit, QPushButton,
    QVBoxLayout, QWidget, QTreeView, QHBoxLayout, QTabWidget,
    QLabel, QLineEdit, QSplitter, QMessageBox
)
from PyQt6.QtGui import QFileSystemModel
from PyQt6.QtCore import Qt


class DocumentManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Document Management System")
        self.setGeometry(100, 100, 1200, 700)

        # Main Layout
        main_layout = QHBoxLayout()
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # File Tree View
        self.folder_path = os.getcwd()  
        self.file_model = QFileSystemModel()
        self.file_model.setRootPath(self.folder_path)

        self.tree = QTreeView()
        self.tree.setModel(self.file_model)
        self.tree.setRootIndex(self.file_model.index(self.folder_path))
        self.tree.clicked.connect(self.open_selected_document)

        # Tabs
        self.tabs = QTabWidget()
        self.create_tab = QWidget()
        self.editor_tab = QWidget()
        self.assignment_tab = QWidget()
        self.tabs.addTab(self.create_tab, "Create")
        self.tabs.addTab(self.editor_tab, "Edit Document")
        self.tabs.addTab(self.assignment_tab, "Assignments")

        # Create Tab Layout
        create_layout = QVBoxLayout()
        self.create_file_button = QPushButton("New Document")
        self.create_file_button.clicked.connect(self.new_document)
        self.create_folder_button = QPushButton("New Folder")
        self.create_folder_button.clicked.connect(self.create_new_folder)
        create_layout.addWidget(self.create_file_button)
        create_layout.addWidget(self.create_folder_button)
        self.create_tab.setLayout(create_layout)

        # **Editor Layout (Now Includes Save Button)**
        editor_layout = QVBoxLayout()
        self.editor = QTextEdit()
        self.editor.textChanged.connect(self.highlight_changes)
        self.save_edit_button = QPushButton("Save Changes")
        self.save_edit_button.clicked.connect(self.save_document)  # **Fix: Save button added**
        editor_layout.addWidget(self.editor)
        editor_layout.addWidget(self.save_edit_button)
        self.editor_tab.setLayout(editor_layout)

        # Assignments Layout
        assignment_layout = QVBoxLayout()
        self.assign_label = QLabel("Assign Document")
        self.assign_name = QLineEdit()
        self.assign_reason = QLineEdit()
        self.assign_button = QPushButton("Assign")
        self.assign_button.clicked.connect(self.assign_document)

        assignment_layout.addWidget(self.assign_label)
        assignment_layout.addWidget(QLabel("Contact Name:"))
        assignment_layout.addWidget(self.assign_name)
        assignment_layout.addWidget(QLabel("Assignment Reason:"))
        assignment_layout.addWidget(self.assign_reason)
        assignment_layout.addWidget(self.assign_button)
        self.assignment_tab.setLayout(assignment_layout)

        # Right Panel (Version History)
        right_panel = QVBoxLayout()
        self.version_label = QLabel("Version History")
        self.version_list = QTextEdit()
        self.version_list.setReadOnly(True)
        right_panel.addWidget(self.version_label)
        right_panel.addWidget(self.version_list)
        right_widget = QWidget()
        right_widget.setLayout(right_panel)

        # Add widgets to splitter
        splitter.addWidget(self.tree)
        splitter.addWidget(self.tabs)
        splitter.addWidget(right_widget)

        # Final Layout
        main_widget = QWidget()
        main_layout.addWidget(splitter)
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # Current File Tracker
        self.current_file = None
        self.last_saved_content = ""

        # Apply Dark Mode
        self.setStyleSheet("""
            QMainWindow { background-color: #121212; color: white; }
            QTextEdit { background-color: #1e1e1e; color: #ffffff; font-size: 14px; }
            QPushButton { background-color: #333333; color: white; border: none; padding: 8px; }
            QPushButton:hover { background-color: #555555; }
            QLabel { font-size: 14px; }
            QLineEdit { background-color: #222222; color: white; padding: 5px; }
        """)

    def new_document(self):
        """Create a new document."""
        file_name, _ = QFileDialog.getSaveFileName(self, "New Document", "", "XDoc Files (*.xdoc);;All Files (*)")

        if file_name:
            if not file_name.endswith(".xdoc"):
                file_name += ".xdoc"

            data = {
                "document_name": os.path.basename(file_name),
                "versions": [{"timestamp": str(datetime.datetime.now()), "content": ""}],
                "assignments": []
            }
            with open(file_name, "w") as file:
                json.dump(data, file, indent=4)

            self.current_file = file_name
            self.editor.clear()
            self.last_saved_content = ""
            self.load_version_list(data["versions"])

    def open_selected_document(self, index):
        """Open a selected document."""
        file_path = self.file_model.filePath(index)
        if file_path.endswith(".xdoc"):
            self.current_file = file_path
            with open(file_path, "r") as file:
                data = json.load(file)

            self.editor.setText(data["versions"][-1]["content"])
            self.last_saved_content = data["versions"][-1]["content"]
            self.load_version_list(data["versions"])

    def save_document(self):
        """Save changes to the document and add a new version."""
        if not self.current_file:
            QMessageBox.warning(self, "Error", "No document selected.")
            return

        new_content = self.editor.toPlainText()
        if new_content == self.last_saved_content:
            return  

        with open(self.current_file, "r") as file:
            data = json.load(file)

        new_version = {
            "timestamp": str(datetime.datetime.now()),
            "content": new_content
        }
        data["versions"].append(new_version)

        with open(self.current_file, "w") as file:
            json.dump(data, file, indent=4)

        self.last_saved_content = new_content
        self.load_version_list(data["versions"])
        self.remove_highlight()
        QMessageBox.information(self, "Saved", "Changes saved successfully!")

    def highlight_changes(self):
        """Highlights unsaved changes in the editor."""
        if self.editor.toPlainText() != self.last_saved_content:
            self.editor.setStyleSheet("color: #ffcc00; font-weight: bold;")
        else:
            self.remove_highlight()

    def remove_highlight(self):
        """Removes unsaved change highlighting."""
        self.editor.setStyleSheet("color: #ffffff; font-weight: normal;")

    def load_version_list(self, versions):
        """Displays the available versions in the right panel."""
        self.version_list.clear()
        for v in versions:
            self.version_list.append(f"{v['timestamp']}\n{v['content'][:50]}...\n")

    def assign_document(self):
        """Assigns a document and saves assignment info inside the .xdoc file."""
        if not self.current_file:
            QMessageBox.warning(self, "Error", "No document selected.")
            return

        with open(self.current_file, "r") as file:
            data = json.load(file)

        assignment = {
            "contact": self.assign_name.text(),
            "reason": self.assign_reason.text()
        }
        data["assignments"].append(assignment)

        with open(self.current_file, "w") as file:
            json.dump(data, file, indent=4)

        QMessageBox.information(self, "Success", "Document assigned!")

    def create_new_folder(self):
        """Creates a new folder."""
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder Location")
        if folder_path:
            os.makedirs(os.path.join(folder_path, "New Folder"), exist_ok=True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DocumentManager()
    window.show()
    sys.exit(app.exec())