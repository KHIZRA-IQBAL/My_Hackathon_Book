#!/bin/bash
# Update agent context file with project information

set -e

# Source common utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

# Find repository root
REPO_ROOT=$(find_repo_root)
if [[ $? -ne 0 ]]; then
    exit 1
fi

cd "$REPO_ROOT"

# Get current branch and feature
CURRENT_BRANCH=$(get_current_branch)
CURRENT_USER=$(get_current_user)
DATE_ISO=$(format_date)

# Determine current feature
CURRENT_FEATURE="none"
if [[ "$CURRENT_BRANCH" =~ ^[0-9]+-(.+)$ ]]; then
    CURRENT_FEATURE="$CURRENT_BRANCH"
fi

# Create agent context file
AGENT_CONTEXT_FILE="$REPO_ROOT/.specify/memory/agent-context.md"

cat > "$AGENT_CONTEXT_FILE" << EOF
# Agent Context

**Last Updated**: $DATE_ISO
**Branch**: $CURRENT_BRANCH
**Feature**: $CURRENT_FEATURE
**User**: $CURRENT_USER

## Current State

- Working on: $CURRENT_FEATURE
- Branch: $CURRENT_BRANCH

## Active Features

EOF

# List all features from specs directory
if [[ -d "$REPO_ROOT/specs" ]]; then
    for dir in "$REPO_ROOT/specs"/*; do
        if [[ -d "$dir" ]]; then
            feature=$(basename "$dir")
            echo "- $feature" >> "$AGENT_CONTEXT_FILE"
        fi
    done
fi

cat >> "$AGENT_CONTEXT_FILE" << EOF

## Recent ADRs

EOF

# List recent ADRs
if [[ -d "$REPO_ROOT/history/adr" ]]; then
    ls -t "$REPO_ROOT/history/adr"/*.md 2>/dev/null | head -5 | while read -r adr; do
        adr_name=$(basename "$adr" .md)
        echo "- $adr_name" >> "$AGENT_CONTEXT_FILE"
    done
fi

echo "Agent context updated: $AGENT_CONTEXT_FILE"

exit 0
