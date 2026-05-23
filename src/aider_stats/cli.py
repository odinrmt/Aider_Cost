from __future__ import annotations
import argparse
from pathlib import Path
from rich.console import Console
from aider_stats.parser import parse_history_file
from aider_stats.stats import aggregate_daily_stats, calculate_global_stats
from aider_stats.ui import render_summary, render_daily_table

def main() -> None:
    """Main entry point for the CLI application."""
    parser = argparse.ArgumentParser(description="Analyze Aider chat history costs and tokens.")
    parser.add_argument(
        "--file", 
        type=Path, 
        default=Path.cwd() / ".aider.chat.history.md",
        help="Path to the .aider.chat.history.md file (defaults to current directory)"
    )
    args = parser.parse_args()
    
    console = Console()
    
    if not args.file.exists():
        console.print(f"[bold red]Error:[/bold red] File {args.file} not found.")
        return

    sessions = parse_history_file(args.file)
    if not sessions:
        console.print("[yellow]No cost or token data found in the history file.[/yellow]")
        return
        
    daily_stats = aggregate_daily_stats(sessions)
    global_stats = calculate_global_stats(daily_stats)
    
    if global_stats:
        render_summary(console, global_stats)
        render_daily_table(console, daily_stats)

if __name__ == "__main__":
    main()
