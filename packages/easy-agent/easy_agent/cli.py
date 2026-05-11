"""CLI entry point for Easy-Agent."""

import argparse
import sys

from easy_agent import __version__
from easy_agent.modes import (
    mode_quick,
    mode_craft,
    mode_outline,
    mode_continue,
    mode_polish,
    mode_inspire,
)
from easy_agent.project import init_project, list_projects, delete_project
from easy_agent.parallel import batch_generate_all_pending
from easy_agent.continuity import check_chapter, format_report


def main():
    parser = argparse.ArgumentParser(
        prog="easy-agent",
        description="Easy-Agent: AI Novel Writing Assistant",
    )
    parser.add_argument("--version", action="version", version=f"easy-agent {__version__}")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # init
    init_parser = subparsers.add_parser("init", help="Initialize a new novel project")
    init_parser.add_argument("name", help="Project name")

    # list
    subparsers.add_parser("list", help="List all projects")

    # delete
    delete_parser = subparsers.add_parser("delete", help="Delete a project")
    delete_parser.add_argument("name", help="Project name")
    delete_parser.add_argument("--force", action="store_true", help="Skip confirmation")

    # novel quick
    quick_parser = subparsers.add_parser("quick", help="Quick Write: concept to outline + chapter")
    quick_parser.add_argument("project", nargs="?", help="Project name")
    quick_parser.add_argument("concept", nargs="?", help="Novel concept description")

    # novel craft
    craft_parser = subparsers.add_parser("craft", help="Craft Mode: turn-by-turn writing")
    craft_parser.add_argument("project", nargs="?", help="Project name")

    # novel outline
    outline_parser = subparsers.add_parser("outline", help="Outline Mode: plan then write")
    outline_parser.add_argument("project", nargs="?", help="Project name")

    # novel continue
    continue_parser = subparsers.add_parser("continue", help="Continue Mode: write next chapter")
    continue_parser.add_argument("project", nargs="?", help="Project name")

    # novel polish
    polish_parser = subparsers.add_parser("polish", help="Polish Mode: style optimization")
    polish_parser.add_argument("project", nargs="?", help="Project name")
    polish_parser.add_argument("--chapter", type=int, help="Chapter number to polish")

    # novel inspire
    inspire_parser = subparsers.add_parser("inspire", help="Inspire Mode: plot suggestions")
    inspire_parser.add_argument("project", nargs="?", help="Project name")

    # parallel
    parallel_parser = subparsers.add_parser("parallel", help="Generate multiple chapters in parallel")
    parallel_parser.add_argument("project", help="Project name")
    parallel_parser.add_argument("from", dest="from_ch", type=int, help="Starting chapter")
    parallel_parser.add_argument("to", dest="to_ch", type=int, help="Ending chapter")

    # check
    check_parser = subparsers.add_parser("check", help="Continuity check a chapter")
    check_parser.add_argument("project", nargs="?", help="Project name")
    check_parser.add_argument("--chapter", type=int, help="Chapter number to check")

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return

    try:
        _execute(args)
    except Exception as e:
        print(f"[!] Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


def _execute(args):
    if args.command == "init":
        init_project(args.name)

    elif args.command == "list":
        projects = list_projects()
        if not projects:
            print("No projects found.")
            return
        print(f"\n{'Name':<20} {'Chapters':<12} {'Drafts':<10}")
        print("-" * 42)
        for p in projects:
            print(f"{p['name']:<20} {p['chapters']:<12} {p['drafts']:<10}")

    elif args.command == "delete":
        delete_project(args.name, force=args.force)

    elif args.command == "quick":
        if args.project and args.concept:
            mode_quick(args.project, args.concept)
        elif args.project:
            concept = input("Enter your novel concept: ").strip()
            mode_quick(args.project, concept)
        else:
            print("Usage: easy-agent quick <project-name> <concept>")
            print("   or: easy-agent quick <project-name>  (will prompt for concept)")

    elif args.command == "craft":
        mode_craft(args.project)

    elif args.command == "outline":
        mode_outline(args.project)

    elif args.command == "continue":
        mode_continue(args.project)

    elif args.command == "polish":
        mode_polish(args.project, args.chapter)

    elif args.command == "inspire":
        mode_inspire(args.project)

    elif args.command == "parallel":
        results = batch_generate_all_pending(args.project, args.from_ch, args.to_ch)
        success = [r for r in results if r["status"] == "completed"]
        failed = [r for r in results if r["status"] == "failed"]
        print(f"[✓] Parallel generation complete: {len(success)} succeeded, {len(failed)} failed")
        for r in success:
            print(f"    - Chapter (file: {r.get('file_path', 'unknown')})")
        for r in failed:
            print(f"    - Chapter {r['task_id']}: {r.get('error', 'unknown error')}")

    elif args.command == "check":
        report = check_chapter(args.project, args.chapter)
        print(format_report(report))


if __name__ == "__main__":
    main()
