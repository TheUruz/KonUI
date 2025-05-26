from typing import Tuple

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QHeaderView,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)


class AllThemeWindow(QDialog):
    def __init__(self, parent, themes: list[Tuple[int, str]]):
        super().__init__(parent)
        self.setWindowTitle("All Themes")
        self.setFixedSize(610, 400)
        self.themes = themes
        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)
        self.add_table()
        self.add_buttons()

    def export_all(self):
        QMessageBox.information(self, "Export Themes", "This feature is not implemented yet")

    def import_theme(self):
        QMessageBox.information(self, "Import Theme", "This feature is not implemented yet")

    def add_table(self) -> None:
        self.table_layout = QVBoxLayout()
        self.table_layout.setContentsMargins(20, 20, 20, 20)
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

            apply_btn.clicked.connect(
                lambda _, n=name: QMessageBox.information(self, "Apply Theme", "This feature is not implemented yet")
            )
            delete_btn.clicked.connect(
                lambda _, n=name: QMessageBox.information(self, "Delete Theme", "This feature is not implemented yet")
            )
            export_btn.clicked.connect(
                lambda _, n=name: QMessageBox.information(self, "Export Theme", "This feature is not implemented yet")
            )

            self.table.setCellWidget(row, 1, apply_btn)
            self.table.setCellWidget(row, 2, delete_btn)
            self.table.setCellWidget(row, 3, export_btn)

        self.table.resizeColumnsToContents()
        self.table.setColumnWidth(1, 50)
        self.table.setColumnWidth(2, 50)
        self.table.setColumnWidth(3, 50)
        self.table_layout.addWidget(self.table)
        self.main_layout.addLayout(self.table_layout)

    def add_buttons(self) -> None:
        buttons_height = 40
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(80)
        buttons_layout.setContentsMargins(20, 10, 20, 10)
        self.export_all_button = QPushButton("Export All")
        self.export_all_button.setMinimumHeight(buttons_height)
        self.import_button = QPushButton("Import Theme")
        self.import_button.setMinimumHeight(buttons_height)

        self.export_all_button.clicked.connect(self.export_all)
        self.import_button.clicked.connect(self.import_theme)

        buttons_layout.addWidget(self.export_all_button)
        buttons_layout.addWidget(self.import_button)

        self.main_layout.addLayout(buttons_layout)
