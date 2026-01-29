# Wiggleby

A command-line tool that displays ASCII art cats in various color patterns.

## Overview

Wiggleby prints a colorful ASCII cat to your terminal. By default, it randomly selects from 29 realistic cat color patterns including solid colors, bicolor, tabby, calico, tortoiseshell, tuxedo, colorpoint, and smoke patterns.

## Usage

```bash
# Display a random colored cat
uv run python main.py

# Display a specific cat
uv run python main.py --iggy
```

## Flags

| Flag | Description |
|------|-------------|
| `--iggy` | Display a black and white tuxedo cat for Iggy |
| `--lucy` | Display a warm brown and golden cat for Lucy |
| `--magda` | Display a solid black cat for Magda the moominkittycat |
| `--cassandra` | Reserved for future use |
| `--persephone` | Reserved for future use |
| `--help` | Show help message and available options |

Note: Cat flags are mutually exclusive - only one can be used at a time.

## Installation

Requires Python 3.11+ and [uv](https://github.com/astral-sh/uv).

```bash
# Install dependencies
uv sync

# Run the application
uv run python main.py
```

## Running Tests

```bash
uv run pytest
```
