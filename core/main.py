import sys
import json
import os
import re
from typing import List, Tuple, Optional, Dict, Set
from adapters.python_adapter import PythonAdapter
from adapters.js_adapter import JSAdapter
from adapters.rust_adapter import RustAdapter

def parse_requirements_file(file_path: str) -> Set[str]:
    """Parse requirements.txt file and return set of package names."""
    packages = set()
    try:
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    # Extract package name (remove version specifiers)
                    package = re.split(r'[=<>!~]', line)[0].strip()
                    packages.add(package)
    except FileNotFoundError:
        pass
    return packages

def parse_package_json(file_path: str) -> Set[str]:
    """Parse package.json file and return set of package names."""
    packages = set()
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            # Get dependencies from both dependencies and devDependencies
            for deps in [data.get('dependencies', {}), data.get('devDependencies', {})]:
                packages.update(deps.keys())
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    return packages

def parse_cargo_toml(file_path: str) -> Set[str]:
    """Parse Cargo.toml file and return set of package names."""
    packages = set()
    try:
        with open(file_path, 'r') as f:
            for line in f:
                # Look for dependencies section
                if line.strip().startswith('[') and 'dependencies' in line:
                    in_deps = True
                    continue
                if in_deps and line.strip().startswith('['):
                    in_deps = False
                    continue
                if in_deps and '=' in line:
                    package = line.split('=')[0].strip()
                    packages.add(package)
    except FileNotFoundError:
        pass
    return packages

def detect_dependencies() -> Dict[str, Set[str]]:
    """Detect all dependencies in the project."""
    dependencies = {
        'python': parse_requirements_file('requirements.txt'),
        'js': parse_package_json('package.json'),
        'rust': parse_cargo_toml('Cargo.toml')
    }
    return dependencies

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

def analyze_package(package_name: str, language: str) -> Dict:
    """Analyze a single package and return results."""
    adapter = get_adapter(package_name, language)
    test_command = get_test_command(language)

    print(f"\n🔍 Analyzing {package_name} for {language}...")
    versions = adapter.enumerate_versions()
    
    if not versions:
        return {
            "package": package_name,
            "status": "error",
            "message": "No versions found"
        }

    print(f"\n📦 Found {len(versions)} versions")
    latest_working, first_broken, dependency_conflicts = binary_search_versions(versions, adapter, test_command)

    return {
        "package": package_name,
        "status": "success",
        "latest_working": latest_working,
        "first_broken": first_broken,
        "dependency_conflicts": dependency_conflicts,
        "total_versions": len(versions)
    }

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
    if len(sys.argv) < 2:
        print("Usage: python main.py [upgrade <package-name> | analyze]")
        sys.exit(1)

    if sys.argv[1] == 'analyze':
        # Analyze all dependencies
        print("🔍 Analyzing project dependencies...")
        dependencies = detect_dependencies()
        
        results = {}
        for language, packages in dependencies.items():
            if packages:
                print(f"\n📦 Found {len(packages)} {language} dependencies:")
                for package in packages:
                    print(f"  - {package}")
                
                print(f"\n🔬 Analyzing {language} dependencies...")
                for package in packages:
                    result = analyze_package(package, language)
                    results[package] = result

        # Output results
        print("\n📊 Analysis Results:")
        for package, result in results.items():
            print(f"\n{package}:")
            if result["status"] == "success":
                if result["latest_working"]:
                    print(f"  ✅ Latest working version: {result['latest_working']}")
                if result["first_broken"]:
                    print(f"  ❌ First broken version: {result['first_broken']}")
                if result["dependency_conflicts"]:
                    print("  ⚠️ Dependency conflicts found:")
                    for dep, issues in result["dependency_conflicts"].items():
                        print(f"    - {dep}:")
                        for issue in issues:
                            print(f"      {issue}")
            else:
                print(f"  ❌ {result['message']}")

        # Output JSON for CLI to parse
        print("\n" + json.dumps(results))

    elif sys.argv[1] == 'upgrade':
        if len(sys.argv) < 3:
            print("Usage: python main.py upgrade <package-name>")
            sys.exit(1)

        package_name = sys.argv[2]
        language = detect_language()
        result = analyze_package(package_name, language)
        print("\n" + json.dumps(result))

    else:
        print("Unknown command. Use 'analyze' or 'upgrade <package-name>'")
        sys.exit(1)

if __name__ == "__main__":
    main() 