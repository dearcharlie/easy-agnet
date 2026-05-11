"""Interaction modes for Easy-Agent CLI.

Each mode maps to a /novel command that orchestrates Hermes skills.
"""

import json
import subprocess
import sys
from pathlib import Path

from easy_agent.project import get_projects_dir


def _hermes_command(cmd: list[str]) -> str:
    """Run a Hermes CLI command and return stdout."""
    try:
        result = subprocess.run(["hermes", *cmd], capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"[!] Hermes command failed: {' '.join(cmd)}", file=sys.stderr)
        print(f"    stderr: {e.stderr}", file=sys.stderr)
        return ""
    except FileNotFoundError:
        print("[!] Hermes CLI not found. Install it first.", file=sys.stderr)
        sys.exit(1)


def _load_skill(skill_name: str) -> str:
    """Load a Hermes skill by name."""
    return _hermes_command(["load", f"novel/{skill_name}"])


def _get_project_path(project_name: str | None) -> Path:
    projects_dir = get_projects_dir()
    if project_name:
        return projects_dir / project_name
    # auto-detect: use the only project if exactly one exists
    projects = list(projects_dir.iterdir()) if projects_dir.exists() else []
    projects = [p for p in projects if p.is_dir() and not p.name.startswith(".")]
    if len(projects) == 1:
        return projects[0]
    elif len(projects) == 0:
        print("[!] No projects found. Create one first: easy-agent init <name>", file=sys.stderr)
        sys.exit(1)
    else:
        print("[!] Multiple projects found. Specify one: easy-agent <mode> <project-name>", file=sys.stderr)
        sys.exit(1)


# ---- Mode Implementations ----


def mode_quick(project_name: str | None, concept: str):
    """Quick Write: given a concept, auto-generate outline + first chapter."""
    project_path = _get_project_path(project_name)

    print("[*] Quick Write mode: generating outline and first chapter...")

    world_builder_skill = _load_skill("world-builder")
    plot_planner_skill = _load_skill("plot-planner")
    chapter_writer_skill = _load_skill("chapter-writer")

    outline_cmd = f"根据以下概念生成小说大纲：{concept}"
    _hermes_command(["-m", outline_cmd])

    chapter_cmd = f"基于已生成的大纲，写出第一章，目标字数2500字"
    result = _hermes_command(["-m", chapter_cmd])

    # Save draft
    drafts_dir = project_path / "drafts"
    drafts_dir.mkdir(exist_ok=True)
    draft_path = drafts_dir / "ch001.draft.md"
    draft_path.write_text(result)
    print(f"[✓] Chapter 1 draft saved to {draft_path}")


def mode_craft(project_name: str | None):
    """Craft Mode: turn-by-turn dialogue, pause after each segment."""
    project_path = _get_project_path(project_name)

    print("[*] Craft Mode: interactive chapter crafting.")
    print("    I'll write a segment, then wait for your feedback.")
    print("    Type 'continue' to accept, edit the text, or type 'done' to finish.\n")

    paragraph_count = 0
    full_text = []

    while True:
        paragraph_count += 1
        prompt = f"这是第{paragraph_count}段的创作。基于已有内容继续：\n\n" + "\n".join(full_text[-3:]) if full_text else "开始写第一段："
        result = _hermes_command(["-m", prompt])

        print(f"\n--- 第{paragraph_count}段 ---")
        print(result)

        response = input("\n>> Your response (continue / edit / done): ").strip()
        if response.lower() == "done":
            break
        elif response.lower() == "continue":
            full_text.append(result)
        else:
            full_text.append(response)

    if full_text:
        drafts_dir = project_path / "drafts"
        ch_num = len(list((project_path / "chapters").glob("ch*.md"))) + 1
        draft_path = drafts_dir / f"ch{ch_num:03d}.draft.md"
        draft_path.write_text("\n\n".join(full_text))
        print(f"[✓] Chapter saved to {draft_path}")


def mode_outline(project_name: str | None):
    """Outline Mode: generate full outline first, then fill chapters."""
    project_path = _get_project_path(project_name)

    print("[*] Outline Mode: generating complete outline...")
    _load_skill("plot-planner")

    prompt = "请为当前小说项目生成完整的大纲，包含分卷和章纲。输出到outline/目录。"
    _hermes_command(["-m", prompt])

    print("\n[?] Outline generated. Review it, then type 'start' to begin filling chapters.")
    input("Press Enter when ready to start writing chapters...")

    num_chapters = input("How many chapters to write now? (default: 3): ").strip()
    num_chapters = int(num_chapters) if num_chapters.isdigit() else 3

    _load_skill("chapter-writer")

    for i in range(1, num_chapters + 1):
        print(f"[*] Writing chapter {i}...")
        result = _hermes_command(["-m", f"基于大纲写出第{i}章"])
        draft_path = project_path / "drafts" / f"ch{i:03d}.draft.md"
        draft_path.write_text(result)
        print(f"[✓] Chapter {i} draft saved.")


def mode_continue(project_name: str | None):
    """Continue Mode: write next chapter based on existing content."""
    project_path = _get_project_path(project_name)

    def _chapter_number(p: Path) -> int:
        try:
            return int(p.stem.replace("ch", "").split(".")[0])
        except ValueError:
            return 0

    chapters = sorted((project_path / "chapters").glob("ch*.md"), key=_chapter_number)
    drafts = sorted((project_path / "drafts").glob("ch*.draft.md"), key=_chapter_number)

    all_chapters = chapters + drafts
    last_chapter_content = all_chapters[-1].read_text()[-500:] if all_chapters else ""

    existing_numbers = {_chapter_number(p) for p in chapters} | {_chapter_number(p) for p in drafts}
    next_num = max(existing_numbers) + 1 if existing_numbers else 1

    print(f"[*] Continue Mode: writing chapter {next_num}...")

    _load_skill("chapter-writer")
    prompt = f"续写下一章（第{next_num}章）。上一章结尾：\n\n{last_chapter_content[-300:]}"
    result = _hermes_command(["-m", prompt])

    draft_path = project_path / "drafts" / f"ch{next_num:03d}.draft.md"
    draft_path.write_text(result)
    print(f"[✓] Chapter {next_num} draft saved to {draft_path}")


def mode_polish(project_name: str | None, chapter: int | None = None):
    """Polish Mode: optimize style of an existing chapter."""
    project_path = _get_project_path(project_name)

    if chapter is None:
        drafts = sorted((project_path / "drafts").glob("ch*.draft.md"))
        if drafts:
            chapter_path = drafts[-1]
            chapter = int(chapter_path.stem.replace("ch", "").split(".")[0])
        else:
            chapters = sorted((project_path / "chapters").glob("ch*.md"))
            if not chapters:
                print("[!] No chapters to polish.", file=sys.stderr)
                return
            chapter_path = chapters[-1]
            chapter = int(chapter_path.stem.replace("ch", ""))

    ch_path = project_path / "chapters" / f"ch{chapter:03d}.md"
    if not ch_path.exists():
        ch_path = project_path / "drafts" / f"ch{chapter:03d}.draft.md"
    if not ch_path.exists():
        print(f"[!] Chapter {chapter} not found.", file=sys.stderr)
        return

    print(f"[*] Polish Mode: editing chapter {chapter}...")
    _load_skill("style-editor")

    content = ch_path.read_text()
    prompt = f"润色以下章节，优化文风、精简水文、增强爽点密度。原文：\n\n{content}"
    result = _hermes_command(["-m", prompt])

    polished_path = project_path / "drafts" / f"ch{chapter:03d}.polished.md"
    polished_path.write_text(result)
    print(f"[✓] Polished chapter saved to {polished_path}")
    print("Review the polished version and approve it to replace the original.")


def mode_inspire(project_name: str | None):
    """Inspire Mode: get plot suggestions when stuck."""
    project_path = _get_project_path(project_name)

    print("[*] Inspire Mode: generating plot suggestions...")
    _load_skill("inspiration")

    chapters = sorted((project_path / "chapters").glob("ch*.md"))
    drafts = sorted((project_path / "drafts").glob("ch*.draft.md"))

    context = ""
    if chapters:
        context = chapters[-1].read_text()[-500:]
    elif drafts:
        context = drafts[-1].read_text()[-500:]

    prompt = f"根据当前故事状态，提供情节建议、冲突点子或转折设计：\n\n{context}" if context else "请提供小说创作的情节建议和灵感启发。"
    result = _hermes_command(["-m", prompt])
    print(result)
