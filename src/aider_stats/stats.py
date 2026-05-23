from __future__ import annotations
from collections import defaultdict
from datetime import datetime
from aider_stats.models import Session, DailyStats, GlobalStats, ProjectStats


def aggregate_project_stats(sessions: list[Session]) -> dict[str, ProjectStats]:
    """Aggregates individual sessions into project statistics.

    Args:
        sessions: A list of Session objects.

    Returns:
        A dictionary mapping project names to ProjectStats objects.
    """
    project_stats: dict[str, ProjectStats] = defaultdict(ProjectStats)

    for session in sessions:
        stats = project_stats[session.project_name]
        stats.sessions_count += 1
        stats.tokens_sent += session.tokens_sent
        stats.tokens_received += session.tokens_received
        stats.cost += session.cost

    return dict(project_stats)


def aggregate_daily_stats(sessions: list[Session]) -> dict[datetime, DailyStats]:
    """Aggregates individual sessions into daily statistics.

    Args:
        sessions: A list of Session objects.

    Returns:
        A dictionary mapping dates to DailyStats objects.
    """
    daily_stats: dict[datetime, DailyStats] = defaultdict(DailyStats)

    for session in sessions:
        stats = daily_stats[session.date]
        stats.sessions_count += 1
        stats.tokens_sent += session.tokens_sent
        stats.tokens_received += session.tokens_received
        stats.cost += session.cost

    return dict(daily_stats)


def calculate_global_stats(
    daily_stats: dict[datetime, DailyStats],
) -> GlobalStats | None:
    """Calculates overall statistics from daily aggregates.

    Args:
        daily_stats: A dictionary mapping dates to DailyStats objects.

    Returns:
        A GlobalStats object, or None if no data is provided.
    """
    if not daily_stats:
        return None

    dates = list(daily_stats.keys())
    min_date = min(dates)
    max_date = max(dates)
    days_span = (max_date - min_date).days + 1

    total_sessions = sum(stats.sessions_count for stats in daily_stats.values())
    total_sent = sum(stats.tokens_sent for stats in daily_stats.values())
    total_received = sum(stats.tokens_received for stats in daily_stats.values())
    total_cost = sum(stats.cost for stats in daily_stats.values())

    return GlobalStats(
        min_date=min_date,
        max_date=max_date,
        total_sessions=total_sessions,
        total_sent=total_sent,
        total_received=total_received,
        total_cost=total_cost,
        active_days=len(daily_stats),
        days_span=days_span,
    )
