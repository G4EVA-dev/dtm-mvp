import subprocess
import json
import requests
from typing import List, Tuple

class PythonAdapter:
    def __init__(self, package_name: str):
        self.package_name = package_name
        self.pypi_url = f"https://pypi.org/pypi/{package_name}/json"

    def enumerate_versions(self) -> List[str]:
        """Fetch all available versions from PyPI."""
        try:
            response = requests.get(self.pypi_url)
            response.raise_for_status()
            data = response.json()
            versions = list(data["releases"].keys())
            # Sort versions semantically
            versions.sort(key=lambda s: [int(u) for u in s.split('.')])
            return versions
        except Exception as e:
            print(f"Error fetching versions: {e}")
            return []

    def install_version(self, version: str) -> bool:
        """Install a specific version using pip."""
        try:
            subprocess.run(
                ["pip", "install", f"{self.package_name}=={version}"],
                check=True,
                capture_output=True,
                text=True
            )
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error installing version {version}: {e.stderr}")
            return False

    def run_tests(self, test_command: str = "pytest") -> Tuple[bool, str]:
        """Run tests and return (success, output)."""
        try:
            result = subprocess.run(
                test_command.split(),
                check=True,
                capture_output=True,
                text=True
            )
            return True, result.stdout
        except subprocess.CalledProcessError as e:
            return False, e.stderr 