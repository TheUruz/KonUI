from pathlib import Path

_CONFIG = {"app_name": "KonUI", "QSS_directory": "QSS"}


class Config:
    @staticmethod
    def get_app_name():
        return _CONFIG["app_name"]

    @staticmethod
    def get_window_qss(filepath: Path) -> str:
        try:
            window_name = filepath.stem
            qss_folder_path = Path().cwd() / _CONFIG["QSS_directory"]
            with open(qss_folder_path / f"{window_name}.qss", "r") as file:
                return file.read()
        except FileNotFoundError:
            print(f"QSS file for window '{window_name}' not found")
            return ""
