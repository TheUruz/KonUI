from PyQt6.QtCore import QObject, pyqtSignal

from shared.konsave_interface import KonsaveInterface


class ImportWorker(QObject):
    finished = pyqtSignal()

    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path

    def run(self):
        KonsaveInterface().import_theme(self.file_path)
        self.finished.emit()
