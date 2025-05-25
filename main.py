import subprocess
import sys

from PyQt6.QtWidgets import QApplication, QMessageBox

from windows.main_window import MainWindow


def check_konsave_installed() -> bool:
    try:
        subprocess.run(["konsave", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    if not check_konsave_installed():
        QMessageBox.critical(
            None, "Konsave not found", "Konsave has not been found on your system. Please install it to use this UI"
        )
        sys.exit(1)
    finestra = MainWindow()
    finestra.show()
    sys.exit(app.exec())
