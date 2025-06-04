import subprocess
import sys

from PyQt6.QtWidgets import QApplication, QMessageBox

from shared.os_interface import OsInterface
from windows.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    if not OsInterface.check_konsave_installed():
        QMessageBox.critical(
            None, "Konsave not found", "Konsave has not been found on your system. Please install it to use this UI"
        )
        sys.exit(1)
    finestra = MainWindow()
    finestra.show()
    sys.exit(app.exec())
