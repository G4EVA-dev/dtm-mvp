import subprocess
import json
import requests
import os
import sys
from typing import List, Tuple, Dict, Optional

class PythonAdapter:
    def __init__(self, package_name: str):
        self.package_name = package_name
        self.pypi_url = f"https://pypi.org/pypi/{package_name}/json"
        self.venv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "venv")
        self._ensure_venv()

    def _ensure_venv(self):
        """Ensure virtual environment exists and is properly set up."""
        if not os.path.exists(self.venv_path):
            subprocess.run([sys.executable, "-m", "venv", self.venv_path], check=True)
            # Install requirements
            requirements_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "requirements.txt")
            if os.path.exists(requirements_path):
                subprocess.run([
                    os.path.join(self.venv_path, "bin", "pip"),
                    "install",
                    "-r",
                    requirements_path
                ], check=True)

    def _get_pip_path(self) -> str:
        """Get the path to pip in the virtual environment."""
        if sys.platform == "win32":
            return os.path.join(self.venv_path, "Scripts", "pip")
        return os.path.join(self.venv_path, "bin", "pip")

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
        """Install a specific version using pip in the virtual environment."""
        try:
            # First, uninstall any existing version
            subprocess.run(
                [self._get_pip_path(), "uninstall", "-y", self.package_name],
                check=False,
                capture_output=True,
                text=True
            )
            
            # Install the specific version
            result = subprocess.run(
                [self._get_pip_path(), "install", f"{self.package_name}=={version}"],
                check=True,
                capture_output=True,
                text=True
            )
            
            # Check for dependency conflicts
            if "ERROR: pip's dependency resolver" in result.stderr:
                print(f"Warning: Dependency conflicts detected for {self.package_name} {version}")
                return False
                
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error installing version {version}: {e.stderr}")
            return False

    def run_tests(self, test_command: str = "pytest") -> Tuple[bool, str]:
        """Run tests in the virtual environment."""
        try:
            # Activate virtual environment and run tests
            if sys.platform == "win32":
                python_path = os.path.join(self.venv_path, "Scripts", "python")
            else:
                python_path = os.path.join(self.venv_path, "bin", "python")
                
            result = subprocess.run(
                [python_path, "-m"] + test_command.split(),
                check=True,
                capture_output=True,
                text=True
            )
            return True, result.stdout
        except subprocess.CalledProcessError as e:
            return False, e.stderr

    def get_dependency_conflicts(self, version: str) -> Optional[Dict[str, List[str]]]:
        """Get dependency conflicts for a specific version."""
        try:
            result = subprocess.run(
                [self._get_pip_path(), "install", f"{self.package_name}=={version}"],
                check=False,
                capture_output=True,
                text=True
            )
            
            if "ERROR: pip's dependency resolver" in result.stderr:
                # Parse the error message to extract conflicts
                conflicts = {}
                current_package = None
                for line in result.stderr.split('\n'):
                    if "requires" in line and "but you have" in line:
                        parts = line.split()
                        if len(parts) >= 4:
                            package = parts[0]
                            required = parts[2]
                            current = parts[-1]
                            if package not in conflicts:
                                conflicts[package] = []
                            conflicts[package].append(f"requires {required} but you have {current}")
                return conflicts
            return None
        except Exception as e:
            print(f"Error checking dependencies: {e}")
            return None 