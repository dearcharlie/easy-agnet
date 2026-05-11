# Easy-Agent

[![Release](https://github.com/anomalyco/easy-agnet/actions/workflows/release.yml/badge.svg)](https://github.com/anomalyco/easy-agnet/actions/workflows/release.yml)

AI Novel Writing Assistant powered by [Hermes Agent](https://github.com/NousResearch/hermes-agent).

## Features

- **7 Novel Skills**: World Builder, Character Designer, Plot Planner, Chapter Writer, Continuity Check, Style Editor, Inspiration
- **6 CLI Modes**: Quick Write, Craft, Outline, Continue, Polish, Inspire
- **Desktop Client**: Tauri v2 native app with Markdown editor + AI chat (Windows/macOS)
- **Local-First**: All data stored as Markdown files on your machine

## Quick Install

### Windows

Download the latest `.msi` or `.exe` installer from [Releases](https://github.com/anomalyco/easy-agnet/releases).

### Unix (Linux/macOS)

```bash
git clone https://github.com/anomalyco/easy-agnet.git
cd easy-agnet
bash scripts/install.sh
```

### Upgrade

```bash
bash scripts/install.sh --upgrade
```

### Pin a Hermes version

```bash
bash scripts/install.sh --hermes-version v2026.5.7
```

## Quick Start

```bash
# Initialize a novel project
easy-agent init "我的小说"

# Quick write: concept to first chapter
easy-agent quick "一个程序员穿越到修仙世界，用代码修改天地规则"

# Continue writing
easy-agent continue

# Polish
easy-agent polish

# Get inspiration
easy-agent inspire
```

## Desktop

```bash
cd apps/desktop
npm run tauri dev
```

## Build Windows Installer Locally

```bash
.\scripts\build-windows.ps1
```

## Project Structure

```
easy-agnet/
├── apps/desktop/           # Tauri v2 desktop client
├── packages/easy-agent/    # Python CLI package
├── scripts/                # Install/build scripts
├── skills/novel/           # 7 Hermes Skills (SKILL.md)
├── templates/              # Project templates
└── openspec/               # Change tracking
```

## License

AGPL-3.0
