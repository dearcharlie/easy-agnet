## ADDED Requirements

### Requirement: Dual-format installer output
The Tauri configuration SHALL produce both `.msi` (Windows Installer) and `.exe` (NSIS) installer formats.

#### Scenario: Build produces both formats
- **WHEN** user runs `npm run tauri build` on Windows
- **THEN** the build SHALL generate a `.msi` file in `src-tauri/target/release/bundle/msi/`
- **THEN** the build SHALL generate an `.exe` file in `src-tauri/target/release/bundle/nsis/`

### Requirement: Windows installer metadata
The Tauri configuration SHALL include proper Windows metadata: product name, publisher, installer icon, and default install directory.

#### Scenario: Installer displays correct metadata
- **WHEN** user runs the `.msi` or `.exe` installer
- **THEN** the installer SHALL display "Easy-Agent Novel Studio" as the product name
- **THEN** the installer SHALL show the correct version number
- **THEN** the installer SHALL default installation to `%LOCALAPPDATA%\easy-agent-novel-studio`

### Requirement: Windows application icon
The application SHALL have a Windows-compatible `.ico` icon file configured in `tauri.conf.json`.

#### Scenario: Icon displays in explorer
- **WHEN** user views the installed application in File Explorer or Start Menu
- **THEN** the application SHALL display the configured icon
- **WHEN** the installer runs
- **THEN** the installer SHALL display the application icon in its UI

### Requirement: Local build script for Windows
The project SHALL provide `scripts/build-windows.ps1` to build the Windows installer locally without CI.

#### Scenario: Local build on Windows
- **WHEN** user runs `.\scripts\build-windows.ps1`
- **THEN** the script SHALL verify Rust and Node.js are installed
- **THEN** it SHALL run `npm install` in `apps/desktop/`
- **THEN** it SHALL run `npm run tauri build`
- **THEN** it SHALL copy the built installers to `dist/installers/`
