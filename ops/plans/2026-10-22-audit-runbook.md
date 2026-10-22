# Agent Setup Audit: runbook (draft, 2026-10-22)

Author: Claude Code. Status: draft for review by a different harness. For an agent or Frank to follow on a prospect's setup. **Read-only.** Offer: `2026-10-22-audit-offer.md`.

Every check below is a defect class we found in our own system. Sources: `ops/sessions/2026-10-21-routing-brain-hardening.md` (rounds 1-13 on PR 377, abbreviated "R1" to "R13"), the PR 379 review (`b30511f`, "379"), the receipt verifier docs (`docs/receipts.md` in the Starlight Intelligence System repo, SIS PR 481, "481"), and `fleet/ROUTING-BRAIN.md` section "What the guarantee covers". PR 377 and PR 481 are open drafts; where a check cites a fix, the fix is in review, not shipped.

## 0. Before you start: scope and consent (all must be yes)

- [ ] The person in front of you owns, or is authorised in writing to share, the machine and every account in scope.
- [ ] Scope is written down: which config files, which gateway or provider accounts, which receipts or ledgers.
- [ ] They know how you will process what you see (section 5), including whether any model will read their configuration.
- [ ] No production credentials will be created, rotated or revoked by you. They do that.
- [ ] They know the stop conditions (section 6).

## 1. Evidence rules

1. **Never print, copy, log, screenshot or retain a secret value.** Report a setting's name and class (`env-reference` or `LITERAL`), never its value. Do not paste a config file into a chat window, a ticket or a model prompt.
2. Use the inspector for config files: `python -I scripts/audit_inspect.py <config.json>`. It prints JSON pointers, value classes, endpoint **hostnames only**, model provider prefixes and provider lists. It is name-based: it will miss a secret stored under a field whose name does not look like a secret, so also ask the owner whether any key lives elsewhere.
3. Prefer counts and booleans (`rg -c`, `rg -l`) over matching lines. Never use `rg -o` or `-n` on anything that might hold a secret.
4. Redact usernames and absolute paths in the report to a placeholder (`<home>`). Customer and project names only with consent.
5. Every finding records: check id, file and setting (pointer), tool version seen, what was observed, and how to reproduce it without the secret.
6. If a model reads the evidence, it must run on a route the owner approved in section 0; do not send their configuration to a provider you have not named to them.

## 2. Checks

Severity scale (same as our reviews): **P1** a way for data or credentials to reach a destination the owner did not intend, or an unbounded loss; **P2** a control that fails under a plausible condition; **P3** hygiene or documentation. Record the observation, not an opinion.

| Id | Check | How (read-only) | Finding when | Our source |
|---|---|---|---|---|
| C1 | Provider keys in plaintext config | Inspector: `SECRET-FIELD ... LITERAL`. Ask where else keys live (shell profile, `.env`, CI). Ask whether a key was ever pasted into a chat or ticket. | Any `LITERAL` provider key. Pasted-in-chat counts as exposed: owner rotates. | Product plan 4.1; `lab/gates.json` `dec-token-pass-key` (key pasted in chat, in plaintext in the OpenCode config) |
| C2 | Provider endpoint overrides | Inspector: `ENDPOINT` hosts and `ENDPOINT-FIELD` for `baseURL`, `api`, `npm`, also model-level. Compare hosts to the gateway hostname the owner intends. | A `baseURL`, `api` or `npm` override on a provider the owner thinks is the gateway, or a host that is not the gateway. | R13 P1 (copying the whole global provider block kept a hostile `baseURL`; fixed in `c2dd301`, in review) |
| C3 | Ambient models and providers | Inspector: `MODEL`, `FALLBACKS` prefixes, `ENABLED_PROVIDERS`, `DISABLED_PROVIDERS`. List every model reachable from every agent, category and fallback, including the small model used for titles and sub-agents. | Any provider prefix that is not the intended gateway; a free-tier provider enabled beside the gateway; fallbacks that differ from the primary's data rule; a missing `small_model`. | R12 P1 (side calls used an ambient model); R7 P1 (free-agent routes bypassed the gateway); R1 P1 and R2 P1 (an empty fallback list made agents inherit free fallbacks) |
| C4 | Which config actually applies | Record the OpenCode version. Ask how agents are started: plain `opencode run`, with `--standalone`, through a wrapper. Note `OPENCODE_CONFIG`, `OPENCODE_CONFIG_DIR`, `OPENCODE_CONFIG_CONTENT` and project-level config presence (names only). | The owner believes a config pins the model but the launch path ignores it. We observed on opencode 2.1.2 that without `--standalone` a run goes to a managed service that does not see the client's environment. Version-bound: re-test on theirs, do not assume. | R12 (empirical check recorded in the session note) |
| C5 | Launcher and Windows shim injection | `where.exe opencode` (Windows) or `command -v opencode`. Is it a `.cmd`/`.bat` npm shim? Do any wrappers or runners build a command string, use `shell=True`, or pass task text without `--`? Does task text come from untrusted places (issue titles, PR bodies)? | A shim is executed with task text in its arguments, or a command line is built by string concatenation. | R13 P1 (task text reached `cmd.exe` through the `.CMD` shim; fixed by running the native executable, in review) |
| C6 | Routing decided by prompt keywords | Read the routing rules. Is the route chosen by matching words in the prompt? | Any claim that such a classifier protects sensitive data. It is a cost heuristic, not a boundary. The control is a gateway key restricted to zero-data-retention providers (C7). | R1-R6 and Option A (every round found another phrasing that slipped through); `fleet/ROUTING-BRAIN.md` guarantee section |
| C7 | Gateway key controls | With the owner at their dashboard or CLI: list keys with names, caps, last use, and whether a key is restricted to zero-data-retention providers. Whether `ai-gateway api-keys list` shows that restriction is **unverified**; check the dashboard. Compare each cap to the pool. | A key whose cap equals the whole shared pool (a leaked key can spend all of it); no ZDR-restricted key for sensitive work; unused keys still live; keys named by tool but shared by several. | `lab/budget.json` (caps set on every key "so one leaked key has a bounded loss"); `dec-delete-low-budget-keys`; session observation 2026-10-22 that Token Pass keys each carried an $80 cap equal to the shared pool (not in a repo file) |
| C8 | Spend checked before the call | Ask how a cap is enforced: provider limit only, or a reserve before each call and a settle after. Ask what happens when two runners start together, when a run dies, and when the month changes (which timezone). | Spend is only counted after the fact; two callers can pass the same headroom; an expired hold frees its budget while the call may still run; month boundaries use local time. | R1 P1 (no hold; two callers passed the cap), R2 P1 (hold expiry released budget; spend reached $80.50 on an $80 cap), R3 (rounding), R7 P2 (month boundary compared without converting to UTC), R12 P2 and R13 P2 (a hold could not be settled once its model left the chain) |
| C9 | Run records | Where is the ledger? One per machine, per checkout, or shared? Count lines and check each ends with a newline (counts only). Do records hold prompts or outputs? | Each checkout writes its own budget; records contain prompt or output text; a truncated last line can swallow the next record. | R1 P1 (each worktree had its own receipts directory), R4 P1 (unterminated tail line swallowed the next receipt), product plan 5 (receipts hold hashes only) |
| C10 | Signed receipts verify | Only if they issue run receipts (SIS run-receipt v1). Needs the verifier from SIS PR 481: `starlight verify-receipt <file.json> --public-key <pub.pem>`. Exit `0` verified, `1` rejected, `2` invalid input. Trust only keys the owner confirms are theirs. | Exit `1`; or a receipt that verifies but fails C11; a trusted key file that is a small-order point (the command refuses it with exit `1`). | 481: Codex passes on the verifier found forgiving base64 decoding, entries with bad signatures beside good ones, and small-order keys; `docs/receipts.md` lists what the verifier does not check |
| C11 | Maker is not the checker | In a verified receipt, compare the accepting decision's actor with `run.host`. Also read how "tests passed" reaches the record: computed by CI or a script they ran, or reported by the agent itself? | The same harness made and accepted the work; acceptance is self-asserted. A signature does not prove the checker ran. | PRD A5; PR 379 review (the bridge cannot prove who accepted; labelled `provenance=self-asserted`); `docs/receipts.md` "What the verifier does NOT check" |
| C12 | Generated config drift | Compare the generated agent config on disk with what its generator would emit now (ask when it was last regenerated). Are backups kept, and is the oldest copy preserved? | The file on disk is old generator output; backups are overwritten by a second run within the same second. | `2026-10-21-harness-measurement-and-scale.md` section 2 (`~/.omo/omo.jsonc` stale); R7 P2 (second-resolution backup names overwrote the original) |
| C13 | Process lifecycle | Do scheduled runners have timeouts? List processes by name (do not kill any). Look for agent processes older than the runner that started them and for temp directories left behind. | A timeout kills the wrapper but leaves the agent running; temp config directories with credentials survive a crash. | R13 P2 (outer timeout killed the wrapper, not OpenCode, and skipped credential cleanup); residual limits in `fleet/ROUTING-BRAIN.md` |

Not in this audit: model quality, prompt content, their business data, anything that needs write access or running their code.

## 3. Findings template

```
ID: F-<nn>            Check: C<n>            Severity: P1 | P2 | P3
Where: <redacted path>#<json pointer>   Tool/version: <name x.y.z>
Observed: <one sentence, no secret value>
Why it matters: <the concrete way data, credentials or money could go wrong>
Reproduce (without the secret): <command or steps>
Fix (smallest): <change>   Owner effort: <unmeasured unless you timed it>
Status: open | fixed by owner | accepted risk (owner's words)
```

Report outline: scope and consent record; tools and versions seen; findings by severity; what was not checked; owner's accepted risks; next review date. Do not put a score or a "compliant" label on it.

## 4. Order of work

1. Scope and consent (section 0).
2. C4 and C5 first: they decide whether the other checks describe what really runs.
3. C1 to C3 with the inspector, then C6 to C9 by questions, then C10 to C11 if receipts exist, then C12 to C13.
4. Write findings the same day; raw notes are deleted at handover (section 5).

## 5. Data handling (proposal; Frank to confirm)

- Keep only the report and the consent record. Working notes and exports are deleted when the report is handed over. [Frank decides: retention period for the report itself.]
- Do not store their config on shared systems or in git. Do not write their findings into starlight-memory (estate rule: no untrusted session text in memory).
- If any personal data of third parties appears (names in logs, prompts), stop and ask the owner to redact before continuing.
- If the prospect is in the EU and any personal data will be processed, a data-processing agreement may be needed. **Not assessed here; needs legal review.**

## 6. Stop conditions

Stop, tell the owner, and do not continue the check if:

- A secret value is displayed on screen or in output. Tell them to rotate it. Do not copy it anywhere.
- A step would need write access, running their code, or changing a setting. The audit is read-only.
- You find a live credential with broad scope (for example a cloud root key). Tell them at once; do not test it.
- Personal data of third parties is in the evidence.
- The person cannot show authority over the machine or accounts, or scope changes without a written update.
- They ask for a compliance conclusion, legal opinion or guarantee. Decline; point to the offer's "does not claim" list.

## 7. Worked example: our own machine, 2026-10-22

Run of `scripts/audit_inspect.py` on the owner's global OpenCode config, output reduced to classes (no values):

| Pointer | Class | Check | Finding |
|---|---|---|---|
| `/provider/vercel/options/apiKey` | LITERAL | C1 | P2: key in plaintext; the config has no `{env:...}` reference for it |
| `/provider/omniroute/options/apiKey` | LITERAL | C1 | P3: local lab provider, key literal |
| `/model` | provider prefix `opencode` | C3 | P2: default model is the free `opencode` provider, outside the gateway key |
| `/enabled_providers` | `["opencode","vercel"]` | C3 | P2: free provider enabled beside the gateway |
| `/provider/omniroute/options/baseURL` | host `localhost` | C2 | P3: intended local endpoint, labelled non-confidential in the config; record as accepted |

An earlier exposed key was removed after the owner rotated it; the key now in the file is its replacement and is still literal. The items above are open at the time of writing; they are the reason the strict launcher exists (R12, R13). This table is an internal worked example. Do not show it to a prospect without Frank's consent.
