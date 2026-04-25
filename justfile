set shell := ["bash", "-euo", "pipefail", "-c"]
set dotenv-load := false

publisher := "teragone-factory"
name := "teragone-factory-theme"
extension_dir := env_var_or_default("VSCODE_EXTENSIONS_DIR", env_var("HOME") + "/.vscode/extensions")

# Show available recipes.
default:
    @just --list

# Symlink the working copy into ~/.vscode/extensions/ for live iteration.
install-local:
    #!/usr/bin/env bash
    version="$(jq -r '.version' package.json)"
    target="{{ extension_dir }}/{{ publisher }}.{{ name }}-${version}"
    if [ -e "${target}" ] || [ -L "${target}" ]; then
        echo "already installed at ${target} — run 'just uninstall-local' first"
        exit 1
    fi
    ln -s "$(pwd)" "${target}"
    echo "linked ${target} → $(pwd)"
    echo "reload VSCode (Developer: Reload Window) and pick 'Teragone Factory' in Color Theme."

# Remove the local symlink.
uninstall-local:
    #!/usr/bin/env bash
    version="$(jq -r '.version' package.json)"
    target="{{ extension_dir }}/{{ publisher }}.{{ name }}-${version}"
    if [ -L "${target}" ]; then
        rm "${target}"
        echo "unlinked ${target}"
    else
        echo "no symlink at ${target}"
    fi

# Open a fresh VSCode window with the extension loaded (leaves user config untouched).
preview:
    code --extensionDevelopmentPath="$(pwd)" .

# Build the VSIX into the repo root.
package:
    npx --yes @vscode/vsce package --no-dependencies

# Run markdownlint on all Markdown files.
lint:
    npx --yes markdownlint-cli2 "**/*.md" "#node_modules/**" "#.venv/**"

# Run the palette parity test.
parity:
    uv run pytest tests/test_palette_parity.py -q

# Regenerate docs/screenshots/*.png (macOS). Pass target names to limit scope.
screenshots *TARGETS:
    scripts/capture-screenshots.sh {{ TARGETS }}

# Assert package.json version, latest CHANGELOG entry, and current git tag (if any) agree.
check-version:
    #!/usr/bin/env bash
    pkg_version="$(jq -r '.version' package.json)"
    changelog_version="$(awk '/^## \[[0-9]/ {gsub(/\[|\]/, "", $2); print $2; exit}' CHANGELOG.md)"
    if [ "${pkg_version}" != "${changelog_version}" ]; then
        echo "mismatch: package.json=${pkg_version} CHANGELOG.md=${changelog_version}"
        exit 1
    fi
    if [ -n "${GITHUB_REF:-}" ] && [[ "${GITHUB_REF}" == refs/tags/v* ]]; then
        tag_version="${GITHUB_REF#refs/tags/v}"
        if [ "${tag_version}" != "${pkg_version}" ]; then
            echo "mismatch: git tag v${tag_version} package.json ${pkg_version}"
            exit 1
        fi
    fi
    echo "version ${pkg_version} consistent across package.json, CHANGELOG.md${GITHUB_REF:+, git tag}"

# Run every local check a contributor should run before opening a PR.
check: lint parity check-version package

# Bump version, prepend CHANGELOG stub, commit, and tag v$VERSION. Push to trigger release.
release VERSION:
    #!/usr/bin/env bash
    version="{{ VERSION }}"
    if ! [[ "${version}" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        echo "VERSION must be semver (e.g. 0.2.0), got: ${version}"
        exit 1
    fi
    if ! git diff-index --quiet HEAD --; then
        echo "working tree is dirty — commit or stash first"
        exit 1
    fi
    echo "about to:"
    echo "  - bump package.json version to ${version}"
    echo "  - mark CHANGELOG.md [Unreleased] as [${version}] with today's date"
    echo "  - commit and tag v${version}"
    read -r -p "proceed? [y/N] " ok
    [[ "${ok}" =~ ^[Yy]$ ]] || { echo "aborted"; exit 1; }
    tmp="$(mktemp)"
    jq --arg v "${version}" '.version = $v' package.json > "${tmp}" && mv "${tmp}" package.json
    today="$(date +%Y-%m-%d)"
    sed -i.bak "s/^## \[Unreleased\]$/## [Unreleased]\n\n## [${version}] — ${today}/" CHANGELOG.md
    rm CHANGELOG.md.bak
    git add package.json CHANGELOG.md
    git commit -m "chore(release): v${version}"
    git tag "v${version}"
    echo "tagged v${version}. push with: git push && git push --tags"
