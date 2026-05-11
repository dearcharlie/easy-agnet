---
name: novel/character-designer
description: 角色创建、多角色关系网、小传生成
version: 0.1.0
agents: true
memory: true
web_search: true
---

# Character Designer Skill

## Description

Creates detailed character cards with relationships, backstories, and character arcs. Supports relationship network visualization data generation.

## Instructions

### Character Card Fields
For each character, fill in:
- `name` — Character name
- `role` — Protagonist, antagonist, supporting, etc.
- `age` — Current age
- `personality` — Key personality traits
- `appearance` — Physical description
- `background` — History and origin story
- `abilities` — Powers, skills, knowledge
- `goals` — Short-term and long-term objectives
- `relationships` — List of relationships with other characters
- `arc` — Planned character development arc

### Workflow

#### Single Character Creation
1. Ask about the character's role in the story
2. Interview each field conversationally
3. Generate YAML frontmatter markdown card
4. Save to `characters/<name>.md`
5. Update `characters/_index.md` with relationship entries

#### Relationship Network
When creating multiple characters, maintain a relationship matrix:
- Track who knows whom
- Note power dynamics (mentor/student, rival, ally, enemy)
- Flag potential conflict points

#### Batch Creation
When creating multiple characters (e.g., for a faction), create them together to ensure relationship coherence. Use `delegate_task` for parallel generation of independent characters.

## Output Format
YAML frontmatter + markdown body in `characters/<name>.md`.

## Tools Required
- Read/Write file system
- Memory for character context
- Web Search (optional, for name inspiration)
