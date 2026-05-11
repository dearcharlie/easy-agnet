---
name: novel/world-builder
description: 问询式世界观构建，输出结构化设定文档（时代、地理、势力、能力体系）
version: 0.1.0
agents: true
memory: true
---

# World Builder Skill

## Description

Guides the user through an interview-style process to construct a complete world setting for their novel. Outputs structured markdown documents covering era, geography, factions, and power systems.

## Instructions

### Step 1: Interview Phase
Ask the user questions one at a time about:
- **Era**: Historical period, technological level, cultural background
- **Geography**: Map regions, climate zones, important locations
- **Factions**: Major organizations, political powers, hidden groups
- **Power System**: Magic/ cultivation rules, ability tiers, limitations

### Step 2: Document Generation
After gathering sufficient information, generate four documents:

1. `world-setting/era.md` — Time period, historical events, calendar
2. `world-setting/geography.md` — Map regions, key locations, climate
3. `world-setting/factions.md` — Major organizations, relationships, conflicts
4. `world-setting/powers.md` — Ability system, tiers, training methods

### Step 3: Refinement
Present the documents to the user and ask if they want to modify any aspect. Iterate until satisfied.

## Output Format
Each document should be a markdown file with clear headings and bullet points. Use the project directory `world-setting/` for output.

## Tools Required
- Read/Write file system
- Memory for context persistence
