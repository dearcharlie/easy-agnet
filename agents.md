# Easy-Agent 项目总体规划

> 基于 [Hermes Agent](https://github.com/NousResearch/hermes-agent) 底层能力封装，面向垂直行业打造提效工具平台。
> 首个落地应用：**AI 小说助手（Novel Studio）**，目标用户为网文作者。

---

## 一、项目定位

```
┌──────────────────────────────────────────────────┐
│              Easy-Agent Desktop                   │
│         (Tauri v2 本地桌面客户端)                  │
├──────────────────────────────────────────────────┤
│  Novel Skill Pack     │  [未来] 营销 Skill Pack   │
│  · 世界观构建          │  · 文案生成               │
│  · 角色设计            │  · 数据分析               │
│  · 大纲规划            │                          │
│  · 章节撰写            │                          │
│  · 一致性检查          │                          │
│  · 文风润色            │                          │
│  · 灵感注入            │                          │
├──────────────────────────────────────────────────┤
│              Hermes Agent (底层引擎)              │
│  Skills · Tools · Memory · Delegation · MCP · API│
└──────────────────────────────────────────────────┘
```

**核心设计原则：**
- Easy-Agent 不重新造 Agent 引擎，只做行业 Skill Pack + Desktop 客户端
- 所有 AI 写作能力通过 Hermes 的 Skill / Plugin / Memory / Delegation 机制实现
- 数据持久化使用本地文件系统 + Markdown 格式，确保用户对数据的完全掌控

---

## 二、安装方式

### 一键安装（推荐）

Easy-Agent 提供一键安装脚本，自动安装 Hermes Agent + Easy-Agent + Novel Skills。

**Unix (Linux/macOS):**
```bash
git clone <repo-url> && cd easy-agnet
bash scripts/install.sh
```

**Windows:**
1. 从 GitHub Releases 下载 `.msi` 或 `.exe` 安装包
2. 或运行 PowerShell: `.\scripts\install.ps1`

**升级:**
```bash
bash scripts/install.sh --upgrade
```

**锁定版本:**
```bash
bash scripts/install.sh --hermes-version v2026.5.7
```

### 手动安装

```bash
pip install hermes-agent
pip install -e packages/easy-agent/
cp -r skills/novel/* ~/.hermes/skills/novel/
```

---

## 三、Hermes Agent 能力映射

| Hermes 能力 | 小说场景应用 |
|-------------|-------------|
| **Skills 系统** | 每个创作环节封装为一个 Skill（大纲、写稿、润色等），SKILL.md 格式，支持渐进式加载 |
| **Subagent Delegation** | `delegate_task` 并行生成多章节、多人设并行创建，最多 3 并发（可配置） |
| **Persistent Memory** | `MEMORY.md` + `USER.md` 跨会话记住角色设定、世界观、情节线索，容量 2200 + 1375 字符 |
| **Session Search** | `session_search` + FTS5 全文检索历史对话，追溯创作决策 |
| **Context Files** | `AGENTS.md` / `.hermes.md` 定义项目级小说创作规范、人设卡、大纲 |
| **Plugin 系统** | 扩展自定义工具（小说字数统计、敏感词检测、网文平台排版） |
| **Code Execution** | `execute_code` 多步骤自动化（如批量章节格式化、数据统计） |
| **API Server** | OpenAI 兼容 HTTP 端点，对接 Desktop 客户端 |
| **Skills Hub** | 发布社区共享的小说模板 / 写作技巧 / 世界观素材 Skill |
| **Memory Providers** | Honcho / Mem0 等外部记忆后端，支持知识图谱级角色关系管理 |
| **Cron** | 定时任务（每日写作提醒、连载更新计划） |

---

## 四、AI 小说助手 — 功能设计

### 4.1 创作工作流

```
设定阶段                  创作阶段                  优化阶段
┌───────────┐    ┌───────────────────┐    ┌──────────────────┐
│ WorldBuilder│    │  章节大纲生成       │    │ ContinuityChecker │
│ Character   │───→│  ChapterWriter     │───→│ (上下文一致性)     │
│ Designer    │    └───────┬───────────┘    └────────┬─────────┘
└───────────┘            │                          │
               ┌─────────┴─────────┐                │ 通过则输出
               ▼                   ▼                ▼
         ┌───────────┐     ┌───────────┐    ┌──────────────┐
         │ Chapter 1  │     │ Chapter 2  │    │ StyleEditor  │
         │ (并行生成)  │ ... │ (并行生成)  │    │ (文风润色)    │
         └───────────┘     └───────────┘    └──────────────┘

随时可选：InspirationInjector（灵感注入）
```

### 4.2 核心 Skill 清单（7 个）

所有 Skill 存于 `~/.hermes/skills/novel/`，符合 [agentskills.io](https://agentskills.io/specification) 标准。

| Skill | 功能 | Hermes 能力依赖 |
|-------|------|----------------|
| `novel/world-builder` | 问询式世界观构建，输出结构化设定文档 | Skills + Memory |
| `novel/character-designer` | 角色创建、多角色关系网、小传生成 | Skills + Memory + Web Search |
| `novel/plot-planner` | 大纲/分卷/章纲规划、节奏控制、高潮点编排 | Skills + Memory |
| `novel/chapter-writer` | 按大纲生成章节正文，支持单章/并行多章生成 | Skills + delegate_task |
| `novel/continuity-check` | 人设一致性检查、前后矛盾检测、伏笔追踪 | Skills + session_search |
| `novel/style-editor` | 文风润色（口语化/书面化、爽点密度调节、水文精简） | Skills |
| `novel/inspiration` | 情节建议、冲突点子、转折设计、卡文突破 | Skills + Web Search |

### 4.3 交互模式

| 模式 | 命令 | 说明 | 适用场景 |
|------|------|------|----------|
| 🚀 **速写模式** | `easy-agent quick <点子>` | 给定点子，自动生成完整大纲 + 首章 | 灵感乍现，快速出稿 |
| 📝 **精细模式** | `easy-agent craft` | 逐段对话式引导，每段可人工修改后继续 | 品质优先，精细打磨 |
| 🗺️ **大纲模式** | `easy-agent outline` | 先生成完整大纲（含分卷、章纲），确认后逐章填充 | 长篇连载规划 |
| 🔄 **续写模式** | `easy-agent continue` | 基于已有内容续写，自动注入上下文和角色状态 | 连载更新 |
| ✨ **润色模式** | `easy-agent polish` | 对已有章节进行文风优化、灌水精简、爽点增强 | 改稿优化 |
| 💡 **灵感模式** | `easy-agent inspire` | 提供情节建议、冲突点子、转折设计 | 卡文突破 |

---

## 五、Desktop 客户端

### 技术选型

| 层面 | 选型 | 理由 |
|------|------|------|
| 框架 | **Tauri v2** | 体积小（<10MB）、跨平台、Rust 安全 |
| 前端 | **React 18 + Vite** | 生态成熟，组件丰富 |
| 编辑器 | Vditor / Monaco | Markdown 所见即所得，支持分屏预览 |
| 状态管理 | Zustand | 轻量，适合桌面应用 |
| 通信 | HTTP ↔ Hermes API Server | OpenAI 兼容端点，无需额外适配 |
| 打包目标 | Windows (.msi/.exe) + macOS (.dmg) | 网文作者主要使用 Windows |

### 构建方式

**CI 自动构建:** 推送 `v*` tag 触发 GitHub Actions，自动产出 MSI/EXE/DMG
**本地构建:** 运行 `scripts/build-windows.ps1` (Windows) 或 `cd apps/desktop && npm run tauri build`

---

## 六、实施路线图

### P0——命令行 MVP（已完成）
- 7 个 Skill 的 SKILL.md 编写完成
- CLI Python 包（init/list/quick/craft/outline/continue/polish/inspire）
- 本地数据模型与模板
- 并行章节生成 + 连续性检查

### P1——Desktop 骨架（已完成）
- Tauri v2 项目搭建，React 18 + Vite 前端
- 项目列表、Markdown 编辑器、AI 对话面板
- Windows 打包配置（MSI + NSIS）

### P2——完整写作体验（待开始）
- 角色面板：角色卡 CRUD + 关系图可视化
- 大纲面板：树形大纲编辑器，支持拖拽排序
- 统计面板：字数 / 章节数 / 进度仪表盘

### P3——发布上线（待开始）
- GitHub Actions CI/CD 自动化构建
- Windows MSI/EXE + macOS DMG 打包
- Skills Hub 发布社区版
