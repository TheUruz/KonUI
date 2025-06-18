import os
import re
import subprocess
from typing import Optional


class OsInterface:

    @staticmethod
    def check_systemd_installed() -> bool:
        try:
            subprocess.run(["systemctl", "--version"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    @staticmethod
    def check_konsave_installed() -> bool:
        try:
            konsave_version = OsInterface().get_kosnave_version()
            return True if konsave_version else False
        except (FileNotFoundError, subprocess.CalledProcessError):
            return False

    @staticmethod
    def get_kosnave_version() -> Optional[str]:
        try:
            output = subprocess.run(["konsave", "--version"], text=True, capture_output=True)
            konsave_version = re.search(r"(\d+\.\d+\.\d+)", output.stdout)
            return konsave_version.group(1) if konsave_version else None
        except (FileNotFoundError, subprocess.CalledProcessError):
            return None

    @staticmethod
    def get_de_protocol() -> str:
        return os.environ.get("XDG_SESSION_TYPE", "").capitalize()

    @staticmethod
    def get_plasmashell_version() -> str:
        try:
            output = subprocess.check_output(["plasmashell", "--version"], text=True)
            for line in output.splitlines():
                if "plasmashell" in line.lower():
                    parts = line.strip().split()
                    for part in parts:
                        if part[0].isdigit():
                            return part
        except Exception as e:
            print(f"Could not read plasmashell version. Error: {e}")
        return "unknown"

    @staticmethod
    def get_current_files_in_working_directory() -> set:
        try:
            return set(os.listdir(os.getcwd()))
        except Exception as e:
            print(f"Could not list files in current working directory. Error: {e}")
            return set()

    @staticmethod
    def get_filename_without_extension(file_path) -> str:
        return os.path.splitext(os.path.basename(file_path))[0]
