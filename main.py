from pathlib import Path


def print_catto() -> None:
    """Print the ASCII art cat from the catto file."""
    catto_path = Path(__file__).parent / "catto"
    content = catto_path.read_text(encoding="utf-8")
    print(content)


def main() -> None:
    print_catto()


if __name__ == "__main__":
    main()
