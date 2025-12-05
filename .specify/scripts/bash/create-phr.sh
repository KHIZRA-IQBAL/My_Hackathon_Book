#!/bin/bash
# Create a Prompt History Record (PHR)

set -e

# Source common utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

# Parse command line arguments
TITLE=""
STAGE=""
FEATURE=""
JSON_OUTPUT=false

show_help() {
    cat << EOF
Usage: create-phr.sh --title "Title" --stage <stage> [--feature <name>] [--json]

Create a Prompt History Record (PHR) in the history/prompts/ directory.

Options:
  --title "Title"     Title for the PHR (required)
  --stage <stage>     Stage: constitution|spec|plan|tasks|red|green|refactor|explainer|misc|general (required)
  --feature <name>    Feature name (required for feature stages, auto-detected from branch)
  --json              Output in JSON format
  --help              Show this help message

Examples:
  create-phr.sh --title "Implement user authentication" --stage spec --feature user-auth
  create-phr.sh --title "Setup project constitution" --stage constitution
  create-phr.sh --title "General question about testing" --stage general

Routing (all under history/prompts/):
  - constitution → history/prompts/constitution/
  - spec|plan|tasks|red|green|refactor|explainer|misc → history/prompts/<feature-name>/
  - general → history/prompts/general/
EOF
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --title)
            TITLE="$2"
            shift 2
            ;;
        --stage)
            STAGE="$2"
            shift 2
            ;;
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

# Validate required arguments
if [[ -z "$TITLE" ]]; then
    echo "Error: --title is required" >&2
    show_help
    exit 1
fi

if [[ -z "$STAGE" ]]; then
    echo "Error: --stage is required" >&2
    show_help
    exit 1
fi

# Validate stage
VALID_STAGES="constitution spec plan tasks red green refactor explainer misc general"
if [[ ! " $VALID_STAGES " =~ " $STAGE " ]]; then
    echo "Error: Invalid stage '$STAGE'. Must be one of: $VALID_STAGES" >&2
    exit 1
fi

# Find repository root
REPO_ROOT=$(find_repo_root)
if [[ $? -ne 0 ]]; then
    exit 1
fi

cd "$REPO_ROOT"

# Determine feature and route
PROMPTS_BASE="$REPO_ROOT/history/prompts"
ROUTE_DIR=""

if [[ "$STAGE" == "constitution" ]]; then
    ROUTE_DIR="$PROMPTS_BASE/constitution"
elif [[ "$STAGE" == "general" ]]; then
    ROUTE_DIR="$PROMPTS_BASE/general"
else
    # Feature stages - need feature name
    if [[ -z "$FEATURE" ]]; then
        # Try to auto-detect from branch
        CURRENT_BRANCH=$(get_current_branch)
        # Check if branch name contains feature pattern (NNN-feature-name)
        if [[ "$CURRENT_BRANCH" =~ ^[0-9]+-(.+)$ ]]; then
            FEATURE="$CURRENT_BRANCH"
        else
            echo "Error: --feature is required for stage '$STAGE' and could not be auto-detected from branch" >&2
            exit 1
        fi
    fi
    ROUTE_DIR="$PROMPTS_BASE/$FEATURE"
fi

# Create route directory if it doesn't exist
mkdir -p "$ROUTE_DIR"

# Get next ID
ID=$(get_next_id "$ROUTE_DIR")
ID_PADDED=$(printf "%03d" "$ID")

# Create slug from title
SLUG=$(create_slug "$TITLE")

# Determine file extension based on stage
if [[ "$STAGE" == "constitution" ]]; then
    EXTENSION="constitution.prompt.md"
elif [[ "$STAGE" == "general" ]]; then
    EXTENSION="general.prompt.md"
else
    EXTENSION="${STAGE}.prompt.md"
fi

# Create filename
FILENAME="${ID_PADDED}-${SLUG}.${EXTENSION}"
FILE_PATH="$ROUTE_DIR/$FILENAME"

# Read template
TEMPLATE_PATH="$REPO_ROOT/.specify/templates/phr-template.prompt.md"
if [[ ! -f "$TEMPLATE_PATH" ]]; then
    echo "Error: Template not found at $TEMPLATE_PATH" >&2
    exit 1
fi

# Get metadata
DATE_ISO=$(format_date)
BRANCH=$(get_current_branch)
USER=$(get_current_user)
MODEL="claude-sonnet-4-5-20250929"
SURFACE="agent"
FEATURE_VALUE="${FEATURE:-none}"

# Create PHR file with placeholders
cp "$TEMPLATE_PATH" "$FILE_PATH"

# Replace placeholders
sed -i "s/{{ID}}/$ID_PADDED/g" "$FILE_PATH"
sed -i "s/{{TITLE}}/$TITLE/g" "$FILE_PATH"
sed -i "s/{{STAGE}}/$STAGE/g" "$FILE_PATH"
sed -i "s/{{DATE_ISO}}/$DATE_ISO/g" "$FILE_PATH"
sed -i "s/{{SURFACE}}/$SURFACE/g" "$FILE_PATH"
sed -i "s/{{MODEL}}/$MODEL/g" "$FILE_PATH"
sed -i "s/{{FEATURE}}/$FEATURE_VALUE/g" "$FILE_PATH"
sed -i "s/{{BRANCH}}/$BRANCH/g" "$FILE_PATH"
sed -i "s/{{USER}}/$USER/g" "$FILE_PATH"
sed -i "s/{{COMMAND}}/create-phr/g" "$FILE_PATH"
sed -i "s/{{LABELS}}/\"phr\", \"$STAGE\"/g" "$FILE_PATH"
sed -i "s/{{LINKS_SPEC}}/null/g" "$FILE_PATH"
sed -i "s/{{LINKS_TICKET}}/null/g" "$FILE_PATH"
sed -i "s/{{LINKS_ADR}}/null/g" "$FILE_PATH"
sed -i "s/{{LINKS_PR}}/null/g" "$FILE_PATH"
sed -i "s/{{FILES_YAML}}/  - none/g" "$FILE_PATH"
sed -i "s/{{TESTS_YAML}}/  - none/g" "$FILE_PATH"
sed -i "s/{{PROMPT_TEXT}}/[User prompt will be added here]/g" "$FILE_PATH"
sed -i "s/{{RESPONSE_TEXT}}/[Agent response will be added here]/g" "$FILE_PATH"
sed -i "s/{{OUTCOME_IMPACT}}/Pending/g" "$FILE_PATH"
sed -i "s/{{TESTS_SUMMARY}}/Pending/g" "$FILE_PATH"
sed -i "s/{{FILES_SUMMARY}}/Pending/g" "$FILE_PATH"
sed -i "s/{{NEXT_PROMPTS}}/Pending/g" "$FILE_PATH"
sed -i "s/{{REFLECTION_NOTE}}/Pending/g" "$FILE_PATH"
sed -i "s/{{FAILURE_MODES}}/None observed/g" "$FILE_PATH"
sed -i "s/{{GRADER_RESULTS}}/Not run/g" "$FILE_PATH"
sed -i "s/{{PROMPT_VARIANT_ID}}/default/g" "$FILE_PATH"
sed -i "s/{{NEXT_EXPERIMENT}}/N\/A/g" "$FILE_PATH"

# Output result
if $JSON_OUTPUT; then
    cat << EOF
{"id": "$ID_PADDED", "path": "$FILE_PATH", "stage": "$STAGE", "title": "$TITLE", "route": "$ROUTE_DIR"}
EOF
else
    echo "PHR created successfully:"
    echo "  ID: $ID_PADDED"
    echo "  Path: $FILE_PATH"
    echo "  Stage: $STAGE"
    echo "  Title: $TITLE"
    echo "  Route: $ROUTE_DIR"
fi

exit 0
