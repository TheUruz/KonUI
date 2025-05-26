from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox, QPushButton, QSizePolicy, QVBoxLayout, QWidget

from shared.config import Config
from shared.konsave_interface import KonsaveInterface
from windows.all_theme_window import AllThemeWindow
from windows.save_theme_dialog import SaveThemeDialog


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.__konsave_interface = KonsaveInterface()
        self.__buttons_width = 200
        self.__buttons_height = 50

        self.setWindowTitle(Config.get_app_name())
        self.setFixedSize(400, 240)

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(50, 50, 50, 50)
        self.main_layout.setSpacing(40)

        self.all_themes_button = QPushButton("All Themes")
        self.all_themes_button.setToolTip("View all available themes")
        self.all_themes_button.setMinimumSize(self.__buttons_width, self.__buttons_height)
        self.all_themes_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.all_themes_button.clicked.connect(self.open_all_themes_dialog)

        self.save_current_theme_button = QPushButton("Save Current Theme")
        self.save_current_theme_button.setToolTip("Save current set of configuration into a theme")
        self.save_current_theme_button.setMinimumSize(self.__buttons_width, self.__buttons_height)
        self.save_current_theme_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.save_current_theme_button.clicked.connect(self.open_save_theme_dialog)

        self.main_layout.addWidget(self.all_themes_button, alignment=Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.save_current_theme_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(self.main_layout)

    def open_save_theme_dialog(self):
        dialog = SaveThemeDialog(self)
        if dialog.exec():
            theme_name = dialog.get_theme_name()
            self.__konsave_interface.save_theme(theme_name)
            print("-> THEME SAVED: {theme_name}".format(theme_name=theme_name))
            QMessageBox.information(self, "Theme Saved", f"Theme '{theme_name}' has been saved successfully.")

    def open_all_themes_dialog(self):
        themes = self.__konsave_interface.get_profile_list()
        dialog = AllThemeWindow(self, themes)
        dialog.exec()
