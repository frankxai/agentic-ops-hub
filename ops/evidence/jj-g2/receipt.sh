#!/usr/bin/env bash
# create / verify signed agent-session receipts built from jj op log + diff stat.
#   receipt.sh create <repo> <base-rev> <head-rev> <private-key> <out-receipt>
#   receipt.sh verify <receipt> <allowed-signers> <principal>
# Signature is an SSH signature (ssh-keygen -Y sign), namespace "agent-receipt",
# written next to the receipt as <receipt>.sig.
set -euo pipefail

NAMESPACE="agent-receipt"
JJ="${JJ:-jj}"

create() {
  local repo=$1 base=$2 head=$3 key=$4 out=$5
  {
    echo "agent-receipt/v1"
    echo "jj: $("$JJ" --version)"
    echo "base: $("$JJ" -R "$repo" log --no-graph --color never -r "$base" -T 'commit_id')"
    echo "head: $("$JJ" -R "$repo" log --no-graph --color never -r "$head" -T 'commit_id')"
    echo "--- jj op log"
    "$JJ" -R "$repo" op log --no-graph --color never
    echo "--- jj diff --stat $base..$head"
    (cd "$repo" && "$JJ" diff --color never --stat --from "$base" --to "$head")
  } > "$out"
  rm -f "$out.sig"
  ssh-keygen -q -Y sign -f "$key" -n "$NAMESPACE" "$out"
  echo "receipt: $out"
  echo "signature: $out.sig"
}

verify() {
  local receipt=$1 allowed=$2 principal=$3
  ssh-keygen -Y verify -f "$allowed" -I "$principal" -n "$NAMESPACE" \
    -s "$receipt.sig" < "$receipt"
}

case "${1:-}" in
  create) shift; [ $# -eq 5 ] || { echo "usage: create <repo> <base> <head> <key> <out>" >&2; exit 2; }; create "$@" ;;
  verify) shift; [ $# -eq 3 ] || { echo "usage: verify <receipt> <allowed-signers> <principal>" >&2; exit 2; }; verify "$@" ;;
  *) echo "usage: receipt.sh create|verify ..." >&2; exit 2 ;;
esac
