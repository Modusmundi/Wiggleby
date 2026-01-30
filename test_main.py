import re
from pathlib import Path

from main import (
    CAT_COLORS,
    RESET,
    _calico_pattern,
    _cassandra_pattern,
    _colorpoint_pattern,
    _iggy_pattern,
    _jennycatto_pattern,
    _persephone_pattern,
    _solid_pattern,
    _tabby_pattern,
    _tortoiseshell_pattern,
    _tuxedo_pattern,
    for_cassandra,
    for_jennycatto,
    for_persephone,
    get_random_pattern,
    print_catto,
)

ANSI_PATTERN = re.compile(r"\033\[[0-9;]+m")


def _strip_ansi(text: str) -> str:
    """Remove all ANSI escape codes from text."""
    return ANSI_PATTERN.sub("", text)


def test_print_catto_outputs_content(capsys: object) -> None:
    """Verify print_catto outputs the catto file content with color codes."""
    print_catto()
    captured = capsys.readouterr()  # type: ignore[attr-defined]

    catto_path = Path(__file__).parent / "catto"
    expected_content = catto_path.read_text(encoding="utf-8")

    # Strip ANSI codes and compare content
    stripped_output = _strip_ansi(captured.out)
    assert stripped_output.strip() == expected_content.strip()


def test_print_catto_contains_cat_features(capsys: object) -> None:
    """Verify the ASCII art contains recognizable cat features."""
    print_catto()
    captured = capsys.readouterr()  # type: ignore[attr-defined]
    output = _strip_ansi(captured.out)

    # Check for M characters that form the cat shape
    assert "MMM" in output
    assert "HHH" in output

    # Check special characters are preserved
    assert "'" in output
    assert "&&&" in output
    assert ":::" in output


def test_print_catto_preserves_structure(capsys: object) -> None:
    """Verify the ASCII art structure is preserved with correct line count."""
    print_catto()
    captured = capsys.readouterr()  # type: ignore[attr-defined]
    output = _strip_ansi(captured.out)
    lines = output.strip().split("\n")

    assert len(lines) == 83
    assert lines[0].strip().startswith("M")
    assert "HMM" in lines[-1]


def test_print_catto_has_color_codes(capsys: object) -> None:
    """Verify the cat is printed with ANSI color codes."""
    print_catto()
    captured = capsys.readouterr()  # type: ignore[attr-defined]
    output = captured.out

    # Check output contains ANSI escape codes
    assert "\033[" in output
    assert RESET in output


def test_get_random_pattern_returns_valid_pattern() -> None:
    """Verify get_random_pattern returns a name and callable."""
    name, func = get_random_pattern()

    assert isinstance(name, str)
    assert len(name) > 0
    assert callable(func)


def test_get_random_pattern_produces_different_results() -> None:
    """Verify randomness by checking multiple calls can produce different patterns."""
    patterns_seen: set[str] = set()

    # Call multiple times to see variety
    for _ in range(50):
        name, _ = get_random_pattern()
        patterns_seen.add(name)

    # Should see at least a few different patterns
    assert len(patterns_seen) >= 3


def test_solid_pattern_applies_single_color() -> None:
    """Verify solid pattern applies one color to entire content."""
    pattern = _solid_pattern("orange")
    result = pattern("MMM\nHHH")

    assert CAT_COLORS["orange"] in result
    assert RESET in result
    # Content should be preserved
    assert "MMM" in _strip_ansi(result)
    assert "HHH" in _strip_ansi(result)


def test_tabby_pattern_applies_stripes() -> None:
    """Verify tabby pattern applies alternating colors."""
    pattern = _tabby_pattern("brown", "chocolate")
    content = "line0\nline1\nline2\nline3\nline4\nline5"
    result = pattern(content)

    assert CAT_COLORS["brown"] in result
    assert CAT_COLORS["chocolate"] in result
    assert _strip_ansi(result) == content


def test_calico_pattern_uses_three_colors() -> None:
    """Verify calico pattern uses white, orange, and black."""
    pattern = _calico_pattern()
    # Need at least 15 lines to cycle through all three patch colors
    content = "MMMMMMMMMMMMMMMMMMMMMMMMMMMMM\n" * 20
    result = pattern(content)

    assert CAT_COLORS["white"] in result
    assert CAT_COLORS["orange"] in result
    assert CAT_COLORS["black"] in result


def test_tortoiseshell_pattern_uses_orange_and_black() -> None:
    """Verify tortoiseshell pattern uses orange, black, and ginger."""
    pattern = _tortoiseshell_pattern()
    content = "MMMMMMMMMMMMMMMMMMMMMMMMMMMMM\n" * 10
    result = pattern(content)

    assert CAT_COLORS["orange"] in result
    assert CAT_COLORS["black"] in result
    assert CAT_COLORS["ginger"] in result


def test_tuxedo_pattern_uses_black_and_white() -> None:
    """Verify tuxedo pattern uses black and white."""
    pattern = _tuxedo_pattern()
    content = "MMMMMMMMMMMMMMMMMMMMMMMMMMMMM\n" * 20
    result = pattern(content)

    assert CAT_COLORS["black"] in result
    assert CAT_COLORS["white"] in result


def test_iggy_pattern_uses_specified_colors() -> None:
    """Verify iggy pattern applies the two specified colors."""
    # Test with black and white (original Iggy colors)
    pattern = _iggy_pattern("black", "white")
    content = "MMMMMMMMMMMMMMMMMMMMMMMMMMMMM\n" * 20
    result = pattern(content)

    assert CAT_COLORS["black"] in result
    assert CAT_COLORS["white"] in result

    # Test with different color combination
    pattern2 = _iggy_pattern("orange", "white")
    result2 = pattern2(content)

    assert CAT_COLORS["orange"] in result2
    assert CAT_COLORS["white"] in result2
    # Should not contain black since we specified orange
    assert CAT_COLORS["black"] not in result2


def test_colorpoint_pattern_has_body_and_points() -> None:
    """Verify colorpoint pattern has different colors for body and extremities."""
    pattern = _colorpoint_pattern("cream", "chocolate")
    content = "\n".join(["MMMMMMMM"] * 20)
    result = pattern(content)

    assert CAT_COLORS["cream"] in result
    assert CAT_COLORS["chocolate"] in result


def test_cat_colors_are_valid_ansi_codes() -> None:
    """Verify all cat colors are valid ANSI 256-color codes."""
    for name, code in CAT_COLORS.items():
        assert code.startswith("\033[38;5;"), f"{name} has invalid format"
        assert code.endswith("m"), f"{name} missing 'm' terminator"
        # Extract the color number
        match = re.search(r"\033\[38;5;(\d+)m", code)
        assert match is not None, f"{name} has invalid ANSI code"
        color_num = int(match.group(1))
        assert 0 <= color_num <= 255, f"{name} color {color_num} out of range"


def test_cassandra_pattern_uses_silver_tabby_colors() -> None:
    """Verify Cassandra's pattern uses silver, gray, dark gray, fawn, and white."""
    pattern = _cassandra_pattern()
    # Need enough lines to cover all regions including tail
    content = "MMMMMMMMMMMMMMMMMMMMMMMMMMMMM\n" * 40
    result = pattern(content)

    assert CAT_COLORS["silver"] in result
    assert CAT_COLORS["gray"] in result
    assert CAT_COLORS["dark_gray"] in result
    assert CAT_COLORS["white"] in result  # White tail tip
    assert CAT_COLORS["fawn"] in result  # Tan/brown accent patches


def test_persephone_pattern_uses_silver_white_bicolor() -> None:
    """Verify Persephone's pattern uses white, silver, gray, and dark gray."""
    pattern = _persephone_pattern()
    # Need enough lines to cover all regions including paws
    content = "MMMMMMMMMMMMMMMMMMMMMMMMMMMMM\n" * 40
    result = pattern(content)

    assert CAT_COLORS["white"] in result  # White chest/belly/paws
    assert CAT_COLORS["silver"] in result  # Silver transitions
    assert CAT_COLORS["gray"] in result  # Gray back/sides
    assert CAT_COLORS["dark_gray"] in result  # Dark gray on head
    assert CAT_COLORS["light_gray"] in result  # Light gray transitions


def test_for_cassandra_prints_message(capsys: object) -> None:
    """Verify for_cassandra prints the custom message."""
    for_cassandra()
    captured = capsys.readouterr()  # type: ignore[attr-defined]
    assert "The babiest brioche loaf you ever saw." in captured.out


def test_for_persephone_prints_message(capsys: object) -> None:
    """Verify for_persephone prints the custom message."""
    for_persephone()
    captured = capsys.readouterr()  # type: ignore[attr-defined]
    assert "Miss independent snugglemonster, Percypie herself." in captured.out


def test_for_jennycatto_outputs_hearto_content(capsys: object) -> None:
    """Verify for_jennycatto outputs the hearto file content."""
    for_jennycatto()
    captured = capsys.readouterr()  # type: ignore[attr-defined]

    hearto_path = Path(__file__).parent / "hearto"
    expected_content = hearto_path.read_text(encoding="utf-8")

    # Strip ANSI codes and compare content
    stripped_output = _strip_ansi(captured.out)
    assert stripped_output.strip() == expected_content.strip()


def test_jennycatto_pattern_uses_forest_green_and_pink_red() -> None:
    """Verify jennycatto pattern uses forest_green for cat and pink_red for heart."""
    hearto_path = Path(__file__).parent / "hearto"
    content = hearto_path.read_text(encoding="utf-8")

    pattern = _jennycatto_pattern()
    result = pattern(content)

    # Both colors should be present
    assert CAT_COLORS["forest_green"] in result  # Cat color
    assert CAT_COLORS["pink_red"] in result  # Heart color


def test_jennycatto_pattern_colors_cat_green() -> None:
    """Verify the cat portion (left side) is colored forest green."""
    hearto_path = Path(__file__).parent / "hearto"
    content = hearto_path.read_text(encoding="utf-8")

    pattern = _jennycatto_pattern()
    result = pattern(content)
    lines = result.split("\n")

    # Check a line that only has cat content (no heart) - line 0
    # Should have forest_green but no pink_red
    assert CAT_COLORS["forest_green"] in lines[0]
    assert CAT_COLORS["pink_red"] not in lines[0]


def test_jennycatto_pattern_colors_heart_pink() -> None:
    """Verify the heart portion (right side, lines 4-8) is colored pink/red."""
    hearto_path = Path(__file__).parent / "hearto"
    content = hearto_path.read_text(encoding="utf-8")

    pattern = _jennycatto_pattern()
    result = pattern(content)
    lines = result.split("\n")

    # Check lines that have heart content (lines 4-8, 0-indexed)
    # These lines should have pink_red color
    for i in range(4, 9):
        assert CAT_COLORS["pink_red"] in lines[i], f"Line {i} should have pink_red heart color"


def test_all_pattern_names_are_descriptive() -> None:
    """Verify pattern names describe realistic cat patterns."""
    valid_prefixes = [
        "solid_", "bicolor_", "tabby_", "calico", "tortoiseshell",
        "tuxedo", "colorpoint_", "smoke_"
    ]

    for _ in range(100):
        name, _ = get_random_pattern()
        has_valid_prefix = any(name.startswith(prefix) for prefix in valid_prefixes)
        assert has_valid_prefix, f"Pattern '{name}' doesn't match known cat patterns"
