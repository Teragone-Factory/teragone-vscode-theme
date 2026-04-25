# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.1] — 2026-04-25

### Fixed

- Markdown preview: mermaid edge labels (e.g. `yes`/`no` on flowchart
  conditional arrows) rendered invisible. The `.mermaid .edgeLabel`
  rule matched both the outer SVG `<g>` and the inner HTML `<span>`,
  so `font-size: 0.82em` compounded along the chain and
  `padding: 0 0.2em` pushed glyphs out of the foreignObject's clipping
  box (mermaid pre-sizes that box against its own 16px text
  measurement, leaving no slack). Split the rule: chrome on the SVG
  group, text inside the foreignObject with `font-size: inherit` and
  `padding: 0`.

### Added

- `scripts/capture-screenshots.sh` — semi-automated, macOS-only
  capture for `docs/screenshots/`. Walks each target with an
  instruction prompt and `screencapture -w` (interactive window pick).
- `docs/fixtures/` — minimal source files (Python, TypeScript,
  Markdown, mermaid) used by the capture script.
- `justfile`: `screenshots` recipe wrapping the capture script.
- README: mermaid screenshot embedded in the "At a glance" section.
- `.vscodeignore`: `scripts/**` excluded from the VSIX.

## [0.2.0] — 2026-04-16

### Added

- **Teragone Factory Dark** — second variant registered alongside the
  light theme. Lifted terracotta (`#E07A4F`) on warm fired-clay dark
  (`#221C18`); same brand surface, evening shift. Brand hue preserved
  across both surfaces; lightness and chroma retuned per OKLCH so the
  terracotta reads cleanly without going garish. Activate via
  `Preferences → Color Theme → Teragone Factory Dark`.
- README "Dark palette" table (12 tokens, mirroring the light table) as
  the canonical source of truth for the dark surface.
- Palette parity test now iterates over both theme JSONs paired with
  their respective README palette blocks; markdown-preview CSS check
  remains light-only by design (preview surface is brand-locked cream).

## [0.1.0] — 2026-04-16

### Added

- Initial public release of the **Teragone Factory** light theme.
- Workbench colours (editor, sidebar, status bar, terminal, peek view, diff
  editor, merge, minimap, charts, debug, settings).
- TextMate syntax highlighting for general scopes plus Python, TypeScript,
  Shell, YAML, TOML, JSON, Markdown.
- Semantic token colours mirroring the TextMate roles so LSP-aware files
  render consistently with plain files.
- Markdown preview stylesheet re-skinning prose and mermaid diagrams.
- Brand icon, gallery banner, and publication metadata for the VSIX.
- CI, parity test, pre-commit hooks, and release workflow that attaches
  the `.vsix` to every tagged GitHub Release.

[Unreleased]: https://github.com/Teragone-Factory/teragone-vscode-theme/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/Teragone-Factory/teragone-vscode-theme/releases/tag/v0.2.0
[0.1.0]: https://github.com/Teragone-Factory/teragone-vscode-theme/releases/tag/v0.1.0
