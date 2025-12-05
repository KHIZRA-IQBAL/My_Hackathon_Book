#!/bin/bash
# Create an Architecture Decision Record (ADR)

set -e

# Source common utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

# Parse command line arguments
TITLE=""
JSON_OUTPUT=false

show_help() {
    cat << EOF
Usage: create-adr.sh --title "Decision Title" [--json]

Create an Architecture Decision Record (ADR) in the history/adr/ directory.

Options:
  --title "Title"     Title for the ADR (required)
  --json              Output in JSON format
  --help              Show this help message

Examples:
  create-adr.sh --title "Use PostgreSQL for primary database"
  create-adr.sh --title "Adopt microservices architecture" --json
EOF
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --title)
            TITLE="$2"
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

# Validate required arguments
if [[ -z "$TITLE" ]]; then
    echo "Error: --title is required" >&2
    show_help
    exit 1
fi

# Find repository root
REPO_ROOT=$(find_repo_root)
if [[ $? -ne 0 ]]; then
    exit 1
fi

cd "$REPO_ROOT"

# Create ADR directory
ADR_DIR="$REPO_ROOT/history/adr"
mkdir -p "$ADR_DIR"

# Get next ID
ID=$(get_next_id "$ADR_DIR")
ID_PADDED=$(printf "%04d" "$ID")

# Create slug from title
SLUG=$(create_slug "$TITLE")

# Create filename
FILENAME="${ID_PADDED}-${SLUG}.md"
FILE_PATH="$ADR_DIR/$FILENAME"

# Read template
TEMPLATE_PATH="$REPO_ROOT/.specify/templates/adr-template.md"
if [[ ! -f "$TEMPLATE_PATH" ]]; then
    echo "Error: Template not found at $TEMPLATE_PATH" >&2
    exit 1
fi

# Get metadata
DATE_ISO=$(format_date)

# Create ADR file
cp "$TEMPLATE_PATH" "$FILE_PATH"

# Replace basic placeholders
sed -i "s/{{ADR_NUMBER}}/$ID_PADDED/g" "$FILE_PATH"
sed -i "s/{{TITLE}}/$TITLE/g" "$FILE_PATH"
sed -i "s/{{DATE}}/$DATE_ISO/g" "$FILE_PATH"
sed -i "s/{{STATUS}}/Proposed/g" "$FILE_PATH"

# Output result
if $JSON_OUTPUT; then
    cat << EOF
{"id": "$ID_PADDED", "path": "$FILE_PATH", "title": "$TITLE"}
EOF
else
    echo "ADR created successfully:"
    echo "  ID: $ID_PADDED"
    echo "  Path: $FILE_PATH"
    echo "  Title: $TITLE"
fi

exit 0
