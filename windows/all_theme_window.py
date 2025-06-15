import subprocess
from pathlib import Path
from typing import Tuple

from PyQt6.QtCore import QEasingCurve, QPropertyAnimation, Qt, QThread
from PyQt6.QtGui import QFont, QIcon, QMovie
from PyQt6.QtWidgets import (
    QDialog,
    QFileDialog,
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

from shared.asset_interface import AssetInterface
from shared.config import Config
from shared.konsave_interface import KonsaveInterface
from shared.os_interface import OsInterface
from shared.resources.export_worker import ExportWorker
from shared.resources.import_worker import ImportWorker
from shared.resources.progress_bar_painter import ProgressBarPainter


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
        self.export_threads = {}
        self.export_progress = {}
        self.import_threads = {}
        self.custom_font = QFont()
        self.custom_font.setPointSize(10)
        self.setStyleSheet(Config.get_window_qss(Path(__file__)))
        self.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(40, 20, 40, 20)
        self.add_table_header()
        self.add_table()

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
        self.table.setColumnCount(4)
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(False)
        self.table.setItemDelegateForColumn(0, ProgressBarPainter(self.export_progress, self.table))

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
            export_btn.clicked.connect(lambda _, n=name, r=row: self.export_theme(n, r))

            self.table.setCellWidget(row, 1, apply_btn)
            self.table.setCellWidget(row, 2, delete_btn)
            self.table.setCellWidget(row, 3, export_btn)

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
        self.import_button = QPushButton("📥")
        self.import_button.setToolTip("Import a theme")

        self.search_toggle_btn.clicked.connect(self.toggle_searchbar)
        self.import_button.clicked.connect(self.import_theme)

        self.table_header_layout.addWidget(label)
        self.table_header_layout.addStretch()
        self.table_header_layout.addWidget(self.search_bar)
        self.table_header_layout.addWidget(self.search_toggle_btn)
        self.table_header_layout.addWidget(self.import_button)

        self.main_layout.addWidget(self.table_header_widget)

    def redraw_table(self) -> None:
        self.main_layout.removeWidget(self.table_widget)
        self.table_widget.deleteLater()
        self.table_widget = None
        self.add_table()

    def import_theme(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(self, "Select a profile file", "", "KNSV File (*.knsv)")
        theme_name = OsInterface().get_filename_without_extension(file_path)
        if not file_path:
            return
        if any(str(t[1]).lower() == theme_name.lower() for t in self.themes):
            QMessageBox.warning(
                self,
                "Existing theme",
                f"Theme '{theme_name}' already exists and cannot be imported.",
            )
            return

        self.import_spinner = QMovie(AssetInterface().get_spinner_path())
        self.import_spinner.start()
        self.import_button.setText("")
        self.import_button.setIcon(QIcon(self.import_spinner.currentPixmap()))
        self.import_button.setToolTip(f"Importing theme '{theme_name}'\nThis might take a few minutes...")
        self.import_spinner.frameChanged.connect(
            lambda: self.import_button.setIcon(QIcon(self.import_spinner.currentPixmap()))
        )
        self.import_button.clicked.disconnect()

        thread = QThread()
        import_worker = ImportWorker(file_path)
        import_worker.moveToThread(thread)
        thread.started.connect(import_worker.run)
        import_worker.finished.connect(self.on_import_finish)
        import_worker.finished.connect(thread.quit)
        import_worker.finished.connect(import_worker.deleteLater)
        thread.finished.connect(thread.deleteLater)
        self.import_threads[theme_name] = (thread, import_worker)
        thread.start()

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
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to delete theme '{theme_name}'\nError: {e}")

    def export_theme(self, theme_name: str, row_index: int) -> None:
        if row_index is None:
            row_index = next((i for i, (_, name) in enumerate(self.themes) if name == theme_name), -1)
        if row_index < 0:
            return

        btn = self.table.cellWidget(row_index, 3)
        if isinstance(btn, QPushButton) and btn.text() != "❌":
            btn.setText("❌")
            btn.setToolTip("Cancel export")
            btn.clicked.disconnect()
            btn.clicked.connect(lambda: self.cancel_export(row_index))

        self.toggle_table_operations_state(range(row_index, row_index + 1), [1, 2])

        worker = ExportWorker(theme_name)
        thread = QThread()
        worker.moveToThread(thread)

        worker.progress.connect(lambda val: self.update_progress(row_index, val))
        worker.finished.connect(lambda: self.export_finished(row_index))
        worker.failed.connect(lambda err: self.export_failed(row_index, err))
        worker.cancelled.connect(lambda: self.cleanup_export(row_index))
        thread.started.connect(worker.run)
        thread.finished.connect(thread.deleteLater)

        self.export_threads[row_index] = (thread, worker)
        self.export_progress[row_index] = 0
        self.table.viewport().update()

        thread.start()

    def filter_table(self, text: str) -> None:
        if not hasattr(self, "table") or self.table is None:
            return

        for row in range(self.table.rowCount()):
            item = self.table.item(row, 0)
            if item:
                self.table.setRowHidden(row, text.lower() not in item.text().lower())

    def toggle_searchbar(self) -> None:
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

    def reload_desktop_environment(self) -> None:
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

    def update_progress(self, row, value) -> None:
        self.export_progress[row] = value
        self.table.viewport().update()

    def export_finished(self, row) -> None:
        self.cleanup_export(row)
        QMessageBox.information(self, "Export Complete", f"Export completed for theme '{self.themes[row][1]}'")

    def export_failed(self, row, error) -> None:
        self.cleanup_export(row)
        QMessageBox.critical(self, "Export Failed", error)

    def cancel_export(self, row) -> None:
        _, worker = self.export_threads[row]
        worker.cancel()

    def cleanup_export(self, row) -> None:
        thread, worker = self.export_threads.pop(row, (None, None))
        self.export_progress.pop(row, None)
        if thread and thread.isRunning():
            thread.quit()
            thread.wait()

        model = self.table.model()
        model.dataChanged.emit(model.index(row, 0), model.index(row, model.columnCount() - 1))

        self.toggle_table_operations_state(range(self.table.rowCount()), [1, 2])
        export_btn = self.table.cellWidget(row, 3)
        if isinstance(export_btn, QPushButton):
            export_btn.setText("📦")
            export_btn.setToolTip("Export this theme")
            export_btn.clicked.disconnect()
            export_btn.clicked.connect(lambda _, n=self.themes[row][1], r=row: self.export_theme(n, r))

    def on_import_finish(self) -> None:
        self.themes = self.__konsave_interface.get_profile_list()

        self.import_spinner.stop()
        self.import_spinner.deleteLater()
        self.import_spinner = None
        self.import_button.setIcon(QIcon())

        self.import_button.setText("📥")
        self.import_button.setToolTip("Import a theme")
        self.import_button.clicked.connect(self.import_theme)
        QMessageBox.information(
            self,
            "Theme Import",
            f"Theme imported successfully",
        )

        self.redraw_table()

    def toggle_table_operations_state(self, rows_to_disable: range, column_to_disable: list[int]) -> None:
        for row in rows_to_disable:
            if row not in self.export_threads.keys():
                for column in column_to_disable:
                    widget = self.table.cellWidget(row, column)
                    if isinstance(widget, QPushButton):
                        widget.setEnabled(not widget.isEnabled())

    # Qt override. do not rename this method
    def closeEvent(self, event) -> None:
        active_threads = [t for t, _ in self.export_threads.values() if t.isRunning()]
        if not active_threads:
            event.accept()
            return

        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowTitle("Export in progress")
        msg.setText("I am still exporting themes.\nWhat do you want to do?")
        terminate_btn = msg.addButton("Terminate exports", QMessageBox.ButtonRole.AcceptRole)
        # let_run_btn = msg.addButton("Close without terminate", QMessageBox.ButtonRole.DestructiveRole)
        _ = msg.addButton("Cancel closure", QMessageBox.ButtonRole.RejectRole)
        msg.exec()

        clicked = msg.clickedButton()
        if clicked == terminate_btn:
            for thread, worker in list(self.export_threads.values()):
                if thread.isRunning():
                    worker.cancel()
                    thread.quit()
                    thread.wait()
            self.export_threads.clear()
            self.export_progress.clear()
            event.accept()
        # elif clicked == let_run_btn:
        #     event.accept()
        else:
            event.ignore()
