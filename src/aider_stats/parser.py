from __future__ import annotations
import os
import re
from pathlib import Path
from datetime import datetime
from aider_stats.models import Session

def parse_tokens(value_str: str, unit_str: str) -> int:
    """Converts token abbreviations (k, M) into integer values.
    
    Args:
        value_str: The numeric part of the token count.
        unit_str: The unit multiplier ('k', 'm', or empty).
        
    Returns:
        The exact integer number of tokens.
    """
    val = float(value_str)
    unit = unit_str.upper()
    if unit == 'K':
        return int(val * 1000)
    if unit == 'M':
        return int(val * 1000000)
    return int(val)

def extract_date(block: str) -> datetime | None:
    """Extracts the date from a session block.
    
    Args:
        block: The raw text block of a session.
        
    Returns:
        A datetime object if a valid date is found, otherwise None.
    """
    date_match = re.search(r"^(\d{4}-\d{2}-\d{2})", block.strip())
    if not date_match:
        return None
    try:
        return datetime.strptime(date_match.group(1), "%Y-%m-%d")
    except ValueError:
        return None

def scan_for_history_files(base_dir: Path) -> list[Path]:
    """Scans a directory recursively for .aider.chat.history.md files.

    Args:
        base_dir: The root directory to start scanning from.

    Returns:
        A list of paths to history files found.
    """
    history_files = []
    ignore_dirs = {
        ".venv", "venv", "env", "node_modules", ".git",
        ".idea", "__pycache__", ".next", "dist", "build"
    }

    for root, dirs, files in os.walk(base_dir):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]

        if ".aider.chat.history.md" in files:
            history_files.append(Path(root) / ".aider.chat.history.md")

    return history_files

def parse_history_file(file_path: Path, project_name: str = "Unknown") -> list[Session]:
    """Reads and parses the Aider history file into Session objects.

    Args:
        file_path: The path to the .aider.chat.history.md file.
        project_name: The name of the project.

    Returns:
        A list of parsed Session objects.
    """
    if not file_path.exists():
        return []

    content = file_path.read_text(encoding="utf-8")
    session_blocks = content.split("# aider chat started at ")
    
    sessions: list[Session] = []
    pattern = r"> Tokens: ([0-9.]+)([kKmM]?) sent, ([0-9.]+)([kKmM]?) received\. Cost: \$([0-9.]+) message, \$([0-9.]+) session\."

    for block in session_blocks:
        if not block.strip():
            continue
            
        session_date = extract_date(block)
        if not session_date:
            continue
            
        matches = re.findall(pattern, block)
        if not matches:
            continue
            
        session_sent = sum(parse_tokens(m[0], m[1]) for m in matches)
        session_received = sum(parse_tokens(m[2], m[3]) for m in matches)
        session_cost = float(matches[-1][5])
        
        sessions.append(Session(
            date=session_date,
            project_name=project_name,
            tokens_sent=session_sent,
            tokens_received=session_received,
            cost=session_cost
        ))
        
    return sessions
