# jj G2: signed receipts

Verdict: PASS. A receipt built from `jj op log` plus a diff stat verifies when untouched and fails verification with one byte changed, in the receipt or in the signature.

Epic: #171. Scope: gate G2 only.

## Environment

- jj 0.45.1-7c41cdeb16b6b321c64e789a966b6adf723816a5, release `jj-v0.45.1-x86_64-pc-windows-msvc.zip` from github.com/jj-vcs/jj, downloaded with `gh release download v0.45.1 -R jj-vcs/jj`.
- The task said Linux binary. This run was on a Windows 11 host (Git Bash, OpenSSH_10.3p1), not a Linux cloud box, so the Windows binary was used. No egress block occurred.
- `agentic-jujutsu` and `agentdb` were not installed. No other repo was touched.

## What the receipt is

`receipt.sh create <repo> <base-rev> <head-rev> <key> <out>` writes a text file with the jj version, base and head commit ids, the full `jj op log --no-graph`, and `jj diff --stat --from base --to head`. It signs that file with `ssh-keygen -Y sign -n agent-receipt` using a throwaway ed25519 key, producing `<out>.sig`.

`receipt.sh verify <receipt> <allowed-signers> <principal>` runs `ssh-keygen -Y verify` with the same namespace.

The test (`test.sh`) generates all keys in a `mktemp -d` directory that is deleted on exit. No key material is in the repo.

## Test run

```
$ JJ=/path/to/jj.exe bash ops/evidence/jj-g2/test.sh; echo "exit=$?"
# jj 0.45.1-7c41cdeb16b6b321c64e789a966b6adf723816a5
ok   - receipt contains op log and diff stat for both commits
ok   - valid receipt (verification: pass, expected)
ok   - tampered copy differs from original by exactly 1 byte
ok   - receipt with one byte changed (verification: fail, expected)
ok   - signature with one byte changed (verification: fail, expected)
ok   - valid signature from a non-allowed key (verification: fail, expected)
ok   - signature in the wrong namespace (verification: fail, expected)
ok   - original receipt still valid (verification: pass, expected)
G2 PASS
exit=0
```

## Gate checked in both directions

The test script itself was checked for failing open. With `verify` replaced by `true` in a scratch copy of `receipt.sh`, the same test exits 1:

```
FAIL - receipt with one byte changed (wanted fail, got pass)
FAIL - signature with one byte changed (wanted fail, got pass)
FAIL - valid signature from a non-allowed key (wanted fail, got pass)
FAIL - signature in the wrong namespace (wanted fail, got pass)
G2 FAIL
sabotage exit=1
```

## Raw walkthrough (`demo.sh`)

Two commits as a fake agent session in a colocated repo (`jj git init --colocate`), then create, verify, flip byte 101 (`0` to `X`), verify again.

```
$ receipt.sh create <repo> 'description(exact:"base\n")' '@-' <key> receipt.txt
receipt: receipt.txt
signature: receipt.txt.sig

agent-receipt/v1
jj: jj 0.45.1-7c41cdeb16b6b321c64e789a966b6adf723816a5
base: 4bf0dc96ffe627d6530c87003d21bc52346f64a2
head: 6f6d577ee02f0ac8471411560554a4492f58ce08
--- jj op log
eff71451038a frank@Starlight default@ 3 seconds ago, lasted 41 milliseconds
commit f332a4dc458cf1815e49188d19eafe6aacd4d37a
args: jj -R .../repo commit -m 'agent: add b.txt'
... (six operations, down to "add workspace 'default'" and root())
--- jj diff --stat description(exact:"base\n")..@-
a.txt | 1 +
b.txt | 2 ++
2 files changed, 3 insertions(+), 0 deletions(-)

$ receipt.sh verify receipt.txt allowed agent-session; echo "exit=$?"
Good "agent-receipt" signature for agent-session with ED25519 key SHA256:1wGnmRUr8RqsBBibU/A4npmRfM3K5hM0Vw9L9gr2/1Q
exit=0

$ printf X | dd of=t.txt bs=1 seek=100 conv=notrunc      # t.txt = copy of receipt.txt
$ cmp -l receipt.txt t.txt
 101  60 130
$ receipt.sh verify t.txt allowed agent-session; echo "exit=$?"
Signature verification failed: incorrect signature
Could not verify signature.
exit=255
```

## Not verified, and limits

- Not run on Linux. The jj and OpenSSH behavior was only seen on Windows (Git Bash). The script uses nothing Windows-specific, but that is untested.
- The receipt proves the text was signed by the key and not altered after. It does not prove the op log is true: an agent holding the key can sign any text. Binding the receipt to the repo (checking that the `head` commit id exists and that the op log matches the repo's actual `.jj/repo/op_store`) is not done here.
- `jj op log` records the OS user and hostname (`frank@Starlight`), not the `JJ_USER`/`JJ_EMAIL` identity used for commits. The receipt carries the machine identity.
- Key trust is the `allowed-signers` file passed to `verify`. Key distribution, rotation and revocation are out of scope.
- jj's own commit signing (`signing.backend = "ssh"`) was not tested. This gate signs a separate receipt file instead.
- Only ed25519 was tested.
