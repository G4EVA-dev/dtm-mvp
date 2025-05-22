# DTM Architecture

## Overview
DTM (Dependency Time Machine) is a developer tool for safe, intelligent dependency upgrades. It automates the process of testing all possible versions of a dependency to find the latest stable version that works with your codebase.

## Components

### 1. CLI (Node.js)
- User interface for developers
- Parses commands and config files
- Orchestrates the upgrade process
- Calls into the Python core logic

### 2. Core Logic (Python)
- Enumerates dependency versions
- Analyzes dependency graphs
- Orchestrates test runs (calls test runner)
- Implements binary search for breakage detection
- Returns results to CLI

### 3. Adapters
- Language/package manager plugins (e.g., pip, npm, cargo)
- Fetch available versions
- Install specific versions
- Run tests

### 4. Test Runner
- Runs tests in isolated environments (Docker/virtualenv)
- Returns pass/fail status

### 5. Cache
- Stores test results for (project, dependency, version) tuples
- Avoids redundant work

## Extensibility
- New language/package manager support can be added via adapters
- Test runner can be extended for new isolation methods

## Security
- Tests run in sandboxed environments
- Minimal privileges required
- Audit logs for compliance 