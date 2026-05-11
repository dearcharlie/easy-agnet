## ADDED Requirements

### Requirement: Quick Write Mode (`/novel quick`)
The system SHALL accept a brief novel concept and automatically generate a complete outline + first chapter.

#### Scenario: One-shot novel generation
- **WHEN** user runs `/novel quick "一个程序员穿越到修仙世界，用代码修改天地规则"`
- **THEN** the system SHALL output a complete outline and first chapter within a single response

### Requirement: Craft Mode (`/novel craft`)
The system SHALL engage in turn-by-turn dialogue, pausing after each segment for user revision before continuing.

#### Scenario: Iterative chapter crafting
- **WHEN** user runs `/novel craft` and writes a paragraph
- **THEN** the system SHALL propose the next paragraph, then wait for user approval or modification before proceeding

### Requirement: Outline Mode (`/novel outline`)
The system SHALL first generate a complete outline (with volumes and chapter outlines), then fill in chapters one by one after user confirmation.

#### Scenario: Outline-then-fill workflow
- **WHEN** user runs `/novel outline`
- **THEN** the system SHALL first present a complete outline, and only generate chapters after user confirms the outline

### Requirement: Continue Mode (`/novel continue`)
The system SHALL continue writing based on existing chapters, automatically injecting context and character states.

#### Scenario: Continue from last chapter
- **WHEN** user runs `/novel continue` after 3 chapters exist
- **THEN** the system SHALL generate the next chapter using the last chapter's ending state as starting context

### Requirement: Polish Mode (`/novel polish`)
The system SHALL optimize style, tighten verbose passages, and enhance satisfying plot points on existing chapters.

#### Scenario: Polish existing chapter
- **WHEN** user runs `/novel polish` targeting chapter 2
- **THEN** the system SHALL output a revised version with identified improvements

### Requirement: Inspire Mode (`/novel inspire`)
The system SHALL provide plot suggestions, conflict ideas, and twist designs when the writer is stuck.

#### Scenario: Break through writer's block
- **WHEN** user runs `/novel inspire` describing a blocked scene
- **THEN** the system SHALL return 3-5 actionable suggestions with concrete next steps
