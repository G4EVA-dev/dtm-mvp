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

### Prerequisites

- Node.js >= 14.0.0
- Python 3.x (for Python package support)
- Rust (for Rust package support)

### Global Installation

```bash
npm install -g dep-time-machine
```

### Local Development

```bash
# Clone the repository
git clone https://github.com/G4EVA-dev/dtm-mvp.git
cd dtm-mvp/cli

# Install dependencies
npm install

# Link for local development
npm link
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

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT © EricBlak and Glennzy 