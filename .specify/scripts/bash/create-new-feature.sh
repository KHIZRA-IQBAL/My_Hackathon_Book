#!/bin/bash
# Create a new feature with spec directory and git branch

set -e

# Source common utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

# Parse command line arguments
DESCRIPTION=""
SHORT_NAME=""
NUMBER=0
JSON_OUTPUT=false

show_help() {
    cat << EOF
Usage: create-new-feature.sh [--short-name <name>] [--number N] [--json] <feature description>

Create a new feature with spec directory, git branch, and prompts directory.

Options:
  --short-name <name>  Provide a custom short name (2-4 words) for the branch
  --number N           Specify branch number manually (overrides auto-detection)
  --json               Output in JSON format
  --help               Show this help message

Examples:
  create-new-feature.sh "Add user authentication system" --short-name "user-auth"
  create-new-feature.sh "Implement OAuth2 integration for API"
EOF
}

# Parse arguments
ARGS=()
while [[ $# -gt 0 ]]; do
    case $1 in
        --short-name)
            SHORT_NAME="$2"
            shift 2
            ;;
        --number)
            NUMBER="$2"
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
            ARGS+=("$1")
            shift
            ;;
    esac
done

# Get description from remaining arguments
DESCRIPTION="${ARGS[*]}"

if [[ -z "$DESCRIPTION" ]]; then
    echo "Error: Feature description is required" >&2
    show_help
    exit 1
fi

# Find repository root
REPO_ROOT=$(find_repo_root)
if [[ $? -ne 0 ]]; then
    exit 1
fi

cd "$REPO_ROOT"

# Create specs directory
SPECS_DIR="$REPO_ROOT/specs"
mkdir -p "$SPECS_DIR"

# Generate branch suffix
if [[ -n "$SHORT_NAME" ]]; then
    BRANCH_SUFFIX=$(echo "$SHORT_NAME" | tr '[:upper:]' '[:lower:]' | sed -e 's/[^a-z0-9]/-/g' -e 's/-\+/-/g' -e 's/^-//' -e 's/-$//')
else
    # Generate from description
    BRANCH_SUFFIX=$(echo "$DESCRIPTION" | tr '[:upper:]' '[:lower:]' | sed -e 's/[^a-z0-9]/ /g' | awk '{for(i=1;i<=3 && i<=NF;i++) printf "%s-", $i}' | sed 's/-$//')
fi

# Determine branch number
if [[ $NUMBER -eq 0 ]]; then
    # Auto-detect next number
    MAX_NUM=0

    # Check existing branches
    if command -v git &> /dev/null; then
        for branch in $(git branch -a | sed 's/^\*//' | sed 's/^[[:space:]]*//' | grep -E "^[0-9]+-"); do
            if [[ "$branch" =~ ^([0-9]+)- ]]; then
                NUM="${BASH_REMATCH[1]}"
                NUM=$((10#$NUM))
                if ((NUM > MAX_NUM)); then
                    MAX_NUM=$NUM
                fi
            fi
        done
    fi

    # Check specs directory
    for dir in "$SPECS_DIR"/*; do
        if [[ -d "$dir" ]]; then
            dirname=$(basename "$dir")
            if [[ "$dirname" =~ ^([0-9]+)- ]]; then
                NUM="${BASH_REMATCH[1]}"
                NUM=$((10#$NUM))
                if ((NUM > MAX_NUM)); then
                    MAX_NUM=$NUM
                fi
            fi
        fi
    done

    NUMBER=$((MAX_NUM + 1))
fi

FEATURE_NUM=$(printf "%03d" "$NUMBER")
BRANCH_NAME="${FEATURE_NUM}-${BRANCH_SUFFIX}"

# Create git branch if git is available
HAS_GIT=false
if command -v git &> /dev/null && git rev-parse --git-dir &> /dev/null; then
    git checkout -b "$BRANCH_NAME" 2>/dev/null || echo "Warning: Could not create git branch (may already exist)" >&2
    HAS_GIT=true
fi

# Create feature directory in specs
FEATURE_DIR="$SPECS_DIR/$BRANCH_NAME"
mkdir -p "$FEATURE_DIR"

# Copy spec template
TEMPLATE="$REPO_ROOT/.specify/templates/spec-template.md"
SPEC_FILE="$FEATURE_DIR/spec.md"
if [[ -f "$TEMPLATE" ]]; then
    cp "$TEMPLATE" "$SPEC_FILE"
else
    touch "$SPEC_FILE"
fi

# Create prompts directory
PROMPTS_DIR="$REPO_ROOT/history/prompts/$BRANCH_NAME"
mkdir -p "$PROMPTS_DIR"

# Set environment variable
export SPECIFY_FEATURE="$BRANCH_NAME"

# Output result
if $JSON_OUTPUT; then
    cat << EOF
{"BRANCH_NAME": "$BRANCH_NAME", "SPEC_FILE": "$SPEC_FILE", "FEATURE_NUM": "$FEATURE_NUM", "HAS_GIT": $HAS_GIT}
EOF
else
    echo "Feature created successfully:"
    echo "  BRANCH_NAME: $BRANCH_NAME"
    echo "  SPEC_FILE: $SPEC_FILE"
    echo "  FEATURE_NUM: $FEATURE_NUM"
    echo "  HAS_GIT: $HAS_GIT"
    echo "  SPECIFY_FEATURE environment variable set to: $BRANCH_NAME"
fi

exit 0
