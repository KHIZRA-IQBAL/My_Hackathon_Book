#!/bin/bash
# Setup planning artifacts for a feature

set -e

# Source common utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

# Parse command line arguments
FEATURE=""
JSON_OUTPUT=false

show_help() {
    cat << EOF
Usage: setup-plan.sh [--feature <name>] [--json]

Setup planning artifacts (plan.md) for a feature.

Options:
  --feature <name>     Feature name (auto-detected from branch if not provided)
  --json               Output in JSON format
  --help               Show this help message

Examples:
  setup-plan.sh --feature user-auth
  setup-plan.sh  # Auto-detect from current branch
EOF
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --feature)
            FEATURE="$2"
            shift 2
            ;;
        --json)
            JSON_OUTPUT=true
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

# Find repository root
REPO_ROOT=$(find_repo_root)
if [[ $? -ne 0 ]]; then
    exit 1
fi

cd "$REPO_ROOT"

# Auto-detect feature from branch if not provided
if [[ -z "$FEATURE" ]]; then
    CURRENT_BRANCH=$(get_current_branch)
    if [[ "$CURRENT_BRANCH" =~ ^[0-9]+-(.+)$ ]] || [[ "$CURRENT_BRANCH" != "main" ]] && [[ "$CURRENT_BRANCH" != "master" ]]; then
        FEATURE="$CURRENT_BRANCH"
    else
        echo "Error: Could not auto-detect feature from branch. Please provide --feature" >&2
        exit 1
    fi
fi

# Determine feature directory
FEATURE_DIR="$REPO_ROOT/specs/$FEATURE"

if [[ ! -d "$FEATURE_DIR" ]]; then
    echo "Error: Feature directory not found: $FEATURE_DIR" >&2
    echo "Run create-new-feature.sh first to create the feature" >&2
    exit 1
fi

# Create plan.md from template
TEMPLATE="$REPO_ROOT/.specify/templates/plan-template.md"
PLAN_FILE="$FEATURE_DIR/plan.md"

if [[ -f "$PLAN_FILE" ]]; then
    echo "Warning: plan.md already exists at $PLAN_FILE" >&2
    echo "Skipping creation to avoid overwriting existing content" >&2
else
    if [[ -f "$TEMPLATE" ]]; then
        cp "$TEMPLATE" "$PLAN_FILE"
        echo "Created plan.md from template" >&2
    else
        echo "Warning: Template not found at $TEMPLATE" >&2
        touch "$PLAN_FILE"
        echo "Created empty plan.md" >&2
    fi
fi

# Output result
if $JSON_OUTPUT; then
    cat << EOF
{"feature": "$FEATURE", "plan_file": "$PLAN_FILE", "exists": $([ -f "$PLAN_FILE" ] && echo "true" || echo "false")}
EOF
else
    echo "Plan setup complete:"
    echo "  Feature: $FEATURE"
    echo "  Plan file: $PLAN_FILE"
fi

exit 0
