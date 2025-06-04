import subprocess
from pathlib import Path
from typing import Tuple

from PyQt6.QtCore import QEasingCurve, QPropertyAnimation, Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from shared.config import Config
from shared.konsave_interface import KonsaveInterface
from shared.os_interface import OsInterface


class AllThemeWindow(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("All Themes")
        self.setFixedSize(610, 400)
        self.__konsave_interface = KonsaveInterface()
        self.themes: list[Tuple[int, str]] = self.__konsave_interface.get_profile_list()
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.action_buttons_side = 35
        self.custom_font = QFont()
        self.custom_font.setPointSize(10)
        self.setStyleSheet(Config.get_window_qss(Path(__file__)))
        self.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(40, 20, 40, 20)
        self.add_table_header()
        self.add_table()
        self.validate_buttons_state()

    def add_table(self) -> None:
        self.table_widget = QWidget()
        self.table_widget.setObjectName("TableContentWidget")
        self.table_layout = QVBoxLayout(self.table_widget)

        if not self.themes:
            label = QLabel("No Themes Found")
            label.setObjectName("NotFoundLabel")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table_layout.addWidget(label, stretch=1)
            self.main_layout.insertWidget(1, self.table_widget)
            return

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(False)

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
            apply_btn.setObjectName("TableButton")
            delete_btn = QPushButton("🗑️")
            delete_btn.setToolTip("Delete this theme")
            delete_btn.setObjectName("TableButton")
            export_btn = QPushButton("📦")
            export_btn.setToolTip("Export this theme")
            export_btn.setObjectName("TableButton")

            apply_btn.clicked.connect(lambda _, n=name: self.apply_theme(n))
            delete_btn.clicked.connect(lambda _, n=name: self.delete_theme(n))
            export_btn.clicked.connect(lambda _, n=name: self.export_theme(n))

            self.table.setCellWidget(row, 1, apply_btn)
            self.table.setCellWidget(row, 2, delete_btn)
            # self.table.setCellWidget(row, 3, export_btn)

        self.table.resizeColumnsToContents()
        button_columns_width = 20
        self.table.setColumnWidth(1, button_columns_width)
        self.table.setColumnWidth(2, button_columns_width)
        self.table.setColumnWidth(3, button_columns_width)
        self.table_layout.addWidget(self.table, stretch=1)
        self.main_layout.insertWidget(1, self.table_widget)

    def add_table_header(self) -> None:
        self.table_header_widget = QWidget()
        self.table_header_widget.setObjectName("TableHeaderWidget")
        self.table_header_layout = QHBoxLayout(self.table_header_widget)

        label = QLabel("Themes")
        label.setStyleSheet("font-weight: bold; font-size: 16px;")

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search theme...")
        self.search_bar.textChanged.connect(self.filter_table)
        self.search_bar.setFixedWidth(0)

        self.searchbar_animation = QPropertyAnimation(self.search_bar, b"minimumWidth")
        self.searchbar_animation.setDuration(300)
        self.searchbar_animation.setEasingCurve(QEasingCurve.Type.OutCubic)

        self.search_toggle_btn = QPushButton("🔍")
        self.export_all_button = QPushButton("📤")
        self.import_button = QPushButton("📥")

        self.export_all_button.setToolTip("Export all themes")
        self.import_button.setToolTip("Import a theme")

        self.search_toggle_btn.clicked.connect(self.toggle_searchbar)
        self.export_all_button.clicked.connect(self.export_all)
        self.import_button.clicked.connect(self.import_theme)

        self.table_header_layout.addWidget(label)
        self.table_header_layout.addStretch()
        self.table_header_layout.addWidget(self.search_bar)
        self.table_header_layout.addWidget(self.search_toggle_btn)
        # self.table_header_layout.addWidget(self.export_all_button)
        # self.table_header_layout.addWidget(self.import_button)

        self.main_layout.addWidget(self.table_header_widget)

    def redraw_table(self) -> None:
        self.main_layout.removeItem(self.table_layout)
        self.table_layout.deleteLater()
        self.add_table()

    def validate_buttons_state(self) -> None:
        self.export_all_button.setEnabled(bool(self.themes))

    def export_all(self) -> None:
        QMessageBox.information(self, "Export Themes", "This feature is not implemented yet")

    def import_theme(self) -> None:
        QMessageBox.information(self, "Import Theme", "This feature is not implemented yet")

    def apply_theme(self, theme_name: str) -> None:
        try:
            self.__konsave_interface.apply_theme(theme_name)
            systemd_installed = OsInterface().check_systemd_installed()
            if systemd_installed:
                try_apply = QMessageBox.question(
                    self,
                    "Try Apply Immediately?",
                    f"I can try to update to the selected theme right away.\nWould you like me to do that now?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                )
                if try_apply == QMessageBox.StandardButton.Yes:
                    self.reload_desktop_environment()
                    QMessageBox.information(
                        self,
                        "Theme Applied",
                        f"Theme '{theme_name}' applied successfully.\nSome changes might still require a relog to take full effect",
                    )
                    return
            QMessageBox.information(
                self,
                "Theme Applied",
                f"Theme '{theme_name}' applied successfully.\nPlease logout and log back in to see the changes",
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

    def filter_table(self, text: str) -> None:
        if not hasattr(self, "table") or self.table is None:
            return

        for row in range(self.table.rowCount()):
            item = self.table.item(row, 0)
            if item:
                self.table.setRowHidden(row, text.lower() not in item.text().lower())

    def toggle_searchbar(self):
        expanded = self.search_bar.width() > 0
        target_width = 250 if not expanded else 0

        self.searchbar_animation.stop()
        self.searchbar_animation.setStartValue(self.search_bar.width())
        self.searchbar_animation.setEndValue(target_width)
        self.searchbar_animation.start()

        if expanded:
            self.search_toggle_btn.setText("🔍")
            self.search_bar.clear()
            self.filter_table("")
        else:
            self.search_toggle_btn.setText("❌")
            self.search_bar.setFocus()

    def reload_desktop_environment(self):
        subprocess.run(["systemctl", "--user", "restart", "plasma-plasmashell.service"], check=True)
        de_protocol = OsInterface().get_de_protocol()

        if de_protocol == "X11":
            plasmashell_version = OsInterface().get_plasmashell_version()
            if plasmashell_version not in ("5", "6"):
                raise ValueError(f"Can't reload desktop environment because of an unsupported plasmashell version")
            if plasmashell_version == "5":
                subprocess.run([f"kquitapp5", "kwin_x11"], check=True)
                subprocess.run(["kstart5", "kwin_x11"], check=True)
            elif plasmashell_version == "6":
                subprocess.run([f"kquitapp6", "kwin_x11"], check=True)
                subprocess.run(["kstart", "kwin_x11"], check=True)
