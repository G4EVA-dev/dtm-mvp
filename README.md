# Dependency Time Machine (DTM)

A developer tool for safe, intelligent dependency upgrades. DTM automatically tests all possible versions of a library against your codebase to find the newest stable version that works, using binary search, sandboxed testing, and dependency graph analysis.

## Features

- 🔍 Automatically detects project language (Python, JavaScript, Rust)
- 📦 Fetches all available versions of a dependency
- 🔬 Uses binary search to efficiently find breaking changes
- ✅ Tests each version in isolation
- 📊 Provides clear upgrade recommendations
- 🔒 Safe and reliable dependency upgrades

## Installation

```bash
npm install -g dependency-time-machine
```

## Prerequisites

- Node.js >= 14.0.0
- Python 3.x (for Python projects)
- npm (for JavaScript projects)
- Cargo (for Rust projects)

## Usage

```bash
# Basic usage
dtm upgrade <package-name>

# Examples
dtm upgrade requests    # For Python projects
dtm upgrade lodash     # For JavaScript projects
dtm upgrade serde      # For Rust projects
```

## Example Projects

Check out the `examples/` directory for sample projects in each supported language:

- `examples/python-example/`: Python project using requests
- `examples/js-example/`: JavaScript project using lodash
- `examples/rust-example/`: Rust project using serde

## How It Works

1. DTM detects your project's language
2. Fetches all available versions of the target dependency
3. Uses binary search to efficiently find the latest working version
4. Tests each version in isolation
5. Provides a detailed report with upgrade instructions

## Supported Languages

- Python (pip)
- JavaScript (npm)
- Rust (Cargo)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT
