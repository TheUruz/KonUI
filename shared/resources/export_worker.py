import os
import shutil
import threading
import time
from codecs import ignore_errors

from PyQt6.QtCore import QObject, pyqtSignal

from shared.konsave_interface import KonsaveInterface
from shared.os_interface import OsInterface


class ExportWorker(QObject):
    progress = pyqtSignal(int)
    finished = pyqtSignal()
    failed = pyqtSignal(str)
    cancelled = pyqtSignal()

    def __init__(self, theme_name):
        super().__init__()
        self.theme_name = theme_name
        self._cancel = False
        self._files_present_before_work = OsInterface().get_current_files_in_working_directory()

    def cancel(self):
        self._cancel = True
        if self._process and self._process.poll() is None:
            self._process.terminate()
            self.cancelled.emit()
            self.remove_created_files()

    def run(self):
        try:
            progress = 0
            stop_flag = threading.Event()

            def simulate_progress():
                nonlocal progress
                while progress < 99 and not stop_flag.is_set():
                    if self._cancel:
                        stop_flag.set()
                        return
                    progress += 1
                    self.progress.emit(progress)
                    time.sleep(self.get_delay(progress))

            thread = threading.Thread(target=simulate_progress)
            thread.start()

            self._process = KonsaveInterface().export_theme(self.theme_name)
            _, stderr = self._process.communicate()

            stop_flag.set()
            thread.join()

            if self._cancel:
                return

            if self._process.returncode != 0:
                raise RuntimeError(stderr.decode().strip())

            self.progress.emit(100)
            self.finished.emit()

        except Exception as e:
            self.failed.emit(str(e))

    def get_delay(self, current_progress: int) -> float:
        base_wait = 0.8
        if current_progress < 50:
            return base_wait
        elif current_progress < 80:
            return base_wait * 2
        else:
            return base_wait * 3

    def remove_created_files(self) -> None:
        current_files = OsInterface().get_current_files_in_working_directory()
        created_files = current_files - self._files_present_before_work
        for file in created_files:
            path = os.path.join(os.getcwd(), file)
            try:
                if os.path.exists(path):
                    if os.path.isdir(path):
                        shutil.rmtree(path, ignore_errors=True)
                    elif os.path.isfile(path):
                        os.remove(path)
            except Exception as e:
                print(f"Errore durante la rimozione di '{path}': {e}")
