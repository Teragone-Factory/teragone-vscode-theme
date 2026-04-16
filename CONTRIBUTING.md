# Contributing

Thanks for wanting to improve **Teragone Factory**. This is a brand-locked
theme, so before you open a PR, please read the palette discipline below.

## Local dev loop

```bash
git clone https://github.com/Teragone-Factory/teragone-vscode-theme.git
cd teragone-vscode-theme
just install-local    # symlinks into ~/.vscode/extensions/
uv sync               # installs pytest for the parity test
pre-commit install    # optional but recommended
```

Edit `themes/teragone-factory-color-theme.json` or
`styles/teragone-markdown-preview.css`, then run `Developer: Reload Window`
in VSCode. No rebuild is needed while the symlink is in place.

Alternatively, `just preview` opens a fresh VSCode window with the
extension loaded via `--extensionDevelopmentPath`, which leaves your main
VSCode configuration untouched.

## Palette discipline

The 12-token table in [`README.md`](./README.md) is the canonical source
of truth for the brand palette. Hard rules:

- **Never pure white, never pure black, never cold grey.** Surfaces stay
  warm.
- Brand primary is `#C85A2C`; brand-dark `#9E4421` is reserved for
  keywords and hover states.
- Derived neutral shades (line-number grey, sidebar section headers,
  etc.) are tuned in context and intentionally not listed in the README
  table. Do not promote them into the canonical palette.
- When a change affects how a canonical token is used, update the
  `colors` block in the theme JSON **and** the matching `--teragone-*`
  custom property in the CSS. The parity test enforces that every
  canonical hex is referenced in both files.

## Before opening a PR

Run, in order:

```bash
just lint      # markdownlint + pre-commit
just parity    # uv run pytest — palette parity across README/JSON/CSS
just package   # sanity-check that the VSIX still builds
```

If the change is visually observable, attach before/after screenshots to
the PR. The PR template has a checklist mirroring this list.

## Commit messages

[Conventional Commits](https://www.conventionalcommits.org/) as a
discipline (`feat:`, `fix:`, `chore:`, `docs:`). No tooling enforces them;
readable CHANGELOG entries matter more than strict machine-parseability.
Do not co-author commits as Claude or any AI assistant.

## Releasing (maintainers only)

```bash
just release VERSION    # bumps package.json, prepends CHANGELOG, tags v$VERSION
git push && git push --tags
```

The `release.yml` workflow packages the `.vsix`, creates the GitHub
Release, extracts the matching CHANGELOG section as the release body, and
attaches the artifact. VS Marketplace and Open VSX publishing are
currently deferred — see `BACKLOG.md`.
