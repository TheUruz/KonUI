from pathlib import Path
from typing import Optional

_CONFIG = {"app_name": "KonUI", "QSS_directory": "QSS", "cache_files": {"last_applied_theme": "last_applied_theme.txt"}}


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

    @staticmethod
    def get_cache_file(key: str) -> Optional[str]:
        return _CONFIG["cache_files"].get(key)
