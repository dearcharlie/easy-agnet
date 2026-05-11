## 1. 一键安装脚本

- [x] 1.1 编写 `scripts/install.sh`（Unix）：检测 Python + pip，执行 `pip install hermes-agent` + `pip install -e packages/easy-agent/`，复制 Skill 文件
- [x] 1.2 编写 `scripts/install.ps1`（Windows PowerShell）：检测 Python，安装 Hermes + Easy-Agent，安装 npm 依赖
- [x] 1.3 实现 `--upgrade` 参数（自动检测版本并升级）
- [x] 1.4 实现 `--hermes-version` 参数（锁定 Hermes Agent 版本号）
- [x] 1.5 更新 `scripts/setup.sh` 复用 install 脚本，保持向后兼容
- [x] 1.6 方案确认：使用 Hermes 官方 install 脚本（而非 pip），更新 install.sh/install.ps1 已适配

## 2. GitHub Actions Release 流水线

- [x] 2.1 创建 `.github/workflows/release.yml`，配置 `on: push: tags: ['v*']` 触发
- [x] 2.2 配置 Rust 工具链步骤（`actions-rust/setup-rust`）
- [x] 2.3 配置 Node.js + npm install + npm 缓存
- [x] 2.4 配置 cargo 缓存（`~/.cargo`）
- [x] 2.5 集成 `tauri-apps/tauri-action` 执行 `tauri build`
- [x] 2.6 配置 GitHub Release 创建 + 上传 MSI/EXE 资产
- [x] 2.7 配置代码签名支持（读取 `TAURI_PRIVATE_KEY` / `TAURI_KEY_PASSWORD` secrets）
- [x] 2.8 添加 workflow badge 到 README

## 3. Windows 打包配置

- [x] 3.1 更新 `apps/desktop/src-tauri/tauri.conf.json`：配置 MSI + NSIS 双格式输出
- [x] 3.2 配置 Windows 安装元数据：productName、publisher、installDir
- [x] 3.3 添加 Windows `.ico` 图标到 `apps/desktop/src-tauri/icons/`
- [x] 3.4 编写 `scripts/build-windows.ps1` 本地构建脚本
- [x] 3.5 更新 `.gitignore` 忽略构建产出（`dist/installers/`、`target/`）

## 4. 文档与验证

- [x] 4.1 更新 README.md 安装章节（Windows 用户可直接下载安装包，Unix 用户使用 install 脚本）
- [x] 4.2 更新 AGENTS.md 记录安装方式变更
- [ ] 4.3 端到端验证：GitHub Actions 触发 release 构建 → 产出 MSI/EXE → 在 Windows 上安装运行（需推送正式 tag 触发）
