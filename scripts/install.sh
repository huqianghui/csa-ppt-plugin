#!/usr/bin/env bash
set -euo pipefail

# CSA-PPT Plugin Multi-Platform Installer
# Verifies symlinks, checks dependencies, and shows platform-specific usage.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_ROOT="$(dirname "$SCRIPT_DIR")"

echo "=== CSA-PPT Plugin Installer ==="
echo "Plugin root: $PLUGIN_ROOT"
echo ""

# --- Symlink setup ---
create_symlink() {
    local target="$1" link_dir="$2" link_name="$3"
    local link_path="$link_dir/$link_name"
    mkdir -p "$link_dir"
    if [ -L "$link_path" ]; then
        echo "  [skip] $link_path (exists)"
    elif [ -d "$link_path" ]; then
        echo "  [skip] $link_path (directory exists)"
    else
        if [[ "${OSTYPE:-}" == msys* || "${OSTYPE:-}" == cygwin* ]]; then
            cmd //c "mklink /J \"$(cygpath -w "$link_path")\" \"$(cygpath -w "$target")\""
        else
            ln -s "$target" "$link_path"
        fi
        echo "  [created] $link_path -> $target"
    fi
}

echo "Setting up cross-platform skill discovery..."
create_symlink "../skills" "$PLUGIN_ROOT/.codex"    "skills"
create_symlink "../skills" "$PLUGIN_ROOT/.agents"   "skills"
create_symlink "../skills" "$PLUGIN_ROOT/.windsurf"  "skills"
create_symlink "../skills" "$PLUGIN_ROOT/.opencode"  "agents"

# --- Verify symlinks ---
echo ""
echo "Verifying skill discovery paths..."
FAIL=0
for dir in ".codex/skills" ".agents/skills" ".windsurf/skills" ".opencode/agents"; do
    full="$PLUGIN_ROOT/$dir"
    if [ -d "$full" ] && [ -f "$full/csa-ppt/SKILL.md" ]; then
        echo "  [ok] $dir"
    else
        echo "  [FAIL] $dir"
        FAIL=1
    fi
done

# Also verify platform manifests
for f in ".claude-plugin/plugin.json" ".cursor-plugin/plugin.json" ".github/plugin/plugin.json" "opencode.json"; do
    if [ -f "$PLUGIN_ROOT/$f" ]; then
        echo "  [ok] $f"
    else
        echo "  [FAIL] $f missing"
        FAIL=1
    fi
done

# --- Check prerequisites ---
echo ""
echo "Checking prerequisites..."
check_cmd() {
    if command -v "$1" >/dev/null 2>&1; then
        echo "  [ok] $1"
    else
        echo "  [warn] $1 not found ($2)"
    fi
}
check_py() {
    if python3 -c "import $1" 2>/dev/null; then
        echo "  [ok] python3 $1"
    else
        echo "  [warn] $1 not found (pip install $1)"
    fi
}

check_cmd python3    "needed for azure-diagrams, skywork-ppt, pptx"
check_cmd node       "needed for pptx html2pptx converter"
check_cmd dot        "graphviz — needed for azure-diagrams"
check_py  diagrams
check_py  pptx

# --- Usage guide ---
echo ""
if [ "$FAIL" -eq 0 ]; then
    echo "=== All checks passed ==="
else
    echo "=== Some checks failed — see above ==="
fi

echo ""
echo "Platform usage:"
echo ""
echo "  Claude Code:   Installed via plugin marketplace"
echo "  Cursor:        Clone repo, .cursor-plugin/plugin.json auto-discovered"
echo "  Copilot CLI:   Clone repo, .github/plugin/plugin.json auto-discovered"
echo "  Codex CLI:     ln -s $PLUGIN_ROOT/skills ~/.codex/skills"
echo "  Windsurf:      ln -s $PLUGIN_ROOT/skills ~/.codeium/windsurf/skills"
echo "  OpenCode:      Clone repo, opencode.json auto-discovered"
