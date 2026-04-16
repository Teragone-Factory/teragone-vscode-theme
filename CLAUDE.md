# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A single-theme VSCode extension: **Teragone Factory**, a warm light theme
(terracotta on cream) for long-form documentation work. No build step, no
tests, no source code — the extension is a manifest, one theme JSON, and
a markdown-preview stylesheet (themes both the prose and mermaid output).

## Commands

Package and install locally (there is no test or lint command):

```bash
# Symlink for live iteration (edit JSON → reload window in VSCode)
ln -s "$(pwd)" ~/.vscode/extensions/teragone-factory.teragone-factory-theme-0.1.0

# Or produce a .vsix and install it
npx @vscode/vsce package
code --install-extension teragone-factory-theme-0.1.0.vsix
```

Activate via `Preferences → Color Theme → Teragone Factory`. After editing
the JSON, reload the VSCode window (`Developer: Reload Window`) to pick up
changes; no rebuild needed when symlinked.

## Architecture

Everything lives in `themes/teragone-factory-color-theme.json`, which has
three sections the manifest points VSCode at:

- `colors` — workbench UI chrome (editor, sidebar, status bar, terminal…).
- `tokenColors` — TextMate-scope syntax highlighting.
- `semanticTokenColors` — semantic highlighting (enabled via
  `"semanticHighlighting": true`); overrides `tokenColors` for LSP-aware
  languages. When tweaking syntax colours, update both layers or the
  result will differ between semantic-aware and plain files.

`package.json` registers the theme under `contributes.themes` with
`uiTheme: "vs"` (light base). Changing `label` or `path` there requires
re-running the symlink/package step.

`styles/teragone-markdown-preview.css` is contributed via
`contributes.markdown.previewStyles` and re-skins the built-in markdown
preview plus mermaid diagrams rendered by `bierner.markdown-mermaid`. It
redeclares `--vscode-*` variables so the preview stays on-brand even when
the editor is set to a dark theme. For cleanest mermaid output users
should set `"markdown-mermaid.lightModeTheme": "base"`. Keep its palette
in sync with the theme JSON — both derive from the same tokens.

## Palette discipline

The theme is brand-locked. Hard constraints (from `README.md`):

- **Never pure white, never pure black, never cold grey.** Surfaces stay
  warm (cream `#FDFBF7`, ink `#1A1614`).
- Brand primary is `#C85A2C` (terracotta, sampled from the Factory
  wordmark); brand-dark `#9E4421` is used for keywords/hover.
- Full palette with roles is documented in `README.md` — treat that table
  as the source of truth and keep it in sync when colours change.

The palette was originally sampled alongside a Teragone Factory Typst
slide template and an MkDocs brand layer used on long-form audit
deliverables. Those live outside this repo and are treated as
historical reference, not live sync targets — no action needed here
when they change, and vice versa.
