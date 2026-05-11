## ADDED Requirements

### Requirement: Project listing page
The Desktop client SHALL display a list of all novel projects under `~/easy-agent-projects/`, with create/open/delete operations.

#### Scenario: List projects on startup
- **WHEN** the Desktop client launches
- **THEN** it SHALL scan `~/easy-agent-projects/` and display all project directories
- **WHEN** user clicks "New Project"
- **THEN** it SHALL prompt for project name and create the directory structure

#### Scenario: Open a project
- **WHEN** user clicks on a project
- **THEN** the client SHALL load the project and display its chapters in the editor

### Requirement: Markdown editor with preview
The Desktop client SHALL integrate Vditor or Monaco editor for Markdown editing with side-by-side preview.

#### Scenario: Edit chapter content
- **WHEN** user opens a chapter
- **THEN** the editor SHALL display the chapter content in Markdown with live preview

### Requirement: Hermes API Server process management
The Desktop client SHALL manage the Hermes API Server process lifecycle: start on app launch, monitor with heartbeat, gracefully stop on exit.

#### Scenario: Auto-start Hermes API
- **WHEN** Desktop client starts
- **THEN** it SHALL spawn `hermes api` process on 127.0.0.1:8520
- **WHEN** the process exits unexpectedly
- **THEN** the client SHALL attempt to restart it (max 3 retries)

#### Scenario: Graceful shutdown
- **WHEN** user closes the Desktop client
- **THEN** it SHALL send SIGTERM to the Hermes API process and wait for clean shutdown

### Requirement: AI chat panel
The Desktop client SHALL provide an embedded chat panel for AI interactions, supporting all `/novel` commands and streaming SSE responses.

#### Scenario: Send message to AI
- **WHEN** user types a message in the AI chat panel
- **THEN** the client SHALL POST to `POST /v1/chat/completions` with streaming enabled
- **THEN** the response SHALL be displayed incrementally as SSE chunks arrive

### Requirement: Quick action buttons
The Desktop client SHALL expose quick action buttons for common operations: Quick Write, Continue, Polish, Check Consistency.

#### Scenario: One-click quick write
- **WHEN** user clicks "Quick Write" button with a concept entered
- **THEN** the client SHALL invoke the `/novel quick` workflow via AI chat
