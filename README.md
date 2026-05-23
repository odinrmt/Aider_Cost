# Aider Stats

Analyze your Aider chat history costs and token usage across multiple projects.

## Features

- **Project-wise Analysis**: See costs and token usage aggregated by project.
- **Daily Breakdown**: Track your spending and token consumption day by day.
- **Global Summary**: Get an overview of your total usage, including average costs per session, day, and week.
- **Recursive Scanning**: Automatically find all `.aider.chat.history.md` files in a directory tree.

## Installation

This project uses `uv` for dependency management.

```bash
uv sync
```

## Usage

### Analyze a specific history file
By default, it looks for `.aider.chat.history.md` in the current directory:
```bash
uv run aider-stats
```

Or specify a file:
```bash
uv run aider-stats --file /path/to/your/.aider.chat.history.md
```

### Scan a directory for multiple projects
```bash
uv run aider-stats --scan /path/to/projects/folder
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
