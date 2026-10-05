#!/usr/bin/env bash
# estate-guard-rollout.sh — install (or upgrade) the estate-guard pack across
# every repo checked out under a directory, one branch + draft PR per repo.
#
#   scripts/estate-guard-rollout.sh ~/repos                 # install everywhere, open PRs
#   scripts/estate-guard-rollout.sh ~/repos --dry-run       # show what would change
#   scripts/estate-guard-rollout.sh ~/repos --only "frankx.ai-vercel-website gencreator.ai"
#   scripts/estate-guard-rollout.sh ~/repos --no-hooks      # CI + scanner only (awesome-* style repos)
#
# Needs: git, node >= 18, python3, gh (authenticated). The pack comes from a
# shallow clone of claude-skills-library main unless ESTATE_GUARD_PACK points at
# a local checkout. Never pushes to main; always a branch and a draft PR.
set -euo pipefail
ROOT="${1:?usage: estate-guard-rollout.sh <dir-of-repos> [--dry-run] [--no-hooks] [--only \"a b c\"]}"; shift
DRY=0; EXTRA=(); ONLY=""
while [ $# -gt 0 ]; do
  case "$1" in
    --dry-run) DRY=1 ;;
    --no-hooks|--no-ci) EXTRA+=("$1") ;;
    --only) ONLY="$2"; shift ;;
    *) echo "unknown flag: $1" >&2; exit 2 ;;
  esac; shift
done
PACK="${ESTATE_GUARD_PACK:-}"
if [ -z "$PACK" ]; then
  TMP="$(mktemp -d)"; git clone -q --depth 1 https://github.com/frankxai/claude-skills-library "$TMP/csl"
  PACK="$TMP/csl/packs/estate-guard"
fi
BRANCH="agent/claude/estate-guard"
for repo in "$ROOT"/*/; do
  repo="${repo%/}"; name="$(basename "$repo")"
  [ -d "$repo/.git" ] || continue
  if [ -n "$ONLY" ] && ! grep -qw "$name" <<<"$ONLY"; then continue; fi
  echo "== $name"
  if [ -n "$(git -C "$repo" status --porcelain)" ]; then echo "   skip: dirty working tree (another agent may be mid-edit)"; continue; fi
  if [ $DRY -eq 1 ]; then "$PACK/install.sh" "$repo" --dry-run "${EXTRA[@]}" | sed 's/^/   /'; continue; fi
  default="$(git -C "$repo" symbolic-ref --short refs/remotes/origin/HEAD 2>/dev/null | sed 's|origin/||' || echo main)"
  git -C "$repo" fetch -q origin "$default"
  git -C "$repo" checkout -q -B "$BRANCH" "origin/$default"
  "$PACK/install.sh" "$repo" "${EXTRA[@]}" | sed 's/^/   /'
  node "$repo/.claude/ci/estate-guard-scan.mjs" --root "$repo" --fail-on never --out "$repo/.claude/ci/estate-guard/last-scan.md" >/dev/null || true
  git -C "$repo" add .claude/ci/estate-guard-scan.mjs .claude/ci/estate-guard/config.json .claude/skills/estate-guard .claude/hooks/estate-guard-*.py .claude/settings.json .github/workflows/estate-guard.yml .gitignore 2>/dev/null || true
  if git -C "$repo" diff --cached --quiet; then echo "   nothing to commit (already current)"; continue; fi
  git -C "$repo" commit -q -m "chore(security): install estate-guard pack (scanner, CI ratchet, hard-stop gate, taint hook)"
  git -C "$repo" push -q -u origin "$BRANCH"
  gh pr create -R "$(git -C "$repo" remote get-url origin | sed -E 's#.*github.com[:/]##; s#\.git$##')" --draft --head "$BRANCH" --base "$default" \
    --title "chore(security): install estate-guard pack" \
    --body "Installs the estate-guard pack from frankxai/claude-skills-library: agentic-surface scanner, weekly + per-PR CI ratchet (high fails), PreToolUse hard-stop gate, PostToolUse taint marker, SessionStart contract. First scan report is in the job summary of the estate-guard check." \
    2>&1 | sed 's/^/   /' || echo "   PR not created (gh error above); branch is pushed"
done
