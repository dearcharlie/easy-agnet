## Context

Easy-Agent 基于 Hermes Agent 构建，不重新造 Agent 引擎。Hermes 已提供 Skills、Memory（MEMORY.md + USER.md）、Subagent Delegation（delegate_task）、Session Search（FTS5）、Code Execution、Plugin、API Server 等核心能力。本项目通过封装 7 个 Novel Skill + Desktop 客户端，将 Hermes 的能力定向到网文创作场景。

InkOS 提供重要参考：其多 Agent 管线（Radar → Planner → Composer → Architect → Writer → Observer → Reflector → Auditor → Reviser）展示了小说创作的 Agent 协作模式。但 Easy-Agent 的设计哲学不同——用 Hermes Skill 替代自有 Agent 引擎，每个 Skill 对应一个创作环节，由 Hermes 自身负责调度。

当前项目状态：仅有 `AGENTS.md` 总体规划文档，无任何代码实现。

## Goals / Non-Goals

**Goals:**
- 完成 7 个 Novel Skill 的 SKILL.md 编写，遵循 agentskills.io 规范，存入 `~/.hermes/skills/novel/`
- 定义并实现本地文件系统数据模型（项目目录结构、模板文件）
- 实现 CLI 全流程：从创建项目到完成一章的创作、润色、检查
- 搭建 Tauri v2 Desktop 骨架，实现项目列表 + Markdown 编辑 + AI 对话

**Non-Goals:**
- 不开发自有 Agent 引擎（完全依赖 Hermes Agent）
- 不实现 Skills Hub 发布（P3 阶段）
- 不实现守护进程自动写章（InkOS 特性，非本版本目标）
- 不实现 AIGC 检测、风格仿写、同人创作等进阶功能
- 不实现 Desktop 统计分析面板、角色关系图等 P2 功能

## Decisions

### Decision 1: Skill 粒度按创作环节而非按 Agent 角色划分
- **方案**：每个创作环节一个 Skill（world-builder, character-designer 等），而非按 InkOS 的 Radar/Planner/Writer/Auditor 等 Agent 角色划分
- **原因**：Hermes Skill 是给 LLM 读取的指令文档，按环节划分更符合用户心智模型（"我要建世界观"→ 加载 world-builder skill）；InkOS 的 Agent 粒度是为管线内部调度设计的
- **替代方案**：按 InkOS 的 Agent 角色划分 → 与 Hermes Skill 设计哲学不符，用户难以理解

### Decision 2: Hermes `delegate_task` 实现并行章节生成
- **方案**：chapter-writer Skill 利用 Hermes 的 `delegate_task` 能力，最多 3 并发生成章节草稿
- **原因**：`delegate_task` 是 Hermes 原生支持的 Subagent 能力，无需额外实现调度逻辑
- **替代方案**：自己实现并发控制 → 重复造轮子，增加维护成本

### Decision 3: 本地文件系统为唯一数据存储，不使用数据库
- **方案**：所有数据存为 Markdown 文件，目录结构即项目结构
- **原因**：用户可直接编辑文件、用 Git 做版本控制、100% 数据主权。InkOS 也采用类似理念
- **替代方案**：SQLite → 增加 Desktop 数据同步复杂度，违背本地优先原则

### Decision 4: Desktop 通过 Hermes API Server（HTTP）通信
- **方案**：Desktop 前端通过 HTTP 调用 Hermes API Server（127.0.0.1:8520），使用 OpenAI 兼容端点
- **原因**：Hermes 原生提供 API Server，无需额外适配层；流式 SSE 支持实时 AI 输出
- **替代方案**：Tauri Rust 层直接调用 Hermes SDK → 耦合紧密，更新 Hermes 时需同步修改

### Decision 5: 先 CLI MVP 再 Desktop
- **方案**：P0 纯 CLI 验证 Skill 和流程，P1 构建 Desktop 骨架
- **原因**：快速验证核心创作流程，避免 Desktop UI 干扰核心逻辑验证
- **替代方案**：CLI + Desktop 同步开发 → 分散精力，核心流程未验证前 Desktop 无实际价值

## Risks / Trade-offs

| 风险 | 缓解措施 |
|------|---------|
| Hermes Agent 的 `delegate_task` 并发限制（目前最多 3 并发） | 通过配置项暴露并发数上限，文档说明 Hermes 限制 |
| Hermes Memory 容量有限（2200 + 1375 字符） | 长篇小说需拆分为多个项目，或在章节间手动清理记忆 |
| Hermes API Server 进程管理复杂（启动/心跳/退出） | Desktop 侧封装 `HermesProcessManager` 模块，处理异常退出和端口冲突 |
| 7 个 Skill 提示词质量直接影响创作效果 | 第一版快速出稿，后续通过实际创作迭代优化 prompt |
| 用户对 Hermes CLI 不熟悉 | `/novel` 命令作为入口，隐藏 Hermes 底层命令 