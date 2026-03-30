#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  scripts/sync_skill_to_workspace.sh <skill-name>

Example:
  scripts/sync_skill_to_workspace.sh 01-run-python

Behavior:
  - Copy skills/<skill-name>/SKILL.md to the OpenClaw workspace
  - Overwrite skills/<skill-name>/scripts/ in the OpenClaw workspace

Environment variables:
  OPENCLAW_WORKSPACE_DIR  Override workspace path (default: ~/.openclaw/workspace)
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

if [[ $# -ne 1 ]]; then
  usage
  exit 1
fi

skill_name="$1"
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "$script_dir/.." && pwd)"

workspace_dir="${OPENCLAW_WORKSPACE_DIR:-$HOME/.openclaw/workspace}"
source_skill_dir="$repo_root/skills/$skill_name"
target_skill_dir="$workspace_dir/skills/$skill_name"

source_skill_md="$source_skill_dir/SKILL.md"
source_scripts_dir="$source_skill_dir/scripts"
target_skill_md="$target_skill_dir/SKILL.md"
target_scripts_dir="$target_skill_dir/scripts"

if [[ ! -d "$source_skill_dir" ]]; then
  echo "Source skill directory not found: $source_skill_dir" >&2
  exit 1
fi

if [[ ! -f "$source_skill_md" ]]; then
  echo "Source SKILL.md not found: $source_skill_md" >&2
  exit 1
fi

if [[ ! -d "$source_scripts_dir" ]]; then
  echo "Source scripts directory not found: $source_scripts_dir" >&2
  exit 1
fi

mkdir -p "$target_skill_dir"

cp "$source_skill_md" "$target_skill_md"
rsync -a --delete "$source_scripts_dir/" "$target_scripts_dir/"

echo "Synced skill: $skill_name"
echo "  source: $source_skill_dir"
echo "  target: $target_skill_dir"
echo "  files: SKILL.md, scripts/"