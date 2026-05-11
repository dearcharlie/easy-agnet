"""Continuity checking module for novel chapters."""

import subprocess
from pathlib import Path

from easy_agent.project import get_projects_dir

CHECK_DIMENSIONS = [
    "character_consistency",
    "plot_contradiction",
    "foreshadowing_tracking",
]


def _session_search(query: str) -> str:
    """Search historical sessions using Hermes session_search."""
    try:
        result = subprocess.run(
            ["hermes", "session_search", query],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""


def check_chapter(project_name: str, chapter_number: int) -> dict:
    """Run all continuity checks on a specific chapter.

    Args:
        project_name: Name of the novel project
        chapter_number: Chapter number to check

    Returns:
        Report dict with findings per dimension
    """
    projects_dir = get_projects_dir()
    project_path = projects_dir / project_name

    # Locate the chapter file
    ch_path = project_path / "chapters" / f"ch{chapter_number:03d}.md"
    if not ch_path.exists():
        ch_path = project_path / "drafts" / f"ch{chapter_number:03d}.draft.md"
    if not ch_path.exists():
        raise FileNotFoundError(f"Chapter {chapter_number} not found")

    chapter_text = ch_path.read_text()

    # Load continuity-check skill
    subprocess.run(["hermes", "load", "novel/continuity-check"], capture_output=True)

    # Search for relevant context
    context = _session_search(f"character states before chapter {chapter_number}")
    foreshadowing = _session_search("open foreshadowing hooks")

    report = {
        "chapter": chapter_number,
        "project": project_name,
        "findings": [],
        "summary": {
            "character_consistency": {"status": "ok", "issues": []},
            "plot_contradiction": {"status": "ok", "issues": []},
            "foreshadowing_tracking": {"status": "ok", "issues": []},
        },
    }

    # Check 1: Character Consistency
    consistency_prompt = (
        f"Check character consistency in the following chapter. "
        f"Context from memory: {context[:1000]}\n\n"
        f"Chapter text:\n{chapter_text}\n\n"
        f"Rules:\n"
        f"- Does each character act according to their established personality?\n"
        f"- Does each character know only what they should know?\n"
        f"- Are abilities used within established limits?\n"
        f"List any HIGH or MEDIUM severity issues."
    )
    consistency_result = _session_search(consistency_prompt)
    if "issue" in consistency_result.lower() or "inconsistency" in consistency_result.lower():
        report["summary"]["character_consistency"]["status"] = "issues_found"
        report["summary"]["character_consistency"]["issues"].append(consistency_result)

    # Check 2: Plot Contradiction
    contradiction_prompt = (
        f"Check plot contradictions in this chapter: {chapter_text[:2000]}\n\n"
        f"Consider:\n"
        f"- Timeline consistency\n"
        f"- Causal relationships\n"
        f"- Item/ability continuity\n"
        f"- Location consistency"
    )
    contradiction_result = _session_search(contradiction_prompt)
    if "contradiction" in contradiction_result.lower() or "inconsistency" in contradiction_result.lower():
        report["summary"]["plot_contradiction"]["status"] = "issues_found"
        report["summary"]["plot_contradiction"]["issues"].append(contradiction_result)

    # Check 3: Foreshadowing Tracking
    foreshadowing_prompt = (
        f"Track foreshadowing in this chapter.\n"
        f"Open hooks: {foreshadowing[:1000]}\n\n"
        f"Chapter text: {chapter_text[:2000]}\n\n"
        f"Identify:\n"
        f"- New foreshadowing planted\n"
        f"- Previously planted foreshadowing that is now resolved\n"
        f"- Foreshadowing that has been open for more than 5 chapters"
    )
    foreshadowing_result = _session_search(foreshadowing_prompt)
    report["summary"]["foreshadowing_tracking"]["issues"].append(foreshadowing_result)

    # Build findings list
    for dim, data in report["summary"].items():
        if data["issues"]:
            report["findings"].append({
                "dimension": dim,
                "severity": "HIGH" if dim == "character_consistency" else "MED",
                "detail": data["issues"][0][:200],
            })

    return report


def format_report(report: dict) -> str:
    """Format a continuity check report as readable text."""
    lines = []
    lines.append(f"## Continuity Check Report - Chapter {report['chapter']}")
    lines.append(f"**Project**: {report['project']}")
    lines.append("")

    if report["findings"]:
        lines.append(f"### Issues Found: {len(report['findings'])}")
        lines.append("")
        lines.append("| Severity | Type | Detail |")
        lines.append("|----------|------|--------|")
        for finding in report["findings"]:
            lines.append(f"| {finding['severity']} | {finding['dimension']} | {finding['detail']} |")
    else:
        lines.append("### No issues found. All clear!")

    lines.append("")
    lines.append("### Summary")
    for dim, data in report["summary"].items():
        status_icon = "✓" if data["status"] == "ok" else "⚠"
        lines.append(f"- {status_icon} {dim}: {data['status']}")

    lines.append("")
    lines.append("---")
    lines.append("*Generated by Easy-Agent Continuity Check*")

    return "\n".join(lines)
