import argparse
import random
import sys
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
    "golden": _color(178),
    "auburn": _color(124),
    "forest_green": _color(34),
    "pink_red": _color(204),
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
        ("bicolor_black_white_tuxedo", _iggy_pattern("black", "white")),
        ("bicolor_black_white_tuxedo_invert", _iggy_pattern("white", "black")),
        ("bicolor_orange_white", _bicolor_pattern("orange", "white")),
        ("bicolor_orange_white_tuxedo", _iggy_pattern("orange", "white")),
        ("bicolor_orange_white_tuxedo_invert", _iggy_pattern("white", "orange")),
        ("bicolor_gray_white", _bicolor_pattern("gray", "white")),
        ("bicolor_gray_white_tuxedo", _iggy_pattern("gray", "white")),
        ("bicolor_gray_white_tuxedo_invert", _iggy_pattern("white", "gray")),
        ("bicolor_brown_white", _bicolor_pattern("brown", "white")),
        ("bicolor_brown_white_tuxedo", _iggy_pattern("brown", "white")),
        ("bicolor_brown_white_tuxedo_invert", _iggy_pattern("white", "brown")),
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


def _iggy_pattern(color1: str, color2: str) -> PatternFunc:
    """Create a tuxedo-style bicolor pattern - color1 cap/back, color2 face/chest."""
    def apply(content: str) -> str:
        lines = content.split("\n")
        total_lines = len(lines)
        result = []

        for i, line in enumerate(lines):
            if not line.strip():
                result.append(line)
                continue

            # Find the center of the actual content (not leading spaces)
            stripped = line.lstrip()
            leading_spaces = len(line) - len(stripped)
            content_len = len(stripped)
            center = leading_spaces + content_len // 2

            colored_line = ""
            for j, char in enumerate(line):
                if char in " \t":
                    colored_line += char
                    continue

                # Calculate relative position from center
                dist_from_center = abs(j - center)
                relative_line = i / total_lines

                # Determine if this position should be color1 (back) or color2 (chest)
                is_back_color = False

                # Very top of head / ear tips (lines 0-6): all color1
                if relative_line < 0.08:
                    is_back_color = True

                # Upper head with blaze starting (lines 7-11)
                # Blaze in center (color2), color1 on sides
                elif relative_line < 0.14:
                    # Narrow blaze in center, widens as we go down
                    blaze_width = 0.08 + (relative_line - 0.08) * 0.5
                    if dist_from_center > content_len * blaze_width:
                        is_back_color = True

                # Upper face (lines 12-18): blaze widens
                elif relative_line < 0.22:
                    blaze_width = 0.12 + (relative_line - 0.14) * 0.8
                    if dist_from_center > content_len * blaze_width:
                        is_back_color = True

                # Face area (lines 18-28): color2 center, color1 edges
                elif relative_line < 0.34:
                    if dist_from_center > content_len * 0.35:
                        is_back_color = True

                # Upper body (lines 28-45): color1 back, color2 chest
                elif relative_line < 0.54:
                    if dist_from_center > content_len * 0.25:
                        is_back_color = True

                # Mid body (lines 45-60): wider color2 chest area
                elif relative_line < 0.72:
                    if dist_from_center > content_len * 0.3:
                        is_back_color = True

                # Lower body/legs (lines 60-75): color2 paws, some color1
                elif relative_line < 0.90:
                    if dist_from_center > content_len * 0.4:
                        is_back_color = True

                # Feet (lines 75+): mostly color2 paws
                else:
                    if dist_from_center > content_len * 0.45:
                        is_back_color = True

                if is_back_color:
                    colored_line += f"{CAT_COLORS[color1]}{char}{RESET}"
                else:
                    colored_line += f"{CAT_COLORS[color2]}{char}{RESET}"

            result.append(colored_line)

        return "\n".join(result)
    return apply


def for_iggy() -> None:
    """Print a black and white tuxedo cat matching Iggy's markings."""
    catto_path = Path(__file__).parent / "catto"
    content = catto_path.read_text(encoding="utf-8")
    pattern_func = _iggy_pattern("black", "white")
    colored_content = pattern_func(content)
    print(colored_content)
    print("I miss the potamus.")


def _lucy_pattern() -> PatternFunc:
    """Create Lucy's warm brown-to-golden gradient pattern."""
    def apply(content: str) -> str:
        lines = content.split("\n")
        total_lines = len(lines)
        result = []

        for i, line in enumerate(lines):
            if not line.strip():
                result.append(line)
                continue

            line_len = len(line)
            stripped = line.lstrip()
            leading_spaces = len(line) - len(stripped)
            content_len = len(stripped)
            center = leading_spaces + content_len // 2

            colored_line = ""
            for j, char in enumerate(line):
                if char in " \t":
                    colored_line += char
                    continue

                dist_from_center = abs(j - center)
                relative_line = i / total_lines

                # Determine color based on position
                # Dark brown on edges and top, golden-orange in center
                if relative_line < 0.15:
                    # Top of head - darker brown tones
                    if dist_from_center > content_len * 0.3:
                        color = "chocolate"
                    else:
                        color = "brown"
                elif relative_line < 0.35:
                    # Face area - brown with some orange
                    if dist_from_center > content_len * 0.35:
                        color = "chocolate"
                    elif dist_from_center > content_len * 0.2:
                        color = "brown"
                    else:
                        color = "ginger"
                elif relative_line < 0.65:
                    # Chest/body - golden center, brown edges
                    if dist_from_center > content_len * 0.35:
                        color = "brown"
                    elif dist_from_center > content_len * 0.2:
                        color = "ginger"
                    else:
                        color = "golden"
                elif relative_line < 0.85:
                    # Lower body - orange/golden belly
                    if dist_from_center > content_len * 0.4:
                        color = "brown"
                    elif dist_from_center > content_len * 0.25:
                        color = "orange"
                    else:
                        color = "golden"
                else:
                    # Legs/paws - brown with ginger
                    if dist_from_center > content_len * 0.35:
                        color = "brown"
                    else:
                        color = "ginger"

                colored_line += f"{CAT_COLORS[color]}{char}{RESET}"

            result.append(colored_line)

        return "\n".join(result)
    return apply


def for_lucy() -> None:
    """Print a warm brown and golden cat for Lucy."""
    catto_path = Path(__file__).parent / "catto"
    content = catto_path.read_text(encoding="utf-8")
    pattern_func = _lucy_pattern()
    colored_content = pattern_func(content)
    print(colored_content)
    print("The world's babiest.")


def for_moo() -> None:
    """Print a black cat for Magda (the moominkittycat)."""
    catto_path = Path(__file__).parent / "catto"
    content = catto_path.read_text(encoding="utf-8")
    pattern_func = _solid_pattern("black")
    colored_content = pattern_func(content)
    print(colored_content)
    print("The moominkittycat would like food.  Please.")


def _cassandra_pattern() -> PatternFunc:
    """Create Cassandra's silver tabby pattern with darker stripes and white tail tip."""
    def apply(content: str) -> str:
        lines = content.split("\n")
        total_lines = len(lines)
        result = []

        for i, line in enumerate(lines):
            if not line.strip():
                result.append(line)
                continue

            stripped = line.lstrip()
            leading_spaces = len(line) - len(stripped)
            content_len = len(stripped)
            center = leading_spaces + content_len // 2

            colored_line = ""
            for j, char in enumerate(line):
                if char in " \t":
                    colored_line += char
                    continue

                dist_from_center = abs(j - center)
                relative_line = i / total_lines

                # Tabby stripe effect based on line position
                is_stripe_line = i % 4 < 2

                # Determine color based on position
                if relative_line < 0.12:
                    # Top of head/ears - dark gray with stripes
                    if is_stripe_line:
                        color = "dark_gray"
                    else:
                        color = "gray"
                elif relative_line < 0.30:
                    # Face area - silver base with gray stripes, some tan accents
                    if dist_from_center > content_len * 0.35:
                        # Outer edges - darker
                        color = "dark_gray" if is_stripe_line else "gray"
                    elif dist_from_center > content_len * 0.2:
                        # Mid face - silver with stripes
                        color = "gray" if is_stripe_line else "silver"
                    else:
                        # Center face - silver with light brown accent
                        if is_stripe_line and i % 6 < 2:
                            color = "fawn"
                        else:
                            color = "silver"
                elif relative_line < 0.55:
                    # Upper body - silver with tabby stripes
                    if dist_from_center > content_len * 0.4:
                        color = "dark_gray" if is_stripe_line else "gray"
                    elif dist_from_center > content_len * 0.25:
                        color = "gray" if is_stripe_line else "silver"
                    else:
                        # Chest area - lighter silver
                        color = "light_gray" if is_stripe_line else "silver"
                elif relative_line < 0.75:
                    # Mid body/belly - silver with stripes and tan patches
                    if dist_from_center > content_len * 0.35:
                        color = "dark_gray" if is_stripe_line else "gray"
                    elif dist_from_center > content_len * 0.2:
                        # Add subtle tan patches
                        if i % 7 < 2:
                            color = "fawn"
                        elif is_stripe_line:
                            color = "gray"
                        else:
                            color = "silver"
                    else:
                        color = "silver"
                elif relative_line < 0.90:
                    # Lower body/legs - gray tabby pattern
                    if is_stripe_line:
                        color = "dark_gray"
                    else:
                        color = "silver"
                else:
                    # Tail/feet area - white-tipped tail
                    if dist_from_center < content_len * 0.15:
                        # Tail tip - white
                        color = "white"
                    elif is_stripe_line:
                        color = "gray"
                    else:
                        color = "silver"

                colored_line += f"{CAT_COLORS[color]}{char}{RESET}"

            result.append(colored_line)

        return "\n".join(result)
    return apply


def for_cassandra() -> None:
    """Print a silver tabby cat for Cassandra."""
    catto_path = Path(__file__).parent / "catto"
    content = catto_path.read_text(encoding="utf-8")
    pattern_func = _cassandra_pattern()
    colored_content = pattern_func(content)
    print(colored_content)
    print("The babiest brioche loaf you ever saw.")


def _persephone_pattern() -> PatternFunc:
    """Create Persephone's silver and white bicolor pattern."""
    def apply(content: str) -> str:
        lines = content.split("\n")
        total_lines = len(lines)
        result = []

        for i, line in enumerate(lines):
            if not line.strip():
                result.append(line)
                continue

            stripped = line.lstrip()
            leading_spaces = len(line) - len(stripped)
            content_len = len(stripped)
            center = leading_spaces + content_len // 2

            colored_line = ""
            for j, char in enumerate(line):
                if char in " \t":
                    colored_line += char
                    continue

                dist_from_center = abs(j - center)
                relative_line = i / total_lines

                # Determine color based on position
                # Gray/silver on back and sides, white on chest/belly/paws
                if relative_line < 0.10:
                    # Top of head/ears - darker gray
                    if dist_from_center > content_len * 0.3:
                        color = "dark_gray"
                    else:
                        color = "gray"
                elif relative_line < 0.25:
                    # Face area - gray on sides, lighter in center
                    if dist_from_center > content_len * 0.35:
                        color = "dark_gray"
                    elif dist_from_center > content_len * 0.2:
                        color = "gray"
                    else:
                        color = "silver"
                elif relative_line < 0.45:
                    # Upper chest - white center, gray sides
                    if dist_from_center > content_len * 0.35:
                        color = "gray"
                    elif dist_from_center > content_len * 0.2:
                        color = "silver"
                    else:
                        color = "white"
                elif relative_line < 0.70:
                    # Chest and belly - prominent white center
                    if dist_from_center > content_len * 0.4:
                        color = "gray"
                    elif dist_from_center > content_len * 0.25:
                        color = "light_gray"
                    else:
                        color = "white"
                elif relative_line < 0.88:
                    # Lower body - white belly, gray back
                    if dist_from_center > content_len * 0.35:
                        color = "gray"
                    elif dist_from_center > content_len * 0.2:
                        color = "silver"
                    else:
                        color = "white"
                else:
                    # Paws - white
                    if dist_from_center > content_len * 0.4:
                        color = "silver"
                    else:
                        color = "white"

                colored_line += f"{CAT_COLORS[color]}{char}{RESET}"

            result.append(colored_line)

        return "\n".join(result)
    return apply


def for_persephone() -> None:
    """Print a silver and white bicolor cat for Persephone."""
    catto_path = Path(__file__).parent / "catto"
    content = catto_path.read_text(encoding="utf-8")
    pattern_func = _persephone_pattern()
    colored_content = pattern_func(content)
    print(colored_content)
    print("Miss independent snugglemonster, Percypie herself.")


def _jennycatto_pattern() -> PatternFunc:
    """Create Jenny's pattern - forest green cat, pink/red heart."""
    # The blank braille character used for spacing
    blank_braille = "⠀"

    # Define where the heart starts on each line (0-indexed line: column)
    # These boundaries were determined by analyzing the hearto file structure
    heart_boundaries: dict[int, int] = {
        4: 28,  # File line 5: heart starts at column 29
        5: 28,  # File line 6: heart starts at column 28
        6: 28,  # File line 7: heart starts at column 28
        7: 30,  # File line 8: heart starts at column 31
        8: 32,  # File line 9: heart starts at column 32 (column 31 is whisker)
    }

    def apply(content: str) -> str:
        lines = content.split("\n")
        result = []

        for i, line in enumerate(lines):
            colored_line = ""
            for j, char in enumerate(line):
                # Skip blank braille characters (spacing)
                if char == blank_braille:
                    colored_line += char
                    continue

                # Check if this position is in the heart region
                is_heart = i in heart_boundaries and j >= heart_boundaries[i]

                if is_heart:
                    colored_line += f"{CAT_COLORS['pink_red']}{char}{RESET}"
                else:
                    colored_line += f"{CAT_COLORS['forest_green']}{char}{RESET}"

            result.append(colored_line)

        return "\n".join(result)
    return apply


def for_jennycatto() -> None:
    """Print the hearto ASCII art for Jenny."""
    hearto_path = Path(__file__).parent / "hearto"
    content = hearto_path.read_text(encoding="utf-8")
    pattern_func = _jennycatto_pattern()
    colored_content = pattern_func(content)
    print(colored_content)
    print("For my love.")
    print("The heart of the catto family.")
    print("I hope we have a fantastic Valentines Day, and a fantastic 100 more Valentines days together.")

CAT_NAMES = ["iggy", "magda", "lucy", "cassandra", "persephone", "jennycatto"]


class CatHelpFormatter(argparse.HelpFormatter):
    """Custom help formatter with wider option column."""

    def __init__(self, prog: str) -> None:
        super().__init__(prog, max_help_position=30)


class CatArgumentParser(argparse.ArgumentParser):
    """Custom argument parser with cat-specific error messages."""

    def error(self, message: str) -> NoReturn:
        """Override error to provide custom message for mutual exclusivity."""
        if "not allowed with argument" in message:
            self.exit(
                2,
                "You cannot call multiple cats!  "
                "You must pick one cat flag only.\n",
            )
        if "unrecognized arguments" in message:
            self.print_help(sys.stderr)
            self.exit(2, f"\nError: {message}\n")
        super().error(message)


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = CatArgumentParser(
        description="Display a colorful ASCII cat.",
        formatter_class=CatHelpFormatter,
    )

    cat_group = parser.add_mutually_exclusive_group()
    cat_group.add_argument(
        "--iggy", "--ignatius",
        action="store_true",
        help="Display a black and white bicolor cat for Iggy",
    )
    cat_group.add_argument(
        "--lucy", "--lucrezia",
        action="store_true",
        help="Display a brown tabby cat for Lucy",
    )
    cat_group.add_argument(
        "--magda", "--moo",
        action="store_true",
        help="Display a black cat for Magda the moominkittycat",
    )
    cat_group.add_argument(
        "--cassandra", "--cassie",
        action="store_true",
        help="Display a silver tabby cat for Cassandra",
    )
    cat_group.add_argument(
        "--persephone", "--percy",
        action="store_true",
        help="Display a silver and white bicolor cat for Persephone",
    )
    cat_group.add_argument(
        "--jennycatto",
        action="store_true",
        help="Display a message for my love.",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.iggy:
        for_iggy()
    elif args.lucy:
        for_lucy()
    elif args.magda:
        for_moo()
    elif args.cassandra:
        for_cassandra()
    elif args.persephone:
        for_persephone()
    elif args.jennycatto:
        for_jennycatto()
    else:
        print_catto()


if __name__ == "__main__":
    main()
