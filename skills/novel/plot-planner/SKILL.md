---
name: novel/plot-planner
description: 大纲/分卷/章纲规划、节奏控制、高潮点编排
version: 0.1.0
agents: true
memory: true
---

# Plot Planner Skill

## Description

Generates complete novel outlines with volume breakdowns, chapter plans, pacing control, and climax arrangement. Supports both full novel planning and per-volume planning.

## Instructions

### Step 1: Gather Parameters
- Novel length (target word count / chapter count)
- Number of volumes (arcs)
- Key plot points the user wants to include
- Genre-specific pacing requirements

### Step 2: Generate Outline

#### Total Outline (`outline/outline.md`)
- Novel title and logline
- Volume list with one-line summaries
- Major plot arcs (setup / confrontation / resolution)
- Character arcs mapped to volumes

#### Per-Volume Outline (`outline/volumes/vXX.md`)
- Volume title and focus
- Chapter list (titles + 1-line summary each)
- Pacing: where to place climax, twists, reveals
- Character focus for this volume

### Step 3: Chapter Beat Sheet
For each chapter, specify:
- **Opening hook** — What grabs reader attention
- **Body** — Key events and dialogue
- **Climax** — Chapter turning point
- **Closing** — Cliffhanger or transition to next chapter
- **Satisfying points** — At least one per chapter

### Pacing Rules
- **Action/Pacing Beat**: Place a major event every 3-5 chapters
- **Rest Beat**: A slower chapter for character development after every major arc
- **Twist Placement**: At 25%, 50%, 75% marks of total length
- **Climax Density**: End-of-volume climax should resolve the volume's central conflict

## Output Format
Markdown files in `outline/` directory. Chapter-level detail in volume outlines.

## Tools Required
- Read/Write file system
- Memory for maintaining plot state
