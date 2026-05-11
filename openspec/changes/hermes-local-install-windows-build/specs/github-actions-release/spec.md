## ADDED Requirements

### Requirement: Release workflow triggers
The GitHub Actions release workflow SHALL trigger when a git tag matching `v*` is pushed.

#### Scenario: Tag push triggers build
- **WHEN** a maintainer pushes a tag `v0.2.0`
- **THEN** the release workflow SHALL start automatically
- **WHEN** a regular commit is pushed without a tag
- **THEN** the release workflow SHALL NOT start

### Requirement: Tauri application build
The workflow SHALL build the Tauri Desktop application for Windows using `tauri-apps/tauri-action`.

#### Scenario: Successful build
- **WHEN** the release workflow runs
- **THEN** it SHALL checkout the repository
- **THEN** it SHALL set up Rust toolchain via `actions-rust/setup-rust`
- **THEN** it SHALL install Node.js and npm dependencies for `apps/desktop/`
- **THEN** it SHALL run `tauri build` via `tauri-apps/tauri-action`
- **THEN** it SHALL produce `.msi` and `.exe` installer files

### Requirement: Artifact caching
The workflow SHALL cache Rust (`~/.cargo`) and npm (`node_modules`) dependencies to speed up subsequent builds.

#### Scenario: Cache hit speeds up build
- **WHEN** the workflow runs after a previous build
- **THEN** cargo dependencies SHALL be restored from cache (if unchanged)
- **THEN** npm dependencies SHALL be restored from cache (if unchanged)
- **THEN** the build SHALL skip downloading already-cached dependencies

### Requirement: GitHub Release publishing
The workflow SHALL create a GitHub Release with the built installer artifacts attached.

#### Scenario: Release created and artifacts uploaded
- **WHEN** the Tauri build completes successfully
- **THEN** the workflow SHALL create a GitHub Release for the tag
- **THEN** it SHALL upload the `.msi` and `.exe` files as release assets
- **THEN** it SHALL generate release notes from conventional commits

### Requirement: Code signing support
The workflow SHALL support code signing via `TAURI_PRIVATE_KEY` and `TAURI_KEY_PASSWORD` repository secrets.

#### Scenario: Signed build with secrets configured
- **WHEN** `TAURI_PRIVATE_KEY` and `TAURI_KEY_PASSWORD` secrets are set in the repository
- **THEN** the build SHALL sign the Windows installer with the provided key
- **WHEN** the secrets are not configured
- **THEN** the build SHALL proceed without signing and log a warning
