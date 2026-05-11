---
name: novel/continuity-check
description: 人设一致性检查、前后矛盾检测、伏笔追踪
version: 0.1.0
agents: true
memory: true
session_search: true
---

# Continuity Check Skill

## Description

Verifies character consistency, detects plot contradictions, and tracks foreshadowing across all chapters. Uses `session_search` for retrieving relevant historical context and Memory for character state comparison.

## Instructions

### Check Dimensions

#### 1. Character Consistency
Verify against character card and memory:
- **Behavior**: Does the action match the character's established personality?
- **Knowledge**: Does the character know only what they should know?
- **Dialogue**: Does the speech pattern match the character's background?
- **Abilities**: Are powers/abilities used within established limits?

#### 2. Plot Contradiction Detection
- **Timeline**: Do events occur in the correct order?
- **Causality**: Does effect follow cause logically?
- **Location**: Are characters where they should be?
- **Inventory**: Do characters have items they previously lost/gained?

#### 3. Foreshadowing Tracking
Maintain a running list:
- Open hooks: foreshadowing planted but not yet resolved
- Resolved hooks: foreshadowing that has paid off
- Stale hooks: unresolved for more than 5 chapters (flag as warning)

### Workflow

1. Load the chapter to check
2. Use `session_search` to find relevant past context
3. Load character memory states
4. Run all 3 check dimensions
5. Generate a formatted report

### Report Format
```markdown
## Continuity Check Report - chXXX

### Issues Found: N

| Severity | Type | Description | Suggested Fix |
|----------|------|-------------|---------------|
| HIGH | Character | ... | ... |
| MED | Plot | ... | ... |
| LOW | Foreshadowing | ... | ... |

### All Clear
- Character consistency: ✓
- Plot coherence: ✓
- Foreshadowing: N open, M resolved
```

## Tools Required
- `session_search` for historical context retrieval
- Memory for character/plot state
- Read/Write file system
