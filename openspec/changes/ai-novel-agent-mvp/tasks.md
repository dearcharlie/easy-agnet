## 1. 环境与项目初始化

- [x] 1.1 安装并验证 Hermes Agent CLI 可用（需用户手动安装，scripts/setup.sh 提供检测）
- [x] 1.2 创建 `~/.hermes/skills/novel/` 目录结构
- [x] 1.3 创建 `~/easy-agent-projects/` 默认项目根目录
- [x] 1.4 创建 `~/.hermes/config.yaml` 添加小说相关配置节
- [x] 1.5 创建 Tauri v2 项目骨架（`apps/desktop/`），集成 React 18 + Vite

## 2. Novel Skill Pack（7 个核心 Skill）

- [x] 2.1 编写 `world-builder/SKILL.md`
- [x] 2.2 编写 `character-designer/SKILL.md`
- [x] 2.3 编写 `plot-planner/SKILL.md`
- [x] 2.4 编写 `chapter-writer/SKILL.md`
- [x] 2.5 编写 `continuity-check/SKILL.md`
- [x] 2.6 编写 `style-editor/SKILL.md`
- [x] 2.7 编写 `inspiration/SKILL.md`
- [x] 2.8 验证所有 Skill 符合 agentskills.io 标准格式

## 3. 本地数据模型与模板

- [x] 3.1 实现项目初始化命令 `easy-agent init <project-name>`，创建完整目录结构
- [x] 3.2 创建 `.hermes.md` 项目上下文模板文件
- [x] 3.3 创建角色卡 YAML 模板文件
- [x] 3.4 实现项目列表扫描逻辑（读取 `~/easy-agent-projects/` 下的项目目录）
- [x] 3.5 实现草稿/已审核章节分离存储逻辑（`drafts/` vs `chapters/`）

## 4. CLI 交互模式

- [x] 4.1 实现 Hermes CLI 入口封装（`easy-agent` 命令路由，对应 `/novel` 能力）
- [x] 4.2 实现 Quick 模式：输入点子 → 调用 world-builder + plot-planner + chapter-writer 连跑
- [x] 4.3 实现 Craft 模式：逐段对话式引导，每段暂停等待用户确认
- [x] 4.4 实现 Outline 模式：先生成大纲，用户确认后逐章填充
- [x] 4.5 实现 Continue 模式：读取已有章节末尾状态，自动续写下一章
- [x] 4.6 实现 Polish 模式：读取指定章节，调用 style-editor Skill
- [x] 4.7 实现 Inspire 模式：读取当前故事状态，返回情节建议
- [ ] 4.8 端到端验证：通过 CLI 完成一部 3 章短篇小说的完整创作流程（需安装 Hermes CLI）

## 5. 并行章节生成

- [x] 5.1 在 chapter-writer Skill 中集成 `delegate_task` 调用逻辑
- [x] 5.2 实现并发数配置项（默认 3，可覆盖）
- [x] 5.3 实现并行章节的依赖顺序保障（基于 Outline 而非基于彼此）
- [x] 5.4 实现并行生成结果的收集与去重写入

## 6. 连续性检查

- [x] 6.1 在 continuity-check Skill 中集成 `session_search` 调用逻辑
- [x] 6.2 实现角色一致性检测规则（行为、知识、对话风格）
- [x] 6.3 实现情节矛盾检测规则（时间线、事件因果）
- [x] 6.4 实现伏笔追踪列表维护与过期告警
- [x] 6.5 实现检查报告的格式化输出（问题列表 + 建议修复）

## 7. Desktop 骨架

- [x] 7.1 搭建 Tauri v2 项目（`apps/desktop/`），配置 Rust 后端 + React 前端
- [x] 7.2 实现项目列表页面：扫描 `~/easy-agent-projects/`，展示项目卡片，支持创建/打开/删除
- [x] 7.3 实现 Markdown 编辑器，支持编辑 + 预览切换
- [x] 7.4 实现 Hermes API Server 进程管理模块（`HermesProcessManager`）：启动/心跳/停止
- [x] 7.5 实现 AI 对话面板组件：HTTP POST + SSE 流式渲染
- [x] 7.6 实现快捷操作按钮栏：Quick Write / Continue / Polish / Check
- [x] 7.7 实现基础侧边面板框架（角色/大纲/AI 对话/统计 标签页切换）
- [ ] 7.8 验证 Desktop 可打开项目、编辑 Markdown、发送消息给 Hermes 并显示回复（需先安装 Hermes CLI + Tauri 构建工具）
