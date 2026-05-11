# Easy-Agent Windows Build Script
# Builds the Tauri Desktop application into MSI/EXE installers

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$DesktopDir = "$ProjectRoot\apps\desktop"

Write-Host "=== Easy-Agent Windows Build ===" -ForegroundColor Cyan

# Check prerequisites
$rustc = Get-Command rustc -ErrorAction SilentlyContinue
if (-not $rustc) {
    Write-Host "[!] Rust is required. Install from: https://rustup.rs" -ForegroundColor Red
    exit 1
}
Write-Host "[✓] Rust found: $(rustc --version)" -ForegroundColor Green

$node = Get-Command node -ErrorAction SilentlyContinue
if (-not $node) {
    Write-Host "[!] Node.js is required. Install from: https://nodejs.org" -ForegroundColor Red
    exit 1
}
Write-Host "[✓] Node.js found: $(node --version)" -ForegroundColor Green

# Install npm dependencies
Write-Host "[*] Installing npm dependencies..." -ForegroundColor Yellow
Push-Location $DesktopDir
npm install
if ($LASTEXITCODE -ne 0) {
    Write-Host "[!] npm install failed" -ForegroundColor Red
    Pop-Location
    exit 1
}
Pop-Location
Write-Host "[✓] npm dependencies installed" -ForegroundColor Green

# Build Tauri application
Write-Host "[*] Building Tauri application..." -ForegroundColor Yellow
Push-Location $DesktopDir
npm run tauri build
if ($LASTEXITCODE -ne 0) {
    Write-Host "[!] Tauri build failed" -ForegroundColor Red
    Pop-Location
    exit 1
}
Pop-Location
Write-Host "[✓] Tauri build complete" -ForegroundColor Green

# Copy installers to dist/
$distDir = "$ProjectRoot\dist\installers"
New-Item -ItemType Directory -Force -Path $distDir | Out-Null

$msiDir = "$DesktopDir\src-tauri\target\release\bundle\msi"
$nsisDir = "$DesktopDir\src-tauri\target\release\bundle\nsis"

if (Test-Path $msiDir) {
    Copy-Item "$msiDir\*.msi" -Destination $distDir -Force
    Write-Host "[✓] MSI installer copied to $distDir" -ForegroundColor Green
}
if (Test-Path $nsisDir) {
    Copy-Item "$nsisDir\*.exe" -Destination $distDir -Force
    Write-Host "[✓] NSIS installer copied to $distDir" -ForegroundColor Green
}

Write-Host ""
Write-Host "=== Build complete! ===" -ForegroundColor Cyan
Write-Host "Installers available at: $distDir"
Get-ChildItem $distDir | ForEach-Object { Write-Host "  - $($_.Name)" }
