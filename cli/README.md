# Dependency Time Machine (DTM)

A powerful CLI tool that helps developers safely upgrade their project dependencies by automatically testing different versions and identifying breaking changes.

## Features

- 🔍 Automatically tests multiple versions of dependencies
- 🎯 Identifies the latest working version
- 🔄 Supports multiple languages:
  - Python
  - JavaScript/Node.js
  - Rust
- 🛡️ Prevents breaking changes in production
- 📊 Provides detailed upgrade reports

## Installation

```bash
npm install -g dtm-cli
```

## Usage

```bash
# Upgrade a specific package
dtm upgrade <package-name>

# Examples
dtm upgrade requests    # Python package
dtm upgrade lodash     # JavaScript package
dtm upgrade serde      # Rust package
```

## How It Works

1. DTM analyzes your project's dependencies
2. Tests multiple versions of the target package
3. Identifies the latest working version
4. Provides upgrade instructions

## Requirements

- Node.js >= 14.0.0
- Python 3.x (for Python package support)
- Rust (for Rust package support)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT © [Anchor] 