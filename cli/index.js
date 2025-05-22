#!/usr/bin/env node

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const pkg = require('./package.json');

function printHelp() {
  console.log(`Dependency Time Machine (DTM) v${pkg.version}
A developer tool for safe, intelligent dependency upgrades.

Usage:
  dtm <command> [options]

Commands:
  upgrade <dependency>   Test and upgrade a dependency safely
  help                  Show this help message
  version               Show version info

Examples:
  dtm upgrade requests  # For Python projects
  dtm upgrade lodash    # For JavaScript projects
`);
}

function parseResults(output) {
  try {
    // Find the last line that's valid JSON
    const lines = output.split('\n');
    for (let i = lines.length - 1; i >= 0; i--) {
      try {
        return JSON.parse(lines[i]);
      } catch (e) {
        continue;
      }
    }
  } catch (e) {
    console.error('Error parsing results:', e);
  }
  return null;
}

function displayResults(results) {
  if (!results) {
    console.error('❌ Failed to get results');
    return;
  }

  console.log('\n📊 Dependency Time Machine Results');
  console.log('==================================');
  console.log(`Package: ${results.package}`);
  console.log(`Language: ${results.language}`);
  console.log(`Total versions analyzed: ${results.total_versions}`);
  
  if (results.latest_working) {
    console.log(`\n✅ Latest working version: ${results.latest_working}`);
    console.log('\nTo upgrade, run:');
    if (results.language === 'python') {
      console.log(`pip install ${results.package}==${results.latest_working}`);
    } else {
      console.log(`npm install ${results.package}@${results.latest_working}`);
    }
  }
  
  if (results.first_broken) {
    console.log(`\n❌ First broken version: ${results.first_broken}`);
    console.log('This version introduced breaking changes.');
  }
}

const [,, cmd, ...args] = process.argv;

switch (cmd) {
  case 'help':
  case undefined:
    printHelp();
    break;
  case 'version':
    console.log(`DTM version ${pkg.version}`);
    break;
  case 'upgrade':
    if (!args[0]) {
      console.error('Please specify a dependency to upgrade.');
      process.exit(1);
    }
    // Call Python core logic
    const pythonPath = path.join(__dirname, '../core/main.py');
    const venvPython = path.join(__dirname, '../core/venv/bin/python3');
    const dep = args[0];
    try {
      const output = execSync(`${venvPython} ${pythonPath} upgrade ${dep}`, { stdio: 'pipe' }).toString();
      const results = parseResults(output);
      displayResults(results);
    } catch (err) {
      console.error('Error running DTM:', err.message);
      process.exit(1);
    }
    break;
  default:
    console.error(`Unknown command: ${cmd}`);
    printHelp();
    process.exit(1);
} 