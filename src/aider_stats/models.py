from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Session:
    """Represents a single Aider chat session.

    Attributes:
        date: The date and time the session started.
        project_name: The name of the project.
        tokens_sent: Total tokens sent in the session.
        tokens_received: Total tokens received in the session.
        cost: Total cost of the session in USD.
    """

    date: datetime
    project_name: str
    tokens_sent: int
    tokens_received: int
    cost: float


@dataclass
class ProjectStats:
    """Aggregated statistics for a single project.

    Attributes:
        sessions_count: Number of sessions in the project.
        tokens_sent: Total tokens sent.
        tokens_received: Total tokens received.
        cost: Total cost in USD.
    """

    sessions_count: int = 0
    tokens_sent: int = 0
    tokens_received: int = 0
    cost: float = 0.0


@dataclass
class DailyStats:
    """Aggregated statistics for a single day.

    Attributes:
        sessions_count: Number of sessions in the day.
        tokens_sent: Total tokens sent.
        tokens_received: Total tokens received.
        cost: Total cost in USD.
    """

    sessions_count: int = 0
    tokens_sent: int = 0
    tokens_received: int = 0
    cost: float = 0.0


@dataclass
class GlobalStats:
    """Overall aggregated statistics for the entire history.

    Attributes:
        min_date: The earliest session date.
        max_date: The latest session date.
        total_sessions: Total number of sessions.
        total_sent: Total tokens sent.
        total_received: Total tokens received.
        total_cost: Total cost in USD.
        active_days: Number of days with at least one session.
        days_span: Total days between min_date and max_date.
    """

    min_date: datetime
    max_date: datetime
    total_sessions: int
    total_sent: int
    total_received: int
    total_cost: float
    active_days: int
    days_span: int
