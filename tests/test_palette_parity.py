"""Palette parity across README, theme JSON, and markdown-preview CSS.

The 12-token table in README.md between the `<!-- palette:start -->` and
`<!-- palette:end -->` markers is the canonical source of truth. This test
asserts:

- Every canonical hex appears at least once in the theme JSON `colors`
  block. If a canonical token is never referenced, the README table has
  grown an orphan entry.
- Every canonical hex appears at least once in the markdown-preview CSS.
  Same rationale.
- Every "core" CSS custom property (e.g. `--tg-brand-primary`) whose name
  matches a README token maps to the expected hex. Catches direct drift
  where the CSS would redefine a canonical role's hex.

Derived neutral shades (e.g. `--tg-border-strong`, `--tg-surface-sunken`)
carry non-canonical hexes by design and are intentionally out of scope
for the strict check. Full role drift across unrelated roles is a known
gap; escalate to a palette-source-of-truth repo if it ever bites.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"
THEME_JSON = REPO_ROOT / "themes" / "teragone-factory-color-theme.json"
MARKDOWN_CSS = REPO_ROOT / "styles" / "teragone-markdown-preview.css"

HEX_RE = re.compile(r"#[0-9A-Fa-f]{6}")
PALETTE_BLOCK_RE = re.compile(
    r"<!--\s*palette:start\s*-->(.*?)<!--\s*palette:end\s*-->",
    re.DOTALL,
)
TG_VAR_RE = re.compile(
    r"--tg-([a-z0-9-]+)\s*:\s*(#[0-9A-Fa-f]{6})",
)

# CSS custom property name -> README token name it must match.
# Only the subset of --tg-* vars whose hex should equal the canonical role.
# Derived neutrals (e.g. --tg-border-strong, --tg-surface-sunken) are
# intentionally omitted.
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


def _canonical_table() -> dict[str, str]:
    """Return {token-name: HEX} parsed from the README palette block."""
    text = README.read_text(encoding="utf-8")
    match = PALETTE_BLOCK_RE.search(text)
    assert match, (
        "README.md is missing the <!-- palette:start --> / <!-- palette:end -->"
        " markers that delimit the canonical palette table."
    )
    block = match.group(1)
    table: dict[str, str] = {}
    row_re = re.compile(r"\|\s*([a-z-]+)\s*\|\s*`(#[0-9A-Fa-f]{6})`")
    for name, hex_code in row_re.findall(block):
        table[name] = hex_code.upper()
    return table


def _json_colors_hexes() -> set[str]:
    data = json.loads(THEME_JSON.read_text(encoding="utf-8"))
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
def canonical() -> dict[str, str]:
    table = _canonical_table()
    assert len(table) >= 10, (
        f"README palette block parsed only {len(table)} entries — expected the"
        " full 12-token table. Check the Markdown table formatting."
    )
    return table


def test_canonical_hexes_all_used_in_theme_json(canonical: dict[str, str]) -> None:
    json_hexes = _json_colors_hexes()
    missing = set(canonical.values()) - json_hexes
    assert not missing, (
        f"Canonical README hexes are not used anywhere in themes/"
        f"teragone-factory-color-theme.json `colors` block: {sorted(missing)}."
        " Either reference them in the theme JSON or remove them from the"
        " README palette table."
    )


def test_canonical_hexes_all_used_in_markdown_css(canonical: dict[str, str]) -> None:
    css_text = MARKDOWN_CSS.read_text(encoding="utf-8")
    css_hexes = _normalise(set(HEX_RE.findall(css_text)))
    missing = set(canonical.values()) - css_hexes
    assert not missing, (
        "Canonical README hexes are not used anywhere in"
        f" styles/teragone-markdown-preview.css: {sorted(missing)}. Either"
        " reference them in the CSS or remove them from the README palette"
        " table."
    )


def test_core_css_vars_match_readme_roles(canonical: dict[str, str]) -> None:
    css_vars = _css_tg_vars()
    mismatches: list[str] = []
    for css_name, readme_token in CORE_CSS_VAR_TO_README_TOKEN.items():
        if css_name not in css_vars:
            mismatches.append(
                f"  --tg-{css_name}: missing from CSS"
                f" (expected {canonical[readme_token]} for README token"
                f" '{readme_token}')"
            )
            continue
        expected = canonical[readme_token]
        actual = css_vars[css_name]
        if expected != actual:
            mismatches.append(
                f"  --tg-{css_name}: CSS has {actual}, README token"
                f" '{readme_token}' has {expected}"
            )
    assert not mismatches, (
        "Core CSS --tg-* custom properties drifted from the README palette"
        " table:\n" + "\n".join(mismatches)
    )
