# Easy-Agent Install Script (Windows PowerShell)
# One-click install of Hermes Agent + Easy-Agent + Novel Skills

param(
    [switch]$Upgrade,
    [string]$HermesVersion = "",
    [switch]$Help
)

if ($Help) {
    Write-Host "Usage: .\install.ps1 [Options]"
    Write-Host ""
    Write-Host "Options:"
    Write-Host "  -Upgrade                  Upgrade existing installation"
    Write-Host "  -HermesVersion VERSION    Pin Hermes Agent to a specific version"
    Write-Host "  -Help                     Show this help"
    exit 0
}

$ProjectRoot = Split-Path -Parent $PSScriptRoot

Write-Host "=== Easy-Agent Install ===" -ForegroundColor Cyan

# Check Python
$python = $null
foreach ($cmd in @("python3", "python")) {
    $p = Get-Command $cmd -ErrorAction SilentlyContinue
    if ($p) { $python = $p.Source; break }
}

if (-not $python) {
    Write-Host "[!] Python 3.10+ is required." -ForegroundColor Red
    Write-Host "    Download from: https://www.python.org/downloads/"
    Write-Host "    Make sure to check 'Add Python to PATH' during installation."
    exit 1
}

$pyVersion = & $python --version
Write-Host "[✓] Python found: $pyVersion" -ForegroundColor Green

# Install Hermes Agent using its official installer (not on PyPI)
$hermesCmd = Get-Command hermes -ErrorAction SilentlyContinue

if ($hermesCmd -and -not $Upgrade) {
    Write-Host "[✓] Hermes Agent already installed" -ForegroundColor Green
} else {
    $hVersion = if ($HermesVersion) { $HermesVersion } else { "v2026.5.7" }
    $hermesInstallUrl = "https://raw.githubusercontent.com/NousResearch/hermes-agent/$hVersion/scripts/install.ps1"

    if ($Upgrade) {
        Write-Host "[*] Upgrading Hermes Agent..." -ForegroundColor Yellow
    } else {
        Write-Host "[*] Installing Hermes Agent..." -ForegroundColor Yellow
    }

    try {
        iex (irm $hermesInstallUrl)
        Write-Host "[✓] Hermes Agent installed" -ForegroundColor Green
    } catch {
        Write-Host "[!] Hermes install encountered issues." -ForegroundColor Yellow
        Write-Host "    Try manually: irm $hermesInstallUrl | iex"
    }
}

# Install Easy-Agent Python package
Write-Host "[*] Installing Easy-Agent..." -ForegroundColor Yellow
& $python -m pip install -e "$ProjectRoot\packages\easy-agent\"

$eaCmd = Get-Command easy-agent -ErrorAction SilentlyContinue
if ($eaCmd) {
    Write-Host "[✓] Easy-Agent installed" -ForegroundColor Green
}

# Copy skills
$hermesSkillsDir = "$env:USERPROFILE\.hermes\skills\novel"
New-Item -ItemType Directory -Force -Path $hermesSkillsDir | Out-Null
$skillsSource = "$ProjectRoot\skills\novel"
if (Test-Path $skillsSource) {
    Copy-Item -Path "$skillsSource\*" -Destination $hermesSkillsDir -Recurse -Force
    Write-Host "[✓] Novel skills installed to ~\.hermes\skills\novel\" -ForegroundColor Green
}

# Create projects directory
$projectsDir = "$env:USERPROFILE\easy-agent-projects"
New-Item -ItemType Directory -Force -Path $projectsDir | Out-Null
Write-Host "[✓] Projects directory: $projectsDir" -ForegroundColor Green

# Create default config
$hermesConfigDir = "$env:USERPROFILE\.hermes"
$hermesConfig = "$hermesConfigDir\config.yaml"
if (-not (Test-Path $hermesConfig)) {
    New-Item -ItemType Directory -Force -Path $hermesConfigDir | Out-Null
    @"
novel:
  projects_dir: $projectsDir
  default_language: zh
  max_concurrency: 3
  chapter_word_count: 2500
"@ | Out-File -FilePath $hermesConfig -Encoding utf8
    Write-Host "[✓] Default config created at ~\.hermes\config.yaml" -ForegroundColor Green
}

# Install npm dependencies for Desktop
$desktopDir = "$ProjectRoot\apps\desktop"
if (Test-Path "$desktopDir\package.json") {
    Write-Host "[*] Installing Desktop npm dependencies..." -ForegroundColor Yellow
    Push-Location $desktopDir
    & npm install 2>&1 | Out-Null
    Pop-Location
    Write-Host "[✓] Desktop dependencies installed" -ForegroundColor Green
}

Write-Host ""
Write-Host "=== Install complete! ===" -ForegroundColor Cyan
Write-Host "Run 'easy-agent init <project-name>' to start a new novel project."
