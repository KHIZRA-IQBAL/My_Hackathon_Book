#!/bin/bash
# Check prerequisites for Spec-Kit Plus

set -e

JSON_OUTPUT=false
PATHS_ONLY=false

show_help() {
    cat << EOF
Usage: check-prerequisites.sh [--json] [--paths-only]

Check if required tools and directories are available.

Options:
  --json          Output in JSON format
  --paths-only    Only check paths, not tool versions
  --help          Show this help message
EOF
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --json)
            JSON_OUTPUT=true
            shift
            ;;
        --paths-only)
            PATHS_ONLY=true
            shift
            ;;
        --help)
            show_help
            exit 0
            ;;
        *)
            echo "Unknown option: $1" >&2
            show_help
            exit 1
            ;;
    esac
done

# Check if command exists
command_exists() {
    command -v "$1" &> /dev/null
}

# Find repository root
find_repo_root() {
    local current_dir="$PWD"
    while [[ "$current_dir" != "/" ]]; do
        if [[ -d "$current_dir/.git" ]] || [[ -d "$current_dir/.specify" ]]; then
            echo "$current_dir"
            return 0
        fi
        current_dir=$(dirname "$current_dir")
    done
    return 1
}

REPO_ROOT=$(find_repo_root)
if [[ $? -ne 0 ]]; then
    echo "Error: Could not find repository root" >&2
    exit 1
fi

cd "$REPO_ROOT"

# Initialize results
HAS_GIT=false
HAS_CLAUDE=false
HAS_SPECIFY_DIR=false
HAS_CLAUDE_DIR=false
HAS_HISTORY_DIR=false
HAS_TEMPLATES=false

# Check git
if command_exists git; then
    HAS_GIT=true
fi

# Check claude (Claude Code CLI)
if command_exists claude; then
    HAS_CLAUDE=true
fi

# Check directories
[[ -d "$REPO_ROOT/.specify" ]] && HAS_SPECIFY_DIR=true
[[ -d "$REPO_ROOT/.claude" ]] && HAS_CLAUDE_DIR=true
[[ -d "$REPO_ROOT/history" ]] && HAS_HISTORY_DIR=true
[[ -d "$REPO_ROOT/.specify/templates" ]] && HAS_TEMPLATES=true

# Calculate overall status
ALL_GOOD=true
[[ "$HAS_SPECIFY_DIR" == "false" ]] && ALL_GOOD=false
[[ "$HAS_CLAUDE_DIR" == "false" ]] && ALL_GOOD=false

# Output results
if $JSON_OUTPUT; then
    cat << EOF
{
  "git": $HAS_GIT,
  "claude": $HAS_CLAUDE,
  "specify_dir": $HAS_SPECIFY_DIR,
  "claude_dir": $HAS_CLAUDE_DIR,
  "history_dir": $HAS_HISTORY_DIR,
  "templates": $HAS_TEMPLATES,
  "all_good": $ALL_GOOD
}
EOF
else
    echo "Prerequisites Check:"
    echo "  Git: $([ "$HAS_GIT" == "true" ] && echo "✓" || echo "✗")"
    echo "  Claude CLI: $([ "$HAS_CLAUDE" == "true" ] && echo "✓" || echo "✗ (optional)")"
    echo "  .specify/: $([ "$HAS_SPECIFY_DIR" == "true" ] && echo "✓" || echo "✗")"
    echo "  .claude/: $([ "$HAS_CLAUDE_DIR" == "true" ] && echo "✓" || echo "✗")"
    echo "  history/: $([ "$HAS_HISTORY_DIR" == "true" ] && echo "✓" || echo "✗")"
    echo "  Templates: $([ "$HAS_TEMPLATES" == "true" ] && echo "✓" || echo "✗")"
    echo ""
    if [[ "$ALL_GOOD" == "true" ]]; then
        echo "Status: ✓ All required prerequisites met"
    else
        echo "Status: ✗ Some prerequisites missing"
        exit 1
    fi
fi

exit 0
