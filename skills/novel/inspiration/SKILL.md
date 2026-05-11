---
name: novel/inspiration
description: 情节建议、冲突点子、转折设计、卡文突破
version: 0.1.0
agents: true
memory: true
web_search: true
---

# Inspiration Skill

## Description

Provides plot suggestions, conflict ideas, twist designs, and writer's block solutions. Uses web search for trending themes and genre conventions, and memory for current story state.

## Instructions

### Input Analysis
When invoked, determine:
- Current story state (from memory)
- Where the writer is stuck
- Genre and tone of the novel
- Recent chapters' content (last 3)

### Suggestion Types

#### 1. Plot Suggestions
- **Conflict Seeds**: Introduce a new conflict based on existing character relationships
- **Subplot Hooks**: Side stories that enrich the main narrative
- **Escalation Paths**: Ways to raise stakes from current situation

#### 2. Twist Designs
- **Character Reveal**: A character's hidden identity or motivation
- **Setting Twist**: A truth about the world the characters discover
- **Plot Reversal**: The situation is not what it seemed

#### 3. Writer's Block Solutions
- **Skip Forward**: Write a later scene and come back
- **Change POV**: Show the scene from another character's perspective
- **Add Obstacle**: Introduce an unexpected complication
- **Time Skip**: Move past the stuck point

#### 4. Trending Themes (with Web Search)
Search for popular themes in the novel's genre:
- Recent popular plot devices
- Reader expectations for the genre
- Current trends on major platforms

### Output Format
Present 3-5 concrete suggestions per request. Each suggestion should include:
- **Idea**: One-sentence description
- **Why It Works**: Connection to current story
- **How to Implement**: Brief execution guide
- **Risk**: Potential pitfalls to avoid

## Tools Required
- Memory for current story context
- Web Search for trending themes
