import os
import subprocess


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
            subprocess.run(["konsave", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            return True
        except (FileNotFoundError, subprocess.CalledProcessError):
            return False

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
