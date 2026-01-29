import argparse
import random
from pathlib import Path
from typing import Callable, NoReturn

RESET = "\033[0m"


def _color(code: int) -> str:
    """Generate ANSI 256-color escape code."""
    return f"\033[38;5;{code}m"


# Realistic cat colors (ANSI 256-color codes)
CAT_COLORS = {
    "black": _color(232),
    "white": _color(255),
    "orange": _color(208),
    "ginger": _color(166),
    "cream": _color(223),
    "brown": _color(130),
    "chocolate": _color(94),
    "gray": _color(245),
    "blue_gray": _color(67),
    "lilac": _color(139),
    "cinnamon": _color(137),
    "fawn": _color(180),
    "silver": _color(250),
    "dark_orange": _color(202),
    "light_gray": _color(249),
    "dark_gray": _color(239),
}

# Pattern type alias
PatternFunc = Callable[[str], str]


def _solid_pattern(color: str) -> PatternFunc:
    """Create a solid single-color pattern."""
    def apply(content: str) -> str:
        return f"{CAT_COLORS[color]}{content}{RESET}"
    return apply


def _bicolor_pattern(color1: str, color2: str) -> PatternFunc:
    """Create a two-color pattern (like tuxedo cats)."""
    def apply(content: str) -> str:
        lines = content.split("\n")
        result = []
        for i, line in enumerate(lines):
            colored_line = ""
            for j, char in enumerate(line):
                if char in " \t\n":
                    colored_line += char
                elif (i + j) % 7 < 4:
                    colored_line += f"{CAT_COLORS[color1]}{char}{RESET}"
                else:
                    colored_line += f"{CAT_COLORS[color2]}{char}{RESET}"
            result.append(colored_line)
        return "\n".join(result)
    return apply


def _tabby_pattern(base: str, stripe: str) -> PatternFunc:
    """Create a striped tabby pattern."""
    def apply(content: str) -> str:
        lines = content.split("\n")
        result = []
        for i, line in enumerate(lines):
            if i % 3 == 0:
                result.append(f"{CAT_COLORS[stripe]}{line}{RESET}")
            else:
                result.append(f"{CAT_COLORS[base]}{line}{RESET}")
        return "\n".join(result)
    return apply


def _calico_pattern() -> PatternFunc:
    """Create a calico pattern (white, orange, black patches)."""
    colors = ["white", "orange", "black"]

    def apply(content: str) -> str:
        lines = content.split("\n")
        result = []
        for i, line in enumerate(lines):
            colored_line = ""
            patch_color = colors[(i // 5) % 3]
            for j, char in enumerate(line):
                if char in " \t\n":
                    colored_line += char
                else:
                    if j % 11 < 4:
                        colored_line += f"{CAT_COLORS['white']}{char}{RESET}"
                    elif j % 11 < 7:
                        colored_line += f"{CAT_COLORS['orange']}{char}{RESET}"
                    else:
                        colored_line += f"{CAT_COLORS[patch_color]}{char}{RESET}"
            result.append(colored_line)
        return "\n".join(result)
    return apply


def _tortoiseshell_pattern() -> PatternFunc:
    """Create a tortoiseshell pattern (black and orange mottled)."""
    def apply(content: str) -> str:
        lines = content.split("\n")
        result = []
        for i, line in enumerate(lines):
            colored_line = ""
            for j, char in enumerate(line):
                if char in " \t\n":
                    colored_line += char
                elif (i * 3 + j * 7) % 5 < 2:
                    colored_line += f"{CAT_COLORS['orange']}{char}{RESET}"
                elif (i * 3 + j * 7) % 5 < 4:
                    colored_line += f"{CAT_COLORS['black']}{char}{RESET}"
                else:
                    colored_line += f"{CAT_COLORS['ginger']}{char}{RESET}"
            result.append(colored_line)
        return "\n".join(result)
    return apply


def _colorpoint_pattern(body: str, points: str) -> PatternFunc:
    """Create a colorpoint pattern (like Siamese - light body, dark extremities)."""
    def apply(content: str) -> str:
        lines = content.split("\n")
        total_lines = len(lines)
        result = []
        for i, line in enumerate(lines):
            if i < total_lines // 5 or i > total_lines * 4 // 5:
                result.append(f"{CAT_COLORS[points]}{line}{RESET}")
            else:
                result.append(f"{CAT_COLORS[body]}{line}{RESET}")
        return "\n".join(result)
    return apply


def _smoke_pattern(color: str) -> PatternFunc:
    """Create a smoke pattern (solid with lighter roots effect)."""
    lighter = {"black": "dark_gray", "gray": "light_gray", "blue_gray": "silver"}
    light_color = lighter.get(color, "silver")

    def apply(content: str) -> str:
        lines = content.split("\n")
        result = []
        for i, line in enumerate(lines):
            colored_line = ""
            for j, char in enumerate(line):
                if char in " \t\n":
                    colored_line += char
                elif j % 4 == 0:
                    colored_line += f"{CAT_COLORS[light_color]}{char}{RESET}"
                else:
                    colored_line += f"{CAT_COLORS[color]}{char}{RESET}"
            result.append(colored_line)
        return "\n".join(result)
    return apply


def _tuxedo_pattern() -> PatternFunc:
    """Create a tuxedo pattern (black with white chest)."""
    def apply(content: str) -> str:
        lines = content.split("\n")
        total_lines = len(lines)
        result = []
        for i, line in enumerate(lines):
            line_len = len(line)
            center_start = line_len // 3
            center_end = line_len * 2 // 3
            chest_zone = total_lines // 4 < i < total_lines * 3 // 4

            colored_line = ""
            for j, char in enumerate(line):
                if char in " \t\n":
                    colored_line += char
                elif chest_zone and center_start < j < center_end:
                    colored_line += f"{CAT_COLORS['white']}{char}{RESET}"
                else:
                    colored_line += f"{CAT_COLORS['black']}{char}{RESET}"
            result.append(colored_line)
        return "\n".join(result)
    return apply


def get_random_pattern() -> tuple[str, PatternFunc]:
    """Select a random cat color pattern."""
    patterns: list[tuple[str, PatternFunc]] = [
        # Solid colors
        ("solid_black", _solid_pattern("black")),
        ("solid_white", _solid_pattern("white")),
        ("solid_orange", _solid_pattern("orange")),
        ("solid_gray", _solid_pattern("gray")),
        ("solid_cream", _solid_pattern("cream")),
        ("solid_brown", _solid_pattern("brown")),
        ("solid_chocolate", _solid_pattern("chocolate")),
        ("solid_blue_gray", _solid_pattern("blue_gray")),
        ("solid_lilac", _solid_pattern("lilac")),
        ("solid_cinnamon", _solid_pattern("cinnamon")),
        ("solid_fawn", _solid_pattern("fawn")),
        # Bicolor patterns
        ("bicolor_black_white", _bicolor_pattern("black", "white")),
        ("bicolor_orange_white", _bicolor_pattern("orange", "white")),
        ("bicolor_gray_white", _bicolor_pattern("gray", "white")),
        ("bicolor_brown_white", _bicolor_pattern("brown", "white")),
        # Tabby patterns
        ("tabby_brown", _tabby_pattern("brown", "chocolate")),
        ("tabby_orange", _tabby_pattern("orange", "ginger")),
        ("tabby_gray", _tabby_pattern("gray", "dark_gray")),
        ("tabby_silver", _tabby_pattern("silver", "gray")),
        ("tabby_cream", _tabby_pattern("cream", "fawn")),
        # Special patterns
        ("calico", _calico_pattern()),
        ("tortoiseshell", _tortoiseshell_pattern()),
        ("tuxedo", _tuxedo_pattern()),
        # Colorpoint patterns
        ("colorpoint_seal", _colorpoint_pattern("cream", "chocolate")),
        ("colorpoint_blue", _colorpoint_pattern("white", "blue_gray")),
        ("colorpoint_lilac", _colorpoint_pattern("white", "lilac")),
        # Smoke patterns
        ("smoke_black", _smoke_pattern("black")),
        ("smoke_gray", _smoke_pattern("gray")),
        ("smoke_blue", _smoke_pattern("blue_gray")),
    ]
    return random.choice(patterns)


def print_catto() -> None:
    """Print the ASCII art cat in a random realistic cat color pattern."""
    catto_path = Path(__file__).parent / "catto"
    content = catto_path.read_text(encoding="utf-8")
    pattern_name, pattern_func = get_random_pattern()
    colored_content = pattern_func(content)
    print(colored_content)


def for_iggy() -> None:
    """Print a black and white bicolor cat for Iggy."""
    catto_path = Path(__file__).parent / "catto"
    content = catto_path.read_text(encoding="utf-8")
    pattern_func = _bicolor_pattern("black", "white")
    colored_content = pattern_func(content)
    print(colored_content)
    print("I miss the potamus.")


CAT_NAMES = ["iggy", "magda", "lucy", "cassandra", "persephone"]


class CatArgumentParser(argparse.ArgumentParser):
    """Custom argument parser with cat-specific error messages."""

    def error(self, message: str) -> NoReturn:
        """Override error to provide custom message for mutual exclusivity."""
        if "not allowed with argument" in message:
            self.exit(
                2,
                "You cannot call multiple cats!  "
                "You must pick between iggy, magda, lucy, cassandra, or persephone.\n",
            )
        super().error(message)


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = CatArgumentParser(description="Display a colorful ASCII cat.")

    cat_group = parser.add_mutually_exclusive_group()
    cat_group.add_argument(
        "--iggy",
        action="store_true",
        help="Display a black and white bicolor cat for Iggy",
    )
    cat_group.add_argument(
        "--lucy",
        action="store_true",
        help="Select Lucy (currently does nothing)",
    )
    cat_group.add_argument(
        "--magda",
        action="store_true",
        help="Select Magda (currently does nothing)",
    )
    cat_group.add_argument(
        "--cassandra",
        action="store_true",
        help="Select Cassandra (currently does nothing)",
    )
    cat_group.add_argument(
        "--persephone",
        action="store_true",
        help="Select Persephone (currently does nothing)",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.iggy:
        for_iggy()
    else:
        print_catto()


if __name__ == "__main__":
    main()
