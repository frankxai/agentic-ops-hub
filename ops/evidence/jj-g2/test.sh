#!/usr/bin/env bash
# G2 test: a valid receipt verifies; any tampering or wrong key fails.
# Exits non-zero if any direction misbehaves. Key material lives only in a temp dir.
set -uo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
RECEIPT="$HERE/receipt.sh"
export JJ="${JJ:-jj}"
export JJ_USER="Fake Agent" JJ_EMAIL="agent@example.invalid"

T=$(mktemp -d)
trap 'rm -rf "$T"' EXIT
fail=0
check() { # check <name> <expected: pass|fail> <command...>
  local name=$1 want=$2; shift 2
  if "$@" >"$T/out" 2>&1; then got=pass; else got=fail; fi
  if [ "$got" = "$want" ]; then echo "ok   - $name (verification: $got, expected)"
  else echo "FAIL - $name (wanted $want, got $got)"; sed 's/^/       /' "$T/out"; fail=1; fi
}
flip() { printf 'X' | dd of="$1" bs=1 seek="$2" conv=notrunc 2>/dev/null; }

echo "# $("$JJ" --version)"
ssh-keygen -q -t ed25519 -N "" -C "agent-session" -f "$T/key" || exit 1
ssh-keygen -q -t ed25519 -N "" -C "attacker" -f "$T/other" || exit 1
echo "agent-session $(cut -d' ' -f1,2 "$T/key.pub")" > "$T/allowed"

R="$T/repo"; mkdir "$R"
"$JJ" git init --colocate "$R" >/dev/null 2>&1 || { echo "FAIL - jj init"; exit 1; }
"$JJ" -R "$R" commit -m "base" >/dev/null 2>&1
BASE=$("$JJ" -R "$R" log --no-graph --color never -r @- -T 'commit_id')
echo one > "$R/a.txt";  "$JJ" -R "$R" commit -m "agent: add a.txt" >/dev/null 2>&1
printf 'two\nthree\n' > "$R/b.txt"; "$JJ" -R "$R" commit -m "agent: add b.txt" >/dev/null 2>&1
HEAD=$("$JJ" -R "$R" log --no-graph --color never -r @- -T 'commit_id')

bash "$RECEIPT" create "$R" "$BASE" "$HEAD" "$T/key" "$T/receipt.txt" || { echo "FAIL - create"; exit 1; }
if grep -q "a.txt" "$T/receipt.txt" && grep -q "b.txt" "$T/receipt.txt" && grep -q "jj op log" "$T/receipt.txt"; then
  echo "ok   - receipt contains op log and diff stat for both commits"
else
  echo "FAIL - receipt content incomplete"; fail=1
fi

check "valid receipt" pass bash "$RECEIPT" verify "$T/receipt.txt" "$T/allowed" agent-session

cp "$T/receipt.txt" "$T/tampered.txt"; cp "$T/receipt.txt.sig" "$T/tampered.txt.sig"
flip "$T/tampered.txt" 100
ndiff=$(cmp -l "$T/receipt.txt" "$T/tampered.txt" | wc -l | tr -d ' ')
if [ "$ndiff" = 1 ]; then echo "ok   - tampered copy differs from original by exactly 1 byte"; else echo "FAIL - tamper changed $ndiff bytes"; fail=1; fi
check "receipt with one byte changed" fail bash "$RECEIPT" verify "$T/tampered.txt" "$T/allowed" agent-session

cp "$T/receipt.txt" "$T/badsig.txt"; cp "$T/receipt.txt.sig" "$T/badsig.txt.sig"
flip "$T/badsig.txt.sig" 120
check "signature with one byte changed" fail bash "$RECEIPT" verify "$T/badsig.txt" "$T/allowed" agent-session

cp "$T/receipt.txt" "$T/forged.txt"; rm -f "$T/forged.txt.sig"
ssh-keygen -q -Y sign -f "$T/other" -n agent-receipt "$T/forged.txt"
check "valid signature from a non-allowed key" fail bash "$RECEIPT" verify "$T/forged.txt" "$T/allowed" agent-session

cp "$T/receipt.txt" "$T/ns.txt"; rm -f "$T/ns.txt.sig"
ssh-keygen -q -Y sign -f "$T/key" -n other-namespace "$T/ns.txt"
check "signature in the wrong namespace" fail bash "$RECEIPT" verify "$T/ns.txt" "$T/allowed" agent-session

check "original receipt still valid" pass bash "$RECEIPT" verify "$T/receipt.txt" "$T/allowed" agent-session

if [ $fail -eq 0 ]; then echo "G2 PASS"; else echo "G2 FAIL"; fi
exit $fail
