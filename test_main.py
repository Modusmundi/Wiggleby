from pathlib import Path

from main import print_catto


def test_print_catto_outputs_content(capsys: object) -> None:
    """Verify print_catto outputs the catto file content."""
    print_catto()
    captured = capsys.readouterr()  # type: ignore[attr-defined]

    catto_path = Path(__file__).parent / "catto"
    expected = catto_path.read_text(encoding="utf-8")

    assert captured.out == expected + "\n"


def test_print_catto_contains_cat_features(capsys: object) -> None:
    """Verify the ASCII art contains recognizable cat features."""
    print_catto()
    captured = capsys.readouterr()  # type: ignore[attr-defined]
    output = captured.out

    # Check for M characters that form the cat shape
    assert "MMM" in output
    assert "HHH" in output

    # Check special characters are preserved
    assert "'" in output  # Single quotes in whiskers/details
    assert "&&&" in output  # Ampersands in the body
    assert ":::" in output  # Colons for shading


def test_print_catto_preserves_structure(capsys: object) -> None:
    """Verify the ASCII art structure is preserved with correct line count."""
    print_catto()
    captured = capsys.readouterr()  # type: ignore[attr-defined]
    lines = captured.out.strip().split("\n")

    # The catto file has 83 lines of content
    assert len(lines) == 83

    # First line starts with spaces then M
    assert lines[0].strip().startswith("M")

    # Last line contains the cat's feet
    assert "HMM" in lines[-1]
