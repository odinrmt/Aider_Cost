# Aider Stats

A professional CLI tool to analyze your Aider chat history, tracking costs and token usage across multiple projects.

## What is an Aider Chat History File?

When you use [Aider](https://aider.chat/) (the AI pair programming tool), it automatically logs your conversations, token usage, and associated costs in a markdown file named `.aider.chat.history.md`. This tool parses those files to give you comprehensive insights into your AI spending and usage patterns.

## Installation

You can install `aider-stats` globally using `pipx` (recommended):

```bash
pipx install aider-stats
```

Alternatively, you can install it using `pip`:

```bash
pip install aider-stats
```

## Usage

### Analyze a specific history file
By default, the tool looks for `.aider.chat.history.md` in the current directory:
```bash
aider-stats
```

Or specify a file explicitly:
```bash
aider-stats --file /path/to/your/.aider.chat.history.md
```

### Scan a directory for multiple projects
To analyze multiple projects at once, use the `--scan` flag:
```bash
aider-stats --scan /path/to/projects/folder
```

## Demo

<!-- INSERT_DEMO_HERE -->

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
