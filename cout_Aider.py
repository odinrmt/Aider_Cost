import re
from pathlib import Path
from collections import defaultdict
from datetime import datetime

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich import box
    from rich.text import Text
except ImportError:
    print("La bibliothèque 'rich' n'est pas installée.")
    print("Veuillez l'installer avec : pip install rich")
    exit()

def parse_tokens(value_str, unit_str):
    """Convertit les abréviations de tokens (k, M) en nombres entiers."""
    val = float(value_str)
    unit = unit_str.upper()
    if unit == 'K':
        return int(val * 1000)
    elif unit == 'M':
        return int(val * 1000000)
    return int(val)

def main():
    console = Console()
    
    # Lecture du fichier
    history_path = Path(__file__).parent / ".aider.chat.history.md"
    if not history_path.exists():
        console.print(f"[bold red]Erreur :[/bold red] Fichier {history_path.name} introuvable.")
        return

    content = history_path.read_text(encoding="utf-8")

    # Séparation par sessions (blocs démarrant par "# aider chat started at")
    session_blocks = content.split("# aider chat started at ")
    
    # Dictionnaire pour stocker les statistiques quotidiennes
    # Format: {'YYYY-MM-DD': {'cost': 0.0, 'sent': 0, 'received': 0, 'sessions': 0}}
    daily_stats = defaultdict(lambda: {'cost': 0.0, 'sent': 0, 'received': 0, 'sessions': 0})
    
    total_cost = 0.0
    total_sessions = 0
    total_sent = 0
    total_received = 0

    # Regex pour extraire les tokens et les coûts
    # Capture ex: "17", "k", "903", "", "0.05", "0.17"
    pattern = r"> Tokens: ([0-9.]+)([kKmM]?) sent, ([0-9.]+)([kKmM]?) received\. Cost: \$([0-9.]+) message, \$([0-9.]+) session\."

    for block in session_blocks:
        if not block.strip():
            continue
            
        # Extraction de la date (les 10 premiers caractères YYYY-MM-DD)
        date_str = block[:10]
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            continue # Ignore si la date n'est pas valide
            
        matches = re.findall(pattern, block)
        if not matches:
            continue
            
        # Calculer le total des tokens pour cette session
        session_sent = sum(parse_tokens(m[0], m[1]) for m in matches)
        session_received = sum(parse_tokens(m[2], m[3]) for m in matches)
        
        # Le coût de la session est la valeur "session" de la TOUTE DERNIÈRE itération du bloc
        session_cost = float(matches[-1][5])

        # Agrégation quotidienne
        daily_stats[date_str]['cost'] += session_cost
        daily_stats[date_str]['sent'] += session_sent
        daily_stats[date_str]['received'] += session_received
        daily_stats[date_str]['sessions'] += 1
        
        # Agrégation globale
        total_cost += session_cost
        total_sent += session_sent
        total_received += session_received
        total_sessions += 1

    if not daily_stats:
        console.print("[yellow]Aucune donnée de coût ou de token trouvée dans l'historique.[/yellow]")
        return

    # --- CALCUL DES MOYENNES ---
    dates = [datetime.strptime(d, "%Y-%m-%d") for d in daily_stats.keys()]
    min_date, max_date = min(dates), max(dates)
    days_span = (max_date - min_date).days + 1
    
    active_days = len(daily_stats)
    avg_per_session = total_cost / total_sessions if total_sessions > 0 else 0
    avg_per_active_day = total_cost / active_days if active_days > 0 else 0
    
    # Calcul de la moyenne par semaine (basé sur la période totale couverte)
    weeks_span = max(1, days_span / 7.0) # Évite la division par 0 ou l'exagération si < 1 semaine
    avg_per_week = total_cost / weeks_span

    # --- AFFICHAGE JOLI AVEC RICH ---
    
    # 1. Panneau de Résumé Global
    summary_text = Text()
    summary_text.append(f"Période analysée : ", style="bold")
    summary_text.append(f"{min_date.strftime('%d/%m/%Y')} au {max_date.strftime('%d/%m/%Y')} ({days_span} jours)\n\n")
    
    summary_table = Table(box=box.SIMPLE, show_header=False)
    summary_table.add_column("Métrique", style="cyan bold")
    summary_table.add_column("Valeur", style="green bold", justify="right")
    
    summary_table.add_row("Sessions Totales", str(total_sessions))
    summary_table.add_row("Total Tokens Envoyés", f"{total_sent:,}".replace(",", " "))
    summary_table.add_row("Total Tokens Reçus", f"{total_received:,}".replace(",", " "))
    summary_table.add_row("Coût Total", f"${total_cost:.4f}")
    summary_table.add_row("---", "---")
    summary_table.add_row("Coût Moyen / Session", f"${avg_per_session:.4f}")
    summary_table.add_row("Coût Moyen / Jour actif", f"${avg_per_active_day:.4f}")
    summary_table.add_row("Coût Moyen / Semaine", f"${avg_per_week:.4f}")

    console.print()
    console.print(Panel(summary_table, title="[bold blue]📊 Résumé Global Aider[/bold blue]", expand=False))
    console.print()

    # 2. Tableau Détaillé par Jour
    daily_table = Table(title="🗓️  Détail Quotidien des Coûts et Tokens", box=box.ROUNDED)
    daily_table.add_column("Date", justify="left", style="cyan", no_wrap=True)
    daily_table.add_column("Sessions", justify="center", style="magenta")
    daily_table.add_column("Tokens Envoyés", justify="right", style="blue")
    daily_table.add_column("Tokens Reçus", justify="right", style="blue")
    daily_table.add_column("Coût du Jour", justify="right", style="red bold")

    for date in sorted(daily_stats.keys()):
        stats = daily_stats[date]
        daily_table.add_row(
            date,
            str(stats['sessions']),
            f"{stats['sent']:,}".replace(",", " "),
            f"{stats['received']:,}".replace(",", " "),
            f"${stats['cost']:.4f}"
        )

    console.print(daily_table)
    console.print()

if __name__ == "__main__":
    main()