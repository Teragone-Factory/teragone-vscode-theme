#!/usr/bin/env bash
# Semi-automated screenshot regeneration for docs/screenshots/.
#
# macOS-only (uses `screencapture -w` for interactive window picking).
# Opens VSCode with the extension loaded against docs/fixtures/, then
# walks you through each shot: you set up the editor state (theme,
# active file, preview pane), the script waits, you click the VSCode
# window, it saves the PNG to the right path.
#
# Usage:
#   scripts/capture-screenshots.sh            # all targets
#   scripts/capture-screenshots.sh mermaid    # one or more named targets

set -euo pipefail

if [[ "$(uname -s)" != "Darwin" ]]; then
    echo "error: this script uses macOS screencapture; port it before running on $(uname -s)" >&2
    exit 1
fi

repo_root="$(cd "$(dirname "$0")/.." && pwd)"
cd "${repo_root}"

out_dir="docs/screenshots"
fixtures="docs/fixtures"

declare -a targets=(
    "editor"
    "editor-dark"
    "workbench"
    "workbench-dark"
    "markdown-preview"
    "mermaid"
)

declare -A instructions=(
    ["editor"]="Pick 'Teragone Factory' (light). Open ${fixtures}/sample.py. Close the sidebar (⌘B) for a clean editor-only frame."
    ["editor-dark"]="Pick 'Teragone Factory Dark'. Open ${fixtures}/sample.py. Close the sidebar (⌘B)."
    ["workbench"]="Pick 'Teragone Factory' (light). Open the sidebar and a terminal panel so chrome is visible around ${fixtures}/sample.ts."
    ["workbench-dark"]="Pick 'Teragone Factory Dark'. Same layout as 'workbench' — sidebar + terminal visible."
    ["markdown-preview"]="Pick 'Teragone Factory' (light). Open ${fixtures}/sample.md and show the Markdown preview side-by-side (⌘K V). Close the sidebar."
    ["mermaid"]="Pick 'Teragone Factory' (light). Open ${fixtures}/sample-mermaid.md and show the Markdown preview only (⌘⇧V). Ensure markdown-mermaid.lightModeTheme is 'base'."
)

requested=("$@")
if [[ ${#requested[@]} -eq 0 ]]; then
    requested=("${targets[@]}")
fi

# Validate target names before launching VSCode.
for name in "${requested[@]}"; do
    if [[ -z "${instructions[${name}]:-}" ]]; then
        echo "error: unknown target '${name}'" >&2
        echo "known targets: ${targets[*]}" >&2
        exit 1
    fi
done

mkdir -p "${out_dir}"

echo "→ launching VSCode with extension loaded from $(pwd)"
code --extensionDevelopmentPath="$(pwd)" "${fixtures}" >/dev/null 2>&1 &
echo "  give VSCode a moment to open, then follow the prompts below."
echo

for name in "${requested[@]}"; do
    out="${out_dir}/${name}.png"
    echo "── ${name} → ${out}"
    echo "   ${instructions[${name}]}"
    read -r -p "   ready? [enter to capture, s to skip] " reply
    if [[ "${reply}" == "s" || "${reply}" == "S" ]]; then
        echo "   skipped."
        echo
        continue
    fi
    echo "   click the VSCode window to capture..."
    screencapture -w "${out}"
    if [[ -f "${out}" ]]; then
        echo "   saved ${out} ($(du -h "${out}" | cut -f1))"
    else
        echo "   warning: ${out} was not written — capture cancelled?"
    fi
    echo
done

echo "done. review with: open ${out_dir}"
