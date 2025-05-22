import subprocess
import json
from typing import List, Tuple

class RustAdapter:
    def __init__(self, package_name: str):
        self.package_name = package_name

    def enumerate_versions(self) -> List[str]:
        """Fetch all available versions from crates.io."""
        try:
            result = subprocess.run(
                ["cargo", "search", self.package_name, "--limit", "100", "--json"],
                check=True,
                capture_output=True,
                text=True
            )
            # Parse the JSON output from cargo search
            versions = []
            for line in result.stdout.splitlines():
                if line.strip():
                    try:
                        data = json.loads(line)
                        if data.get("name") == self.package_name:
                            versions.append(data["vers"])
                    except json.JSONDecodeError:
                        continue
            return sorted(versions, key=lambda s: [int(u) for u in s.split('.')])
        except Exception as e:
            print(f"Error fetching versions: {e}")
            return []

    def install_version(self, version: str) -> bool:
        """Install a specific version using Cargo."""
        try:
            # Update Cargo.toml with the specific version
            with open("Cargo.toml", "r") as f:
                content = f.read()
            
            # Replace or add the dependency
            dep_line = f'{self.package_name} = "{version}"'
            if f'"{self.package_name}"' in content:
                # Replace existing version
                import re
                content = re.sub(
                    f'{self.package_name} = "[^"]*"',
                    dep_line,
                    content
                )
            else:
                # Add new dependency
                content = content.replace(
                    "[dependencies]",
                    f"[dependencies]\n{dep_line}"
                )
            
            with open("Cargo.toml", "w") as f:
                f.write(content)

            # Run cargo update
            subprocess.run(
                ["cargo", "update", "-p", f"{self.package_name}"],
                check=True,
                capture_output=True,
                text=True
            )
            return True
        except Exception as e:
            print(f"Error installing version {version}: {e}")
            return False

    def run_tests(self, test_command: str = "cargo test") -> Tuple[bool, str]:
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