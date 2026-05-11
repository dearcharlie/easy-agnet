---
name: novel/style-editor
description: 文风润色（口语化/书面化、爽点密度调节、水文精简）
version: 0.1.0
agents: true
memory: false
---

# Style Editor Skill

## Description

Polishes chapter text by adjusting style parameters: dialogue-to-narrative ratio, satisfying-point density, verbosity trimming, and tone consistency.

## Instructions

### Style Axes

#### 1. Dialogue vs Narrative Ratio
- **Target**: ~30% dialogue, ~70% narrative (configurable)
- If too much dialogue: convert some exposition to narrative description
- If too little dialogue: add character reactions/interjections

#### 2. Pacing & Satisfying Points
Check density of satisfying moments (打脸, 升级, 收获):
- Target: at least 1 per chapter
- If insufficient, suggest adding one at a natural break point
- If excessive, flag potential reader fatigue

#### 3. Verbosity Trimming (水文精简)
Identify and suggest tightening:
- Redundant descriptions (same thing described twice)
- Purple prose (overly ornate language for web novels)
- Filler dialogue (small talk that doesn't advance plot)
- Over-explained actions ("He stood up, then walked to the door, then opened it" → "He walked to the door")

#### 4. Tone Consistency
- Verify the tone matches the novel's genre and target platform
- Adjust for platform conventions (Qidian vs Fanqie vs Feilu)

### Workflow
1. Read the chapter
2. Analyze against style axes
3. Present a diff showing proposed changes
4. Apply changes after user approval

### Report
```markdown
## Style Edit Report - chXXX

### Changes Made
- Dialogue ratio: 25% → 32% ✓
- Pacing density: 1 satisfying point → 2 ✓
- Verbosity reduced: 150 chars trimmed
- Tone adjusted: aligned with platform conventions
```
