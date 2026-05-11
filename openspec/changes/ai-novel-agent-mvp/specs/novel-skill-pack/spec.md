## ADDED Requirements

### Requirement: Skill follows agentskills.io standard
Each novel skill SHALL follow the agentskills.io SKILL.md format with `name`, `description`, `instructions`, `tools`, and `triggers` sections.

#### Scenario: Skill file validates against spec
- **WHEN** a user inspects any skill at `~/.hermes/skills/novel/<name>/SKILL.md`
- **THEN** the file SHALL contain valid YAML frontmatter with `name`, `description` fields

### Requirement: World Builder Skill
The world-builder skill SHALL guide users through an interview-style process to construct a structured world-setting document covering era, geography, factions, and power systems.

#### Scenario: Build a complete world setting
- **WHEN** user invokes `/novel world-builder` with a novel concept
- **THEN** the skill SHALL produce `world-setting/era.md`, `world-setting/geography.md`, `world-setting/powers.md`, and `world-setting/factions.md`

### Requirement: Character Designer Skill
The character-designer skill SHALL allow creating character cards with name, role, age, personality, appearance, background, abilities, goals, relationships, and character arc.

#### Scenario: Create a character with relationships
- **WHEN** user creates a character via character-designer
- **THEN** the skill SHALL generate a YAML character card and update `characters/_index.md` with relationship entries

### Requirement: Plot Planner Skill
The plot-planner skill SHALL generate novel outlines with volume and chapter breakdowns, including pacing control and climax arrangement.

#### Scenario: Plan a multi-volume outline
- **WHEN** user requests an outline via plot-planner
- **THEN** the skill SHALL produce `outline/outline.md` with volumes, chapter list, and key plot beats

### Requirement: Chapter Writer Skill
The chapter-writer skill SHALL generate chapter text based on the outline, supporting single-chapter and parallel multi-chapter generation via `delegate_task`.

#### Scenario: Write a single chapter from outline
- **WHEN** user invokes chapter-writer for a specific chapter
- **THEN** the skill SHALL generate a chapter in `chapters/chXXX.md` with 2000-3000 characters

#### Scenario: Generate multiple chapters in parallel
- **WHEN** user invokes chapter-writer with `--parallel 3` for chapters 1-3
- **THEN** the skill SHALL use `delegate_task` to generate up to 3 chapters concurrently

### Requirement: Continuity Check Skill
The continuity-check skill SHALL verify character consistency, detect contradictions, and track foreshadowing across chapters using `session_search` and Memory.

#### Scenario: Detect character inconsistency
- **WHEN** a character references an event they did not witness
- **THEN** the continuity-check SHALL flag the contradiction with the source of truth reference

### Requirement: Style Editor Skill
The style-editor skill SHALL polish chapter text by adjusting dialogue-to-narrative ratio, pacing density, and tightening verbose passages.

#### Scenario: Polish a chapter
- **WHEN** user invokes style-editor on a chapter
- **THEN** the skill SHALL output a revised version with measurable improvements in pacing and conciseness

### Requirement: Inspiration Skill
The inspiration skill SHALL provide plot suggestions, conflict ideas, twist designs, and writer's block solutions using web search for trending themes.

#### Scenario: Get plot suggestions
- **WHEN** user invokes inspiration for a stalled scene
- **THEN** the skill SHALL return 3-5 concrete plot suggestions based on genre conventions and current story state
