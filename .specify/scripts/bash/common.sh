#!/bin/bash
# Common utilities for Spec-Kit Plus bash scripts

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
    echo "Error: Could not find repository root" >&2
    return 1
}

# Get current git branch name
get_current_branch() {
    if command -v git &> /dev/null; then
        git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "main"
    else
        echo "main"
    fi
}

# Get current user
get_current_user() {
    if command -v git &> /dev/null; then
        git config user.name 2>/dev/null || echo "$(whoami)"
    else
        echo "$(whoami)"
    fi
}

# Get next ID in a directory
get_next_id() {
    local dir="$1"
    local max_id=0

    if [[ -d "$dir" ]]; then
        for file in "$dir"/*.md "$dir"/*.prompt.md; do
            [[ -f "$file" ]] || continue
            local filename=$(basename "$file")
            if [[ "$filename" =~ ^([0-9]+)- ]]; then
                local id="${BASH_REMATCH[1]}"
                id=$((10#$id))  # Convert to base 10
                if ((id > max_id)); then
                    max_id=$id
                fi
            fi
        done
    fi

    echo $((max_id + 1))
}

# Create slug from title
create_slug() {
    local title="$1"
    echo "$title" | tr '[:upper:]' '[:lower:]' | sed -e 's/[^a-z0-9]/-/g' -e 's/-\+/-/g' -e 's/^-//' -e 's/-$//'
}

# Format date as ISO 8601
format_date() {
    date +%Y-%m-%d
}

# Export functions for use in other scripts
export -f find_repo_root
export -f get_current_branch
export -f get_current_user
export -f get_next_id
export -f create_slug
export -f format_date
