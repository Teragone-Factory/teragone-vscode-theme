# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
