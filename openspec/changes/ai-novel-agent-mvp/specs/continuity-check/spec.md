## ADDED Requirements

### Requirement: Character consistency verification
The continuity-check SHALL verify that character actions, dialogue, and knowledge are consistent with their established personality, background, and known information.

#### Scenario: Flag out-of-character behavior
- **WHEN** a gentle character suddenly acts cruel without narrative justification
- **THEN** the check SHALL flag this as a potential inconsistency

### Requirement: Plot contradiction detection
The continuity-check SHALL detect contradictions between chapter content and established plot facts (e.g., a character died but appears in a later chapter).

#### Scenario: Detect resurrection error
- **WHEN** a character appears in chapter 5 after dying in chapter 3
- **THEN** the check SHALL flag the contradiction with reference to the death event

### Requirement: Foreshadowing tracking
The continuity-check SHALL maintain a list of open foreshadowing hooks and verify they are resolved within a reasonable chapter window.

#### Scenario: Track unresolved foreshadowing
- **WHEN** a foreshadowing hook is planted in chapter 2
- **THEN** the check SHALL note it as unresolved
- **WHEN** 5 chapters pass without resolution
- **THEN** the check SHALL warn about stale foreshadowing

### Requirement: Session search integration
The continuity-check SHALL use Hermes `session_search` (FTS5) to retrieve relevant context from historical sessions for consistency validation.

#### Scenario: Search for relevant context
- **WHEN** checking a chapter for consistency
- **THEN** the system SHALL query `session_search` for related character and plot context from prior sessions
