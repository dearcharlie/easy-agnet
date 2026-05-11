## Why

当前 Easy-Agent 的安装流程需要用户手动安装 Hermes Agent CLI 作为前置依赖，增加了使用门槛。同时缺少 CI/CD 流水线来自动构建 Windows 安装包，限制了面向网文作者（主要使用 Windows）的分发能力。本变更将 Hermes Agent 的安装集成到 Easy-Agent 一键安装流程中，并配置 GitHub Actions 自动构建 Windows MSI/EXE 安装包。

## What Changes

- 创建一键安装脚本 `install.py`/`install.ps1`，自动检测并安装 Hermes Agent (pip install hermes-agent)
- 创建 GitHub Actions workflow (`.github/workflows/release.yml`)，在打 tag 时自动构建 Tauri Desktop → Windows MSI/EXE
- 配置 Tauri v2 Windows 打包目标（`.msi` 和 `.exe`）及代码签名
- 创建 `scripts/build-windows.ps1` 本地构建辅助脚本
- 创建 `scripts/install.sh` / `scripts/install.ps1` 全平台安装入口（Hermes + Easy-Agent 一键装好）
- 更新 `README.md` 安装说明

## Capabilities

### New Capabilities
- `hermes-bundled-install`: 将 Hermes Agent 安装集成到 Easy-Agent 一键安装流程，支持 pip install hermes-agent 自动检测与安装
- `github-actions-release`: GitHub Actions CI/CD 流水线，在 git tag 触发时自动编译 Tauri Desktop 并产出 Windows MSI/EXE 安装包
- `windows-installer-packaging`: Tauri v2 Windows 打包配置，含 .msi / .exe 双格式输出和代码签名支持

### Modified Capabilities
- （无现有 spec 被修改）

## Impact

- **新增文件**：`.github/workflows/release.yml`、`scripts/install.sh`、`scripts/install.ps1`、`scripts/build-windows.ps1`
- **修改文件**：`scripts/setup.sh`（集成 Hermes 安装）、`apps/desktop/src-tauri/tauri.conf.json`（补充 Windows 配置）、`README.md`
- **新增依赖**：`hermes-agent` Python 包（运行时）、`@tauri-apps/cli`（构建）、`wix`（Windows 打包）
- **CI 变更**：新增 GitHub Actions release 工作流，需配置 `TAURI_PRIVATE_KEY` 和 `TAURI_KEY_PASSWORD` secrets
