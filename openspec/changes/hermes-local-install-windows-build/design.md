## Context

当前项目缺少一键安装脚本（用户需手动安装 Hermes Agent + Easy-Agent 两步操作），也缺少 CI 自动构建 Windows 安装包的流水线。目标用户（网文作者）主要使用 Windows，手动编译 Tauri 桌面端对其门槛过高。

已有基础：`scripts/setup.sh` 检测 Hermes 安装但不提供自动安装；`apps/desktop/` 已配置 Tauri v2 项目骨架。

## Goals / Non-Goals

**Goals:**
- 全平台一键安装脚本（Windows PowerShell + Unix Shell），自动安装 Hermes Agent + Easy-Agent
- GitHub Actions release 流水线：打 tag 时自动构建 Tauri Desktop → Windows MSI/EXE
- 配置 Tauri v2 的 Windows 打包参数（图标、名称、安装目录等）
- 提供本地 Windows 构建辅助脚本

**Non-Goals:**
- 不做 macOS/Linux 安装包构建（仅 CI 中做 Windows，本地脚本通用于开发）
- 不做自动签名（需配置 secrets 签名证书，CI 中预留 hook）
- 不做自动发布到 GitHub Releases 以外的渠道（如 winget、choco）
- 不做 Hermes Agent 源码级别的打包（仅 pip install）

## Decisions

### Decision 1: pip install hermes-agent 作为 Hermes 安装方式
- **方案**：一键安装脚本执行 `pip install hermes-agent` 安装 Hermes
- **原因**：Hermes 以 PyPI 包发布，pip 安装是最标准、最可靠的方式；支持版本锁定
- **替代方案**：npm install / 源码编译 → 增加依赖复杂度，pip 对 Python 用户更直接

### Decision 2: GitHub Actions 使用 tauri-action 构建
- **方案**：使用 `tauri-apps/tauri-action` GitHub Action 进行跨平台构建
- **原因**：官方维护，自动处理 Rust 环境、依赖缓存、签名等
- **替代方案**：自写 cargo build + npm build 脚本 → 需手动管理环境，增加 CI 维护成本

### Decision 3: 双格式输出 MSI + EXE（NSIS）
- **方案**：Tauri v2 同时配置 MSI（Windows Installer）和 NSIS（EXE）两种输出格式
- **原因**：MSI 适合企业/批量部署，EXE 更适合普通用户双击安装；双格式覆盖所有场景
- **替代方案**：仅 MSI → 用户需要管理员权限才能安装，增加门槛

### Decision 4: 打 tag 触发 release，而非每次 push
- **方案**：release workflow 仅在 `v*` tag push 时触发
- **原因**：避免每次 commit 都触发耗时构建；tag 触发建立版本发布的纪律
- **替代方案**：每次 push 到 main 触发 → 浪费 CI 资源，且非每个 commit 都适合发布

## Risks / Trade-offs

| 风险 | 缓解措施 |
|------|---------|
| 用户环境中无 Python/pip | install 脚本检测并引导安装 Python，Windows 下推荐使用 Python 官方安装包 |
| Tauri Windows 构建需要 Windows runner | GitHub Actions `windows-latest` 满足需求；本地构建需 Windows 系统 |
| `tauri-action` 构建耗时较长（首次需下载 Rust crate） | 配置 cargo 缓存（`~/.cargo`）和 npm 缓存加速后续构建 |
| Hermes pip 包可能更新导致不兼容 | 在 install 脚本中可锁定版本号，release 时测试兼容版本 |
| 代码签名证书需要额外配置 | CI 中预留 `TAURI_SIGNING_PRIVATE_KEY` 环境变量，文档说明如何申请证书 |
