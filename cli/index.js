#!/usr/bin/env node

const { program } = require('commander');
const chalk = require('chalk');
const inquirer = require('inquirer');
const { execSync } = require('child_process');
const path = require('path');

// Get the path to the core directory
const corePath = path.join(__dirname, '..', 'core');

program
  .version('0.1.1')
  .description('A developer tool for safe, intelligent dependency upgrades');

program
  .command('analyze')
  .description('Analyze all dependencies in the project')
  .action(async () => {
    try {
      console.log(chalk.blue('\n🔍 Analyzing project dependencies...\n'));
      
      // Run the Python script with the correct path
      const result = execSync(`python3 ${path.join(corePath, 'main.py')} analyze`, { encoding: 'utf-8' });
      const analysis = JSON.parse(result.split('\n').pop());

      // Process results
      const packages = Object.entries(analysis);
      
      if (packages.length === 0) {
        console.log(chalk.yellow('No dependencies found in the project.'));
        return;
      }

      // Group packages by status
      const upgradable = [];
      const conflicts = [];
      const errors = [];

      for (const [package, data] of packages) {
        if (data.status === 'error') {
          errors.push({ package, message: data.message });
        } else if (data.dependency_conflicts) {
          conflicts.push({ package, ...data });
        } else if (data.latest_working) {
          upgradable.push({ package, ...data });
        }
      }

      // Display results
      if (upgradable.length > 0) {
        console.log(chalk.green('\n✅ Upgradable Packages:'));
        for (const pkg of upgradable) {
          console.log(`\n  ${chalk.bold(pkg.package)}:`);
          console.log(`    Latest working version: ${pkg.latest_working}`);
          if (pkg.first_broken) {
            console.log(`    First broken version: ${pkg.first_broken}`);
          }
        }
      }

      if (conflicts.length > 0) {
        console.log(chalk.yellow('\n⚠️ Packages with Conflicts:'));
        for (const pkg of conflicts) {
          console.log(`\n  ${chalk.bold(pkg.package)}:`);
          console.log('    Dependency conflicts:');
          for (const [dep, issues] of Object.entries(pkg.dependency_conflicts)) {
            console.log(`      - ${dep}:`);
            issues.forEach(issue => console.log(`        ${issue}`));
          }
        }
      }

      if (errors.length > 0) {
        console.log(chalk.red('\n❌ Errors:'));
        for (const pkg of errors) {
          console.log(`\n  ${chalk.bold(pkg.package)}: ${pkg.message}`);
        }
      }

      // Ask if user wants to upgrade packages
      if (upgradable.length > 0) {
        const { action } = await inquirer.prompt([
          {
            type: 'list',
            name: 'action',
            message: '\nWhat would you like to do?',
            choices: [
              { name: 'Upgrade all packages', value: 'all' },
              { name: 'Choose packages to upgrade', value: 'select' },
              { name: 'Exit', value: 'exit' }
            ]
          }
        ]);

        if (action === 'exit') {
          return;
        }

        if (action === 'all') {
          for (const pkg of upgradable) {
            console.log(`\n${chalk.blue(`Upgrading ${pkg.package}...`)}`);
            execSync(`dtm upgrade ${pkg.package}`, { stdio: 'inherit' });
          }
        } else if (action === 'select') {
          const { selectedPackages } = await inquirer.prompt([
            {
              type: 'checkbox',
              name: 'selectedPackages',
              message: 'Select packages to upgrade:',
              choices: upgradable.map(pkg => ({
                name: `${pkg.package} (${pkg.latest_working})`,
                value: pkg.package
              }))
            }
          ]);

          for (const package of selectedPackages) {
            console.log(`\n${chalk.blue(`Upgrading ${package}...`)}`);
            execSync(`dtm upgrade ${package}`, { stdio: 'inherit' });
          }
        }
      }

    } catch (error) {
      console.error(chalk.red('\nError running DTM:'), error.message);
      process.exit(1);
    }
  });

program
  .command('upgrade <package-name>')
  .description('Upgrade a specific package')
  .action((packageName) => {
    try {
      console.log(chalk.blue(`\n🔍 Analyzing ${packageName}...\n`));
      execSync(`python3 ${path.join(corePath, 'main.py')} upgrade ${packageName}`, { stdio: 'inherit' });
    } catch (error) {
      console.error(chalk.red('\nError running DTM:'), error.message);
      process.exit(1);
    }
  });

program.parse(process.argv); 