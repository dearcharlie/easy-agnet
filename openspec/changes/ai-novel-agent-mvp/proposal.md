## Why

当前 AI 小说写作领域缺乏一个既充分利用成熟 Agent 框架（Hermes Agent）能力、又提供本地优先体验专为网文作者设计的工具。InkOS 已验证了多 Agent 管线创作小说的可行性，但其依赖自有 Agent 引擎，耦合度高。Easy-Agent 定位为 **Hermes Agent 的垂直行业 Skill Pack**，复用其 Skills、Memory、Delegation、MCP 等原生能力，以最小成本快速交付网文创作全流程支持。

## What Changes

- 在 Hermes Agent 之上封装 7 个核心小说创作 Skill（world-builder, character-designer, plot-planner, chapter-writer, continuity-check, style-editor, inspiration）
- 定义本地文件系统数据模型（项目目录结构、角色卡模板、`.hermes.md` 上下文模板）
- 实现 6 种交互模式 CLI 命令（quick/craft/outline/continue/polish/inspire）
- 实现多 Agent 并行章节生成（通过 Hermes `delegate_task`）
- 实现上下文一致性检查（通过 Hermes `session_search` + Memory）
- 实现 Tauri v2 Desktop 骨架，对接 Hermes API Server

## Capabilities

### New Capabilities
- `novel-skill-pack`: 7 个 Hermes Skill（world-builder, character-designer, plot-planner, chapter-writer, continuity-check, style-editor, inspiration），遵循 agentskills.io 标准
- `cli-interaction-modes`: 6 种 CLI 创作模式（quick/craft/outline/continue/polish/inspire）
- `local-data-model`: 基于本地文件系统的项目数据模型（项目目录、角色卡、大纲、章节、草稿、笔记）
- `parallel-generation`: 基于 Hermes `delegate_task` 的多章节并行生成
- `continuity-check`: 基于 Hermes `session_search` + Memory 的人设一致性检查
- `tauri-desktop-skeleton`: Tauri v2 Desktop 客户端骨架（项目列表、Markdown 编辑器、AI 对话面板）

### Modified Capabilities
- （无现有 spec 被修改）

## Impact

- **新增目录**：`~/.hermes/skills/novel/`（7 个 Skill 目录）、`~/easy-agent-projects/`（用户项目目录）
- **新增依赖**：Hermes Agent（运行时）、Tauri v2（Desktop）、React 18 + Vite（前端）、Vditor（编辑器）
- **配置变更**：`~/.hermes/config.yaml` 新增小说相关配置
- **进程管理**：Desktop 客户端需管理 Hermes API Server 进程生命周期
