---
name: novel/chapter-writer
description: 按大纲生成章节正文，支持单章/并行多章生成
version: 0.1.0
agents: true
memory: true
delegation: true
---

# Chapter Writer Skill

## Description

Generates chapter body text based on the outline. Supports single-chapter generation and parallel multi-chapter generation via `delegate_task`. Each chapter targets 2000-3000 Chinese characters.

## Instructions

### Pre-Writing Checklist
Before writing, verify:
1. Outline exists for this chapter
2. Character states are loaded from memory
3. Previous chapter's ending state is available
4. Key plot points for this chapter are identified

### Writing Guidelines

#### Structure
- **Opening** (10%): Hook reader with a question, action, or悬念
- **Body** (75%): Main events, dialogue, character interaction
- **Closing** (15%): Mini-climax or transition to next chapter

#### Style Rules
- Dialogue to narrative ratio: ~30:70
- At least one satisfying plot point per chapter
- Maintain consistent POV throughout the chapter
- Show, don't tell — use action and dialogue to convey information
- End with a hook that makes readers want to continue

#### Word Count
- Target: 2000-3000 characters per chapter
- Minimum: 1500
- Maximum: 4000

### Parallel Generation (via delegate_task)

When generating multiple chapters concurrently:
1. Load the outline once (shared context)
2. Spawn subagents via `delegate_task`, one per chapter
3. Each subagent receives:
   - Chapter outline and beat sheet
   - Previous chapter summary (if applicable)
   - Current character states
4. Collect all drafts into `drafts/`
5. Flag any content overlap between chapters

### Save Format
- Draft: `drafts/chXXX.draft.md`
- Approved: `chapters/chXXX.md`

## Tools Required
- Read/Write file system
- Memory for character and plot state
- `delegate_task` for parallel generation
