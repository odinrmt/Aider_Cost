from __future__ import annotations
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from rich.text import Text
from aider_stats.models import DailyStats, GlobalStats, ProjectStats

def render_project_table(console: Console, project_stats: dict[str, ProjectStats]) -> None:
    """Renders the project statistics table.
    
    Args:
        console: The rich Console instance.
        project_stats: A dictionary mapping project names to ProjectStats objects.
    """
    table = Table(title="Cost per Project", box=box.ROUNDED)
    table.add_column("Project", justify="left", style="cyan")
    table.add_column("Sessions", justify="center", style="magenta")
    table.add_column("Tokens Sent", justify="right", style="blue")
    table.add_column("Tokens Received", justify="right", style="blue")
    table.add_column("Total Cost", justify="right", style="red bold")

    sorted_projects = sorted(project_stats.items(), key=lambda item: item[1].cost, reverse=True)

    for project_name, stats in sorted_projects:
        table.add_row(
            project_name,
            str(stats.sessions_count),
            f"{stats.tokens_sent:,}".replace(",", " "),
            f"{stats.tokens_received:,}".replace(",", " "),
            f"${stats.cost:.4f}"
        )

    console.print(table)
    console.print()

def render_summary(console: Console, stats: GlobalStats) -> None:
    """Renders the global summary panel.
    
    Args:
        console: The rich Console instance.
        stats: The GlobalStats object to display.
    """
    avg_per_session = stats.total_cost / stats.total_sessions if stats.total_sessions > 0 else 0
    avg_per_active_day = stats.total_cost / stats.active_days if stats.active_days > 0 else 0
    weeks_span = max(1.0, stats.days_span / 7.0)
    avg_per_week = stats.total_cost / weeks_span

    summary_text = Text()
    summary_text.append("Analyzed period: ", style="bold")
    summary_text.append(f"{stats.min_date.strftime('%d/%m/%Y')} to {stats.max_date.strftime('%d/%m/%Y')} ({stats.days_span} days)\n\n")
    
    summary_table = Table(box=box.SIMPLE, show_header=False)
    summary_table.add_column("Metric", style="cyan bold")
    summary_table.add_column("Value", style="green bold", justify="right")
    
    summary_table.add_row("Total Sessions", str(stats.total_sessions))
    summary_table.add_row("Total Tokens Sent", f"{stats.total_sent:,}".replace(",", " "))
    summary_table.add_row("Total Tokens Received", f"{stats.total_received:,}".replace(",", " "))
    summary_table.add_row("Total Cost", f"${stats.total_cost:.4f}")
    summary_table.add_row("---", "---")
    summary_table.add_row("Avg Cost / Session", f"${avg_per_session:.4f}")
    summary_table.add_row("Avg Cost / Active Day", f"${avg_per_active_day:.4f}")
    summary_table.add_row("Avg Cost / Week", f"${avg_per_week:.4f}")

    console.print()
    console.print(Panel(summary_table, title="[bold blue]📊 Aider Global Summary[/bold blue]", expand=False))
    console.print()

def render_daily_table(console: Console, daily_stats: dict[datetime, DailyStats]) -> None:
    """Renders the detailed daily statistics table.
    
    Args:
        console: The rich Console instance.
        daily_stats: A dictionary mapping dates to DailyStats objects.
    """
    daily_table = Table(title="🗓️  Daily Cost and Token Details", box=box.ROUNDED)
    daily_table.add_column("Date", justify="left", style="cyan", no_wrap=True)
    daily_table.add_column("Sessions", justify="center", style="magenta")
    daily_table.add_column("Tokens Sent", justify="right", style="blue")
    daily_table.add_column("Tokens Received", justify="right", style="blue")
    daily_table.add_column("Daily Cost", justify="right", style="red bold")

    for date in sorted(daily_stats.keys()):
        stats = daily_stats[date]
        daily_table.add_row(
            date.strftime("%Y-%m-%d"),
            str(stats.sessions_count),
            f"{stats.tokens_sent:,}".replace(",", " "),
            f"{stats.tokens_received:,}".replace(",", " "),
            f"${stats.cost:.4f}"
        )

    console.print(daily_table)
    console.print()
