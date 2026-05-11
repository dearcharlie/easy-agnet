## ADDED Requirements

### Requirement: Project directory structure
Each novel project SHALL be a directory under `~/easy-agent-projects/` following a defined directory layout: `world-setting/`, `characters/`, `outline/`, `chapters/`, `drafts/`, `notes/`, and `.hermes.md`.

#### Scenario: Initialize a new project
- **WHEN** user creates a new novel project
- **THEN** the system SHALL create the full directory structure under `~/easy-agent-projects/<项目名>/` with all required subdirectories

### Requirement: `.hermes.md` project context
The `.hermes.md` file SHALL contain project metadata (type, target word count, update frequency, target platform), writing conventions, and important agreements.

#### Scenario: Auto-load project context
- **WHEN** user switches to a novel project
- **THEN** Hermes SHALL automatically load `.hermes.md` as context for all subsequent interactions

### Requirement: Character card template
Character cards SHALL be stored as YAML frontmatter Markdown files in `characters/`, supporting fields: name, role, age, personality, appearance, background, abilities, goals, relationships, arc.

#### Scenario: Read character card
- **WHEN** user views a character card
- **THEN** the system SHALL display all required fields in a structured format

### Requirement: Chapter file format
Chapter files SHALL be named `chXXX.md` and contain a Markdown title `# 第X章 <标题>` followed by chapter body text.

#### Scenario: Write first chapter
- **WHEN** user generates chapter 1
- **THEN** the system SHALL create `chapters/ch001.md` with proper chapter heading

### Requirement: Multi-chapter drafts directory
Unapproved chapter drafts SHALL reside in `drafts/` with a `drafts/chXXX.draft.md` naming convention, keeping approved chapters and drafts separate.

#### Scenario: Draft vs approved separation
- **WHEN** a chapter is generated but not yet approved
- **THEN** it SHALL be stored in `drafts/chXXX.draft.md`
- **WHEN** the user approves the chapter
- **THEN** it SHALL be moved to `chapters/chXXX.md`
