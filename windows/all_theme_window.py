from typing import Tuple

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)

from shared.konsave_interface import KonsaveInterface


class AllThemeWindow(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("All Themes")
        self.setFixedSize(610, 400)
        self.__konsave_interface = KonsaveInterface()
        self.themes: list[Tuple[int, str]] = self.__konsave_interface.get_profile_list()
        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)
        self.add_table()
        self.add_buttons()
        self.validate_buttons_state()

    def add_table(self) -> None:
        self.table_layout = QVBoxLayout()
        self.table_layout.setContentsMargins(20, 20, 20, 20)

        if not self.themes:
            label = QLabel("No Themes Found")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setStyleSheet("font-size: 16px; color: gray;")
            self.table_layout.addWidget(label)
            self.main_layout.insertLayout(0, self.table_layout)
            return

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setAlternatingRowColors(True)

        self.table.setHorizontalHeaderLabels(["Theme", "", "", ""])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setVisible(False)

        self.table.verticalHeader().setVisible(True)
        self.table.verticalHeader().setMinimumWidth(30)
        self.table.verticalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)

        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)

        self.table.setRowCount(len(self.themes))
        for row, (_, name) in enumerate(self.themes):
            self.table.setItem(row, 0, QTableWidgetItem(name))

            apply_btn = QPushButton("✅")
            apply_btn.setToolTip("Apply this theme")
            delete_btn = QPushButton("🗑️")
            delete_btn.setToolTip("Delete this theme")
            export_btn = QPushButton("📦")
            export_btn.setToolTip("Export this theme")

            apply_btn.clicked.connect(lambda _, n=name: self.apply_theme(n))
            delete_btn.clicked.connect(lambda _, n=name: self.delete_theme(n))
            export_btn.clicked.connect(lambda _, n=name: self.export_theme(n))

            self.table.setCellWidget(row, 1, apply_btn)
            self.table.setCellWidget(row, 2, delete_btn)
            self.table.setCellWidget(row, 3, export_btn)

        self.table.resizeColumnsToContents()
        self.table.setColumnWidth(1, 50)
        self.table.setColumnWidth(2, 50)
        self.table.setColumnWidth(3, 50)
        self.table_layout.addWidget(self.table)
        self.main_layout.insertLayout(0, self.table_layout)

    def add_buttons(self) -> None:
        buttons_height = 40
        buttons_width = 220
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(80)
        buttons_layout.setContentsMargins(20, 10, 20, 10)
        self.export_all_button = QPushButton("Export All")
        self.import_button = QPushButton("Import Theme")
        self.export_all_button.setMinimumSize(buttons_width, buttons_height)
        self.import_button.setMinimumSize(buttons_width, buttons_height)

        self.export_all_button.clicked.connect(self.export_all)
        self.import_button.clicked.connect(self.import_theme)

        buttons_layout.addWidget(self.export_all_button, alignment=Qt.AlignmentFlag.AlignHCenter)
        buttons_layout.addWidget(self.import_button, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.main_layout.addLayout(buttons_layout)

    def redraw_table(self) -> None:
        self.main_layout.removeItem(self.table_layout)
        self.table_layout.deleteLater()
        self.add_table()

    def validate_buttons_state(self) -> None:
        self.export_all_button.setEnabled(bool(self.themes))

    def export_all(self):
        QMessageBox.information(self, "Export Themes", "This feature is not implemented yet")

    def import_theme(self):
        QMessageBox.information(self, "Import Theme", "This feature is not implemented yet")

    def apply_theme(self, theme_name: str) -> None:
        try:
            self.__konsave_interface.apply_theme(theme_name)
            QMessageBox.information(
                self,
                "Theme Applied",
                f"Theme '{theme_name}' applied successfully.\nPlease logout and log back in to see the changes.",
            )
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to apply theme '{theme_name}'\nError: {e}")

    def delete_theme(self, theme_name: str) -> None:
        try:
            confirmation = QMessageBox.question(
                self,
                "Confirm Deletion",
                f"Are you sure you want to delete theme '{theme_name}'?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )
            if confirmation == QMessageBox.StandardButton.Yes:
                self.__konsave_interface.delete_theme(theme_name)
                self.themes = self.__konsave_interface.get_profile_list()
                self.redraw_table()
                QMessageBox.information(self, "Theme Deleted", f"Theme '{theme_name}' deleted successfully.")
                self.validate_buttons_state()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to delete theme '{theme_name}'\nError: {e}")

    def export_theme(self, theme_name: str) -> None:
        # TODO: this should be made asynchronous and show a spinnger while exporting as themes can be very large files
        try:
            confirmation = QMessageBox.question(
                self,
                "Confirm Export",
                f"Are you sure you want to export theme '{theme_name}'?\nWARNING: This might take a few minutes depending on the theme size!",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )
            if confirmation == QMessageBox.StandardButton.Yes:
                self.__konsave_interface.export_theme(theme_name)
                QMessageBox.information(self, "Theme Exported", f"Theme '{theme_name}' exported successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to export theme '{theme_name}'\nError: {e}")
