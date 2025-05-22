import subprocess
import json
from typing import List, Tuple

class JSAdapter:
    def __init__(self, package_name: str):
        self.package_name = package_name

    def enumerate_versions(self) -> List[str]:
        """Fetch all available versions from npm."""
        try:
            result = subprocess.run(
                ["npm", "view", self.package_name, "versions", "--json"],
                check=True,
                capture_output=True,
                text=True
            )
            versions = json.loads(result.stdout)
            return versions
        except Exception as e:
            print(f"Error fetching versions: {e}")
            return []

    def install_version(self, version: str) -> bool:
        """Install a specific version using npm."""
        try:
            subprocess.run(
                ["npm", "install", f"{self.package_name}@{version}"],
                check=True,
                capture_output=True,
                text=True
            )
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error installing version {version}: {e.stderr}")
            return False

    def run_tests(self, test_command: str = "npm test") -> Tuple[bool, str]:
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