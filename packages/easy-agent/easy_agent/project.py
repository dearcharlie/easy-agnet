"""Project management for Easy-Agent novel projects."""

import os
import shutil
from datetime import datetime
from pathlib import Path

from easy_agent.config import get_projects_dir, load_config

TEMPLATES_DIR = Path(__file__).resolve().parent.parent.parent / "templates"

PROJECT_STRUCTURE = [
    "world-setting",
    "characters",
    "outline/volumes",
    "chapters",
    "drafts",
    "notes",
]


def init_project(name: str) -> Path:
    projects_dir = get_projects_dir()
    project_path = projects_dir / name

    if project_path.exists():
        raise FileExistsError(f"Project '{name}' already exists at {project_path}")

    project_path.mkdir(parents=True, exist_ok=True)

    for subdir in PROJECT_STRUCTURE:
        (project_path / subdir).mkdir(parents=True, exist_ok=True)

    hermes_context_src = TEMPLATES_DIR / "hermes-context.md"
    if hermes_context_src.exists():
        shutil.copy(hermes_context_src, project_path / ".hermes.md")

    # create _index.md for characters
    (project_path / "characters" / "_index.md").write_text(
        "# 角色关系总览\n\n<!-- 此文件自动维护角色关系 -->\n"
    )

    # create empty outline index
    (project_path / "outline" / "outline.md").write_text(
        f"# 《{name}》大纲\n\n> 创建于 {datetime.now().strftime('%Y-%m-%d')}\n\n## 分卷\n\n"
    )

    print(f"[✓] Project '{name}' created at {project_path}")
    return project_path


def list_projects() -> list[dict]:
    projects_dir = get_projects_dir()
    if not projects_dir.exists():
        return []

    projects = []
    for item in sorted(projects_dir.iterdir()):
        if item.is_dir() and not item.name.startswith("."):
            chapters_dir = item / "chapters"
            draft_dir = item / "drafts"
            chapter_count = len(list(chapters_dir.glob("ch*.md"))) if chapters_dir.exists() else 0
            draft_count = len(list(draft_dir.glob("ch*.draft.md"))) if draft_dir.exists() else 0
            projects.append({
                "name": item.name,
                "path": str(item),
                "chapters": chapter_count,
                "drafts": draft_count,
            })
    return projects


def delete_project(name: str, force: bool = False) -> bool:
    projects_dir = get_projects_dir()
    project_path = projects_dir / name

    if not project_path.exists():
        raise FileNotFoundError(f"Project '{name}' not found")

    if not force:
        confirm = input(f"Delete project '{name}' and all its data? [y/N] ")
        if confirm.lower() != "y":
            print("Cancelled.")
            return False

    shutil.rmtree(project_path)
    print(f"[✓] Project '{name}' deleted.")
    return True


def get_next_chapter_number(project_path: Path) -> int:
    chapters_dir = project_path / "chapters"
    if not chapters_dir.exists():
        return 1

    existing = [f.stem for f in chapters_dir.glob("ch*.md")]
    numbers = []
    for name in existing:
        try:
            num = int(name.replace("ch", ""))
            numbers.append(num)
        except ValueError:
            continue

    return max(numbers) + 1 if numbers else 1
