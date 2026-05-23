from __future__ import annotations
import argparse
from pathlib import Path
from rich.console import Console
from aider_stats.parser import parse_history_file, scan_for_history_files
from aider_stats.stats import (
    aggregate_daily_stats,
    calculate_global_stats,
    aggregate_project_stats,
)
from aider_stats.ui import render_summary, render_daily_table, render_project_table


def main() -> None:
    """Main entry point for the CLI application."""
    parser = argparse.ArgumentParser(
        description="Analyze Aider chat history costs and tokens."
    )
    parser.add_argument(
        "--file",
        type=Path,
        default=Path.cwd() / ".aider.chat.history.md",
        help="Path to the .aider.chat.history.md file (defaults to current directory)",
    )
    parser.add_argument(
        "--scan",
        type=Path,
        help="Path to a parent directory to scan recursively for Aider history files",
    )
    args = parser.parse_args()

    console = Console()

    if args.scan:
        if not args.scan.is_dir():
            console.print(
                f"[bold red]Error:[/bold red] Directory {args.scan} not found or is not a valid directory."
            )
            return
        files = scan_for_history_files(args.scan)
    else:
        if not args.file.exists():
            console.print(f"[bold red]Error:[/bold red] File {args.file} not found.")
            return
        files = [args.file]

    all_sessions = []
    for file in files:
        project_name = file.parent.name
        try:
            sessions = parse_history_file(file, project_name)
        except Exception as e:
            console.print(
                f"[yellow]Warning: Skipping {file} due to error: {e}[/yellow]"
            )
            continue
        all_sessions.extend(sessions)

    if not all_sessions:
        console.print("[yellow]No cost or token data found.[/yellow]")
        return

    project_stats = aggregate_project_stats(all_sessions)
    daily_stats = aggregate_daily_stats(all_sessions)
    global_stats = calculate_global_stats(daily_stats)

    if global_stats:
        render_project_table(console, project_stats)
        render_summary(console, global_stats)
        render_daily_table(console, daily_stats)


if __name__ == "__main__":
    main()
