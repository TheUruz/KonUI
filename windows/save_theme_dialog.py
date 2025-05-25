from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QLabel, QLineEdit, QMessageBox, QPushButton, QVBoxLayout

from shared.konsave_interface import KonsaveInterface


class SaveThemeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Save Current Theme")
        self.setFixedSize(320, 180)
        self.__konsave_interface = KonsaveInterface()
        self.__placeholder_text = "Enter theme name..."
        self.__layout_margins = 20

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(
            self.__layout_margins, self.__layout_margins, self.__layout_margins, self.__layout_margins
        )

        self.input = QLineEdit()
        self.input.setFixedWidth(220)
        self.input.setMinimumHeight(35)
        self.input.setPlaceholderText(self.__placeholder_text)
        self.input.textChanged.connect(self.on_text_changed)

        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red;")
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.error_label.setMinimumHeight(15)

        self.confirm_button = QPushButton("Save Theme")
        self.confirm_button.setEnabled(False)
        self.confirm_button.setMinimumSize(150, 40)
        self.confirm_button.clicked.connect(self.accept)

        self.main_layout.addWidget(self.input, alignment=Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.error_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.confirm_button, alignment=Qt.AlignmentFlag.AlignCenter)

    def on_text_changed(self, text: str):
        existing_theme = self.__konsave_interface.get_existing(text)
        if existing_theme:
            self.error_label.setText(f"Theme already exists!\n(Found '{existing_theme[1]}')")
            # self.confirm_button.setEnabled(False)
        elif not text.strip():
            self.input.setStyleSheet("")
            self.error_label.setText("")
            self.input.setPlaceholderText(self.__placeholder_text)
            self.confirm_button.setEnabled(False)
        else:
            self.input.setStyleSheet("")
            self.error_label.setText("")
            self.confirm_button.setEnabled(True)

    def get_theme_name(self) -> str:
        return self.input.text().strip()

    def accept(self):
        existing_theme = self.__konsave_interface.get_existing(self.input.text())
        if existing_theme:
            reply = QMessageBox.warning(
                self,
                "Conflicting theme name",
                "Theme with selected name already exists.\nDo you want to overwrite it?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )
            if reply == QMessageBox.StandardButton.No:
                return
        super().accept()
