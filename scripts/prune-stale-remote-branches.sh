#!/usr/bin/env bash
# Remove remote-tracking branches (remotes/<remote>/<branch>) that no longer
# exist on the remote — the stale entries you see from `git branch -a`.
#
# Usage:
#   ./scripts/prune-stale-remote-branches.sh           # prune all remotes
#   ./scripts/prune-stale-remote-branches.sh --dry-run # show what would be removed

set -euo pipefail

dry_run=false

usage() {
  cat <<'EOF'
Usage: prune-stale-remote-branches.sh [OPTIONS]

Deletes stale remote-tracking refs (e.g. remotes/origin/old-feature) whose
branches were deleted on the remote but still appear in `git branch -a`.

Options:
  -n, --dry-run   Show branches that would be pruned, without changing anything
  -h, --help      Show this help

Does not delete local branches — only remote-tracking references.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    -n | --dry-run) dry_run=true; shift ;;
    -h | --help) usage; exit 0 ;;
    *)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Error: not inside a git repository." >&2
  exit 1
fi

remotes="$(git remote)"
if [[ -z "$remotes" ]]; then
  echo "No remotes configured."
  exit 0
fi

if $dry_run; then
  echo "Dry run — stale remote-tracking branches that would be removed:"
  echo
  found=false
  while IFS= read -r remote; do
    [[ -z "$remote" ]] && continue
    while IFS= read -r line; do
      [[ -z "$line" ]] && continue
      found=true
      printf '  %s\n' "$line"
    done < <(git remote prune "$remote" --dry-run 2>&1 | sed -n 's/^ \* \[would prune\] //p')
  done <<<"$remotes"
  if ! $found; then
    echo "  (none — already up to date)"
  fi
  exit 0
fi

echo "Fetching and pruning stale remote-tracking branches..."
git fetch --all --prune

echo "Done. Run \`git branch -a\` to verify."
