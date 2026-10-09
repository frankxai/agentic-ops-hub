#!/usr/bin/env bash
# Prints one full create / verify / tamper / verify walkthrough with raw output.
# Usage: JJ=/path/to/jj bash demo.sh [dir-to-copy-sample-receipt-into]
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
export JJ="${JJ:-jj}" JJ_USER="Fake Agent" JJ_EMAIL="agent@example.invalid"
W=$(mktemp -d); trap 'rm -rf "$W"' EXIT
set -x
ssh-keygen -q -t ed25519 -N "" -C agent-session -f "$W/key"
echo "agent-session $(cut -d' ' -f1,2 "$W/key.pub")" > "$W/allowed"
mkdir "$W/repo"
"$JJ" git init --colocate "$W/repo"
"$JJ" -R "$W/repo" commit -m base
echo one > "$W/repo/a.txt"
"$JJ" -R "$W/repo" commit -m "agent: add a.txt"
printf 'two\nthree\n' > "$W/repo/b.txt"
"$JJ" -R "$W/repo" commit -m "agent: add b.txt"
bash "$HERE/receipt.sh" create "$W/repo" 'description(exact:"base\n")' '@-' "$W/key" "$W/receipt.txt"
set +x
echo "==== receipt.txt"; cat "$W/receipt.txt"
echo "==== receipt.txt.sig (first 3 lines)"; head -3 "$W/receipt.txt.sig"
set -x
bash "$HERE/receipt.sh" verify "$W/receipt.txt" "$W/allowed" agent-session; echo "exit=$?"
cp "$W/receipt.txt" "$W/t.txt"; cp "$W/receipt.txt.sig" "$W/t.txt.sig"
printf X | dd of="$W/t.txt" bs=1 seek=100 conv=notrunc 2>/dev/null
cmp -l "$W/receipt.txt" "$W/t.txt"
bash "$HERE/receipt.sh" verify "$W/t.txt" "$W/allowed" agent-session; echo "exit=$?"
set +x
if [ -n "${1:-}" ]; then cp "$W/receipt.txt" "$1/sample-receipt.txt"; cp "$W/receipt.txt.sig" "$1/sample-receipt.txt.sig"; fi
