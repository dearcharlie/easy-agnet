## ADDED Requirements

### Requirement: Parallel chapter generation via delegate_task
The system SHALL use Hermes `delegate_task` to generate multiple chapter drafts concurrently.

#### Scenario: Generate 3 chapters in parallel
- **WHEN** user requests chapters 4, 5, 6 in parallel mode
- **THEN** the system SHALL spawn up to 3 subagent tasks via `delegate_task`
- **THEN** each subagent SHALL independently generate one chapter draft
- **THEN** all completed drafts SHALL be collected and saved to `drafts/`

### Requirement: Configurable concurrency limit
The system SHALL allow users to configure the maximum number of concurrent subagents (default 3).

#### Scenario: Override concurrency limit
- **WHEN** user sets `maxConcurrency: 2` in config
- **THEN** `delegate_task` SHALL spawn at most 2 subagents simultaneously

### Requirement: Chapter dependency ordering
When generating consecutive chapters in parallel, the system SHALL enforce that each chapter respects the outline's chapter ordering and does not skip plot points.

#### Scenario: Parallel chapters maintain sequence
- **WHEN** chapters 4 and 5 are generated in parallel
- **THEN** each chapter SHALL reference the outline but not depend on other parallel chapters' content
- **THEN** the chapter numbering SHALL be sequential and correct
