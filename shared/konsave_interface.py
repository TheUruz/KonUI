import subprocess
from typing import Tuple


class KonsaveInterface:

    def get_existing(self, theme_name: str) -> Tuple[int, str] | None:
        comparison_name = theme_name.strip().lower()
        for t in self.get_profile_list():
            if t[1].strip().lower() == comparison_name:
                return t
        return None

    def get_profile_list(self) -> list[Tuple[int, str]]:
        process_result = subprocess.run(["konsave", "-l"], capture_output=True, text=True, check=True)
        output = process_result.stdout.strip().splitlines()
        profiles: list[Tuple[int, str]] = []
        for p in output:
            parts = p.split("\t")
            if len(parts) == 2 and parts[0].isdigit():
                profiles.append((int(parts[0]), parts[1]))

        # Validate integrity
        indexes = [t[0] for t in profiles]
        if not indexes == list(range(1, len(indexes) + 1)):
            raise ValueError("Cannot read all saved themes from Konsave")
        return profiles

    def save_theme(self, theme_name: str) -> None:
        subprocess.run(["konsave", "-s", theme_name, "-f"], check=True)

    def apply_theme(self, theme_name: str) -> None:
        subprocess.run(["konsave", "-a", theme_name], check=True)

    def delete_theme(self, theme_name: str) -> None:
        subprocess.run(["konsave", "-r", theme_name], check=True)

    def export_theme(self, theme_name: str) -> None:
        subprocess.run(["konsave", "-e", theme_name], check=True)
