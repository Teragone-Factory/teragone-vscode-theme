"""Palette parity across README, theme JSONs, and markdown-preview CSS.

Two 12-token tables in README.md are canonical sources of truth — one per
surface (light, dark) — delimited by HTML comment markers:

    <!-- palette:start --> ... <!-- palette:end -->          (light)
    <!-- palette-dark:start --> ... <!-- palette-dark:end -->(dark)

Each palette table maps to one theme JSON in `themes/`. For each pair:

- Every canonical hex must appear at least once in that theme JSON's
  `colors` block. If a canonical token is never referenced, the README
  table has grown an orphan entry.

For the markdown-preview CSS (light-only, contributed once regardless of
which theme variant is active):

- Every canonical *light* palette hex must appear at least once.
- Every "core" CSS custom property whose name matches a light token must
  resolve to that light hex.

The dark palette is intentionally not enforced against the CSS — the
markdown preview is a brand-locked light surface (see header comment in
`styles/teragone-markdown-preview.css`).

Derived neutral shades (`--tg-border-strong`, `--tg-surface-sunken`,
their dark counterparts) carry non-canonical hexes by design and are
intentionally out of scope for the strict check.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"
THEMES_DIR = REPO_ROOT / "themes"
MARKDOWN_CSS = REPO_ROOT / "styles" / "teragone-markdown-preview.css"

HEX_RE = re.compile(r"#[0-9A-Fa-f]{6}")
TG_VAR_RE = re.compile(
    r"--tg-([a-z0-9-]+)\s*:\s*(#[0-9A-Fa-f]{6})",
)

# (README marker name, theme JSON filename relative to themes/).
# Each entry is one (palette table, theme JSON) parity pair.
PALETTE_PAIRS = [
    ("palette",      "teragone-factory-color-theme.json"),
    ("palette-dark", "teragone-factory-dark-color-theme.json"),
]

# CSS custom property name -> README *light* token name it must match.
# The markdown preview is light-only, so this map is intentionally not
# parameterised over surfaces.
CORE_CSS_VAR_TO_README_TOKEN = {
    "brand-primary": "brand-primary",
    "brand-primary-dark": "brand-dark",
    "brand-primary-soft": "brand-soft",
    "ink": "ink",
    "text-primary": "text-primary",
    "text-muted": "text-muted",
    "border": "border",
    "surface": "surface",
    "surface-muted": "surface-muted",
    "success": "success",
    "warning": "warning",
    "danger": "danger",
}


def _normalise(hexes):
    return {h.upper() for h in hexes}


def _palette_block(marker: str) -> str:
    """Return the raw markdown between <!-- {marker}:start --> and :end -->."""
    text = README.read_text(encoding="utf-8")
    pattern = re.compile(
        rf"<!--\s*{re.escape(marker)}:start\s*-->(.*?)<!--\s*{re.escape(marker)}:end\s*-->",
        re.DOTALL,
    )
    match = pattern.search(text)
    assert match, (
        f"README.md is missing the <!-- {marker}:start --> / "
        f"<!-- {marker}:end --> markers that delimit a canonical palette table."
    )
    return match.group(1)


def _canonical_table(marker: str) -> dict[str, str]:
    """Return {token-name: HEX} parsed from the README palette block."""
    block = _palette_block(marker)
    table: dict[str, str] = {}
    row_re = re.compile(r"\|\s*([a-z-]+)\s*\|\s*`(#[0-9A-Fa-f]{6})`")
    for name, hex_code in row_re.findall(block):
        table[name] = hex_code.upper()
    return table


def _json_colors_hexes(theme_path: Path) -> set[str]:
    data = json.loads(theme_path.read_text(encoding="utf-8"))
    colors = data.get("colors", {})
    found: set[str] = set()
    for value in colors.values():
        if isinstance(value, str):
            # Workbench colors may carry an 8-hex alpha suffix; normalise to 6.
            for match in re.finditer(r"#[0-9A-Fa-f]{6}", value):
                found.add(match.group(0))
    return _normalise(found)


def _css_tg_vars() -> dict[str, str]:
    text = MARKDOWN_CSS.read_text(encoding="utf-8")
    return {name: hex_code.upper() for name, hex_code in TG_VAR_RE.findall(text)}


@pytest.fixture(scope="module")
def light_palette() -> dict[str, str]:
    table = _canonical_table("palette")
    assert len(table) >= 10, (
        f"README light palette block parsed only {len(table)} entries — expected"
        " the full 12-token table. Check the Markdown table formatting."
    )
    return table


@pytest.mark.parametrize(("marker", "theme_file"), PALETTE_PAIRS, ids=[p[0] for p in PALETTE_PAIRS])
def test_canonical_hexes_all_used_in_theme_json(marker: str, theme_file: str) -> None:
    theme_path = THEMES_DIR / theme_file
    assert theme_path.exists(), (
        f"Expected theme JSON {theme_path} for palette block '{marker}' but"
        " the file is missing. Either add the theme or remove the README block."
    )
    canonical = _canonical_table(marker)
    assert len(canonical) >= 10, (
        f"README palette block '{marker}' parsed only {len(canonical)} entries"
        " — expected the full 12-token table. Check the Markdown table formatting."
    )
    json_hexes = _json_colors_hexes(theme_path)
    missing = set(canonical.values()) - json_hexes
    assert not missing, (
        f"Canonical README hexes from '{marker}' are not used anywhere in"
        f" {theme_path.relative_to(REPO_ROOT)} `colors` block: {sorted(missing)}."
        " Either reference them in the theme JSON or remove them from the"
        " README palette table."
    )


def test_light_canonical_hexes_all_used_in_markdown_css(
    light_palette: dict[str, str],
) -> None:
    css_text = MARKDOWN_CSS.read_text(encoding="utf-8")
    css_hexes = _normalise(set(HEX_RE.findall(css_text)))
    missing = set(light_palette.values()) - css_hexes
    assert not missing, (
        "Canonical light palette hexes are not used anywhere in"
        f" styles/teragone-markdown-preview.css: {sorted(missing)}. Either"
        " reference them in the CSS or remove them from the light palette"
        " table. (The dark palette is intentionally not enforced against the"
        " CSS — markdown preview is a light-only brand surface.)"
    )


def test_core_css_vars_match_readme_light_roles(
    light_palette: dict[str, str],
) -> None:
    css_vars = _css_tg_vars()
    mismatches: list[str] = []
    for css_name, readme_token in CORE_CSS_VAR_TO_README_TOKEN.items():
        if css_name not in css_vars:
            mismatches.append(
                f"  --tg-{css_name}: missing from CSS"
                f" (expected {light_palette[readme_token]} for README token"
                f" '{readme_token}')"
            )
            continue
        expected = light_palette[readme_token]
        actual = css_vars[css_name]
        if expected != actual:
            mismatches.append(
                f"  --tg-{css_name}: CSS has {actual}, README light token"
                f" '{readme_token}' has {expected}"
            )
    assert not mismatches, (
        "Core CSS --tg-* custom properties drifted from the README light"
        " palette table:\n" + "\n".join(mismatches)
    )
