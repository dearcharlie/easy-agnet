"""Parallel chapter generation via Hermes delegate_task."""

import json
import subprocess
import sys
from pathlib import Path

from easy_agent.config import load_config
from easy_agent.project import get_projects_dir


def _delegate_task(task_description: str, task_id: str) -> dict:
    """Delegate a task to a Hermes subagent."""
    try:
        result = subprocess.run(
            ["hermes", "delegate_task", task_description],
            capture_output=True,
            text=True,
            check=True,
        )
        return {
            "task_id": task_id,
            "status": "completed",
            "output": result.stdout,
        }
    except subprocess.CalledProcessError as e:
        return {
            "task_id": task_id,
            "status": "failed",
            "error": e.stderr,
        }


def generate_chapters_parallel(
    project_name: str,
    chapters: list[dict],
    max_concurrency: int | None = None,
) -> list[dict]:
    """Generate multiple chapter drafts in parallel using delegate_task.

    Args:
        project_name: Name of the project
        chapters: List of dicts with 'number' and 'outline' keys
        max_concurrency: Max parallel tasks (default from config)

    Returns:
        List of results with chapter number and file path
    """
    config = load_config()
    max_concurrency = max_concurrency or config.get("novel", {}).get("max_concurrency", 3)

    projects_dir = get_projects_dir()
    project_path = projects_dir / project_name

    if not project_path.exists():
        raise FileNotFoundError(f"Project '{project_name}' not found")

    results = []
    pending = list(chapters)

    # Load the chapter-writer skill once
    subprocess.run(["hermes", "load", "novel/chapter-writer"], capture_output=True)

    while pending:
        batch = pending[:max_concurrency]
        pending = pending[max_concurrency:]

        batch_results = []
        for ch in batch:
            task_desc = (
                f"Write chapter {ch['number']} for novel project '{project_name}'. "
                f"Outline: {ch.get('outline', 'Use project outline')}. "
                f"Word count target: {ch.get('word_count', 2500)}. "
                f"Do NOT reference other chapters being written in parallel."
            )
            result = _delegate_task(task_desc, f"ch{ch['number']:03d}")

            if result["status"] == "completed":
                draft_path = project_path / "drafts" / f"ch{ch['number']:03d}.draft.md"
                draft_path.parent.mkdir(exist_ok=True)
                draft_path.write_text(result["output"])
                result["file_path"] = str(draft_path)
            else:
                result["file_path"] = None

            batch_results.append(result)

        results.extend(batch_results)

        if pending:
            print(f"[*] Batch complete. {len(pending)} chapters remaining...")

    return results


def batch_generate_all_pending(
    project_name: str,
    from_chapter: int,
    to_chapter: int,
) -> list[dict]:
    """Generate a range of chapters in parallel batches."""
    chapters = []
    for i in range(from_chapter, to_chapter + 1):
        chapters.append({
            "number": i,
            "outline": f"Chapter {i} based on project outline",
            "word_count": 2500,
        })

    return generate_chapters_parallel(project_name, chapters)
