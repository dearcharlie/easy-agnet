## ADDED Requirements

### Requirement: Cross-platform one-click install script
The system SHALL provide `scripts/install.sh` (Unix) and `scripts/install.ps1` (Windows) that install both Hermes Agent and Easy-Agent in a single step.

#### Scenario: Fresh install on Linux/macOS
- **WHEN** user runs `bash scripts/install.sh`
- **THEN** the script SHALL detect whether Python 3.10+ is installed
- **THEN** it SHALL run `pip install hermes-agent`
- **THEN** it SHALL run `pip install -e packages/easy-agent/`
- **THEN** it SHALL create the `~/.hermes/skills/novel/` directory and copy skill files
- **THEN** it SHALL print a success message with next steps

#### Scenario: Fresh install on Windows
- **WHEN** user runs `scripts/install.ps1` in PowerShell
- **THEN** the script SHALL detect Python 3.10+ or prompt to install it
- **THEN** it SHALL run `pip install hermes-agent`
- **THEN** it SHALL run `pip install -e packages/easy-agent/`
- **THEN** it SHALL install npm dependencies for the desktop app
- **THEN** it SHALL print a success message

### Requirement: Existing install upgrade
The install script SHALL support upgrading existing installations by checking current versions and updating only if newer.

#### Scenario: Upgrade existing installation
- **WHEN** user runs install script with `--upgrade` flag
- **THEN** the script SHALL run `pip install --upgrade hermes-agent`
- **THEN** the script SHALL update skill files from the latest source
- **THEN** it SHALL skip npm install if package.json hasn't changed

### Requirement: Version lock support
The install script SHALL support pinning Hermes Agent to a specific version for compatibility.

#### Scenario: Install with version lock
- **WHEN** user runs `bash scripts/install.sh --hermes-version 0.2.0`
- **THEN** the script SHALL run `pip install hermes-agent==0.2.0` instead of the latest
