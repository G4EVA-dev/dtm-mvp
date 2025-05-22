import sys
import json
import os
from typing import List, Tuple, Optional, Dict
from adapters.python_adapter import PythonAdapter
from adapters.js_adapter import JSAdapter
from adapters.rust_adapter import RustAdapter

def detect_language() -> str:
    """Detect the project language based on files present."""
    if os.path.exists("package.json"):
        return "js"
    elif os.path.exists("Cargo.toml"):
        return "rust"
    elif os.path.exists("requirements.txt") or os.path.exists("setup.py"):
        return "python"
    return "python"  # Default to Python for now

def get_adapter(package_name: str, language: str):
    """Get the appropriate adapter for the language."""
    if language == "js":
        return JSAdapter(package_name)
    elif language == "rust":
        return RustAdapter(package_name)
    return PythonAdapter(package_name)

def get_test_command(language: str) -> str:
    """Get the default test command for the language."""
    if language == "js":
        return "npm test"
    elif language == "rust":
        return "cargo test"
    return "pytest"

def binary_search_versions(versions: List[str], adapter, test_command: str) -> Tuple[Optional[str], Optional[str], Optional[Dict]]:
    """Find the latest working version using binary search."""
    if not versions:
        return None, None, None

    left, right = 0, len(versions) - 1
    latest_working = None
    first_broken = None
    dependency_conflicts = None

    while left <= right:
        mid = (left + right) // 2
        version = versions[mid]
        print(f"\nTesting version {version}...")

        if adapter.install_version(version):
            success, output = adapter.run_tests(test_command)
            if success:
                print(f"✅ Version {version} works!")
                latest_working = version
                left = mid + 1
            else:
                print(f"❌ Version {version} failed!")
                first_broken = version
                right = mid - 1
        else:
            print(f"❌ Failed to install version {version}")
            first_broken = version
            # Check for dependency conflicts
            if hasattr(adapter, 'get_dependency_conflicts'):
                conflicts = adapter.get_dependency_conflicts(version)
                if conflicts:
                    dependency_conflicts = conflicts
                    print("\n🔍 Dependency conflicts detected:")
                    for package, issues in conflicts.items():
                        print(f"  - {package}:")
                        for issue in issues:
                            print(f"    {issue}")
            right = mid - 1

    return latest_working, first_broken, dependency_conflicts

def main():
    if len(sys.argv) < 3 or sys.argv[1] != 'upgrade':
        print("Usage: python main.py upgrade <package-name>")
        sys.exit(1)

    package_name = sys.argv[2]
    language = detect_language()
    adapter = get_adapter(package_name, language)

    print(f"\n🔍 Analyzing {package_name} for {language}...")
    versions = adapter.enumerate_versions()
    
    if not versions:
        print("❌ No versions found!")
        sys.exit(1)

    print(f"\n📦 Found {len(versions)} versions")
    print(f"Versions: {', '.join(versions)}")

    # Get test command from config or use default
    test_command = get_test_command(language)
    
    print("\n🔬 Starting binary search for latest working version...")
    latest_working, first_broken, dependency_conflicts = binary_search_versions(versions, adapter, test_command)

    print("\n📊 Results:")
    if latest_working:
        print(f"✅ Latest working version: {latest_working}")
    if first_broken:
        print(f"❌ First broken version: {first_broken}")
    if dependency_conflicts:
        print("\n⚠️ Dependency conflicts found:")
        for package, issues in dependency_conflicts.items():
            print(f"  - {package}:")
            for issue in issues:
                print(f"    {issue}")

    # Output JSON for CLI to parse
    result = {
        "package": package_name,
        "language": language,
        "latest_working": latest_working,
        "first_broken": first_broken,
        "dependency_conflicts": dependency_conflicts,
        "total_versions": len(versions)
    }
    print("\n" + json.dumps(result))

if __name__ == "__main__":
    main() 