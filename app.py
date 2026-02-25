"""Lexloop — DSL correction feedback loop.

PyQt6 GUI: pick a file, click Run, see results in the browser.
"""

import sys

from PyQt6.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

import runner


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lexloop")
        self.setMinimumWidth(500)

        # Widgets
        self.path_edit = QLineEdit()
        self.path_edit.setReadOnly(True)
        self.path_edit.setPlaceholderText("No file selected")

        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self.browse)

        self.run_btn = QPushButton("Run")
        self.run_btn.clicked.connect(self.run)
        self.run_btn.setEnabled(False)

        self.status_label = QLabel("Select a file and click Run.")

        # Layout
        file_row = QHBoxLayout()
        file_row.addWidget(self.path_edit, stretch=1)
        file_row.addWidget(browse_btn)

        layout = QVBoxLayout()
        layout.addLayout(file_row)
        layout.addWidget(self.run_btn)
        layout.addWidget(self.status_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def browse(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select DSL file", "", "All Files (*)"
        )
        if path:
            self.path_edit.setText(path)
            self.run_btn.setEnabled(True)

    def run(self):
        file_path = self.path_edit.text()
        if not file_path:
            return
        self.status_label.setText("Running...")
        QApplication.processEvents()

        try:
            summary = runner.run(file_path)
            self.status_label.setText(summary)
        except Exception as e:
            self.status_label.setText(f"Error: {e}")


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
