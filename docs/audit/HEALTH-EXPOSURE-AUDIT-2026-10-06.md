# Health Intelligence System: public exposure audit (2026-10-06)

Target: `frankxai/health-intelligence-system` (PUBLIC). Read-only audit. Nothing in the target repo was modified, and no visibility, delete or force-push command was run. No sensitive text is quoted here; findings cite path, commit and a one-line classification only.

## 1. Verdict

**CLEAN for personal medical content and secrets, with 4 low-severity SUSPECT notes (below). Confidence: high for git history and the 4 release ZIPs, medium overall.** Not checked: wiki, forks' contents, issue/PR comment bodies, Actions logs and artifacts, and GitHub-side unreachable objects (details in section 6).

The 2026-09-01 internal report said medical documents were "not read" and the repo "might need to be private". That concern is not supported by evidence: after path enumeration of all 225 files ever tracked plus pattern scans and targeted reads of fixtures, templates and demo seeds, no personal medical record was found. Going private is not required for exposure reasons. A guard is still worth adding (section 4), because the project plans real subject-zero ingestion.

## 2. What was examined

| Scope | Result |
| --- | --- |
| Clone | Full, non-shallow. 24 commits on branches and 28 once `refs/pull/*/head` was fetched. Local branches: `main`, `agent/hermes/bios-v01`, `codex/performance-learning-20260906`, `codex/vitalis-foundation-20260824`. |
| Files ever tracked (`git log --all --name-only --diff-filter=AMR`) | 225 unique paths, 141 in the current tree. Identical set before and after fetching PR refs. |
| Binary/record-type paths | The only non-text files are `assets/health-intelligence-system-banner.png` and `apps/bios-steward/src/app/favicon.ico`. No PDF, DICOM, JPEG, XLS(X), SQLite, ZIP, `.env` or key files in any commit. |
| Secrets, full history `-p` | Regex sweep for AWS, GitHub, Anthropic/OpenAI, Slack and Google keys, private-key blocks, JWTs and generic `key/secret/token/password = <16+ chars>`: **0 hits**. gitleaks and trufflehog were not installed, so this is grep-only. PR #3's body says gitleaks full-history passed (self-reported, not verified here). |
| Personal identifiers | Commit metadata only (see S1). Phone/SSN/ID-shaped regexes matched only ISBNs in book citations. No other e-mail addresses in any added line. |
| First-person / patient-style content | Regex for "my diagnosis/cancer/labs/doctor…", "I was diagnosed…", DOB, MRN, named providers, hospital/clinic, lab units and markers. The only hits were prompts and templates phrased as user questions or refusals. |
| Releases | 4 releases (v0.1.0, v0.1.1, v0.2.0, v0.2.1). All 4 main ZIPs were downloaded and listed, and the v0.2.1 ZIP plus the agent pack were also scanned for secrets and e-mails. Contents match repo docs, templates, commands and prompts only. |
| Issues / PRs | 0 issues. 5 PRs (#1 to #5): bodies state synthetic/fictional data only, which matches the diff content. |
| Metadata | Description and topics contain no private context (see S3). 1 star, 0 forks per the API. |

## 3. Flagged items

| Path | Commit(s) | Classification |
| --- | --- | --- |
| `fixtures/gut/fictional-family.json` | PR #1 (merged 2026-07-29), present on `main` | Fictional fixture (`"fictional": true`, alias only). Not real. |
| `fixtures/wellness/fictional-daily.csv` | PR #4 | Synthetic constant values (sleep 6.5 h, steps 6000). Not real. |
| `bios/templates/*`, `templates/health-record-index.md`, `templates/private-vault-manifest.md`, `templates/medication-supplement-inventory.md`, `templates/side-effect-log.md`, other `templates/*.md` | v0.1.0 onward | Blank templates with `<placeholder>` fields. Framework. |
| `commands/cancer-*.md`, `docs/cancer-detection-prep-treatment.md`, `MEMORY.md`, `SOUL.md` | v0.1.0 onward | Product/module description, "never recommend treatment". Framework. |
| `apps/bios-steward/src/lib/store.ts`, `design-loop-evidence.json` (history only; absent from the current tree) | `15b704a` | Demo seed: "You / Grandma / Demo household", "demo seed". Not real. |
| `prompts/*.md` | v0.2.x | System prompts that refuse diagnosis and lab interpretation. Framework. |
| `release-manifest.json` | `347b424` | Tracked despite being listed in `.gitignore`. Checksums only. Harmless (see S4). |

No item was classified as real personal content.

### Low-severity SUSPECT notes (not medical)

- **S1: personal e-mail in commit metadata.** 22 of 28 commits carry the author address `friemerx@gmail.com` (the other 6 use the GitHub noreply address). This is publicly harvestable and is the only personal identifier found. It is not health data.
- **S2: stated intent to ingest real data.** PR #2's test plan lists "subject-zero real Apple/Garmin ingest" and a family ChatGPT project as to-dos. No such data is committed, and `_local/` and `private/` are gitignored, but this is the plausible path to a future leak. This is the main reason for the guard in section 4.
- **S3: repo description.** The description reads as a personal and community health mission statement (and has a typo, "peparations"). It leaks no private context.
- **S4: `.gitignore` drift.** `release-manifest.json`, `dist/`, `packages/` and `private/` are ignored, but `release-manifest.json` is tracked. There is no ignore rule for record-type extensions (PDF, DICOM, XLSX and so on), so nothing blocks someone from committing a real record.

## 4. Proposed `.gitignore` and pre-commit guard

### `.gitignore` additions (health repo)

```gitignore
# Personal health data must never be committed
_local/
vault/
*.vault/
*-record.*
*-records.*
*.dcm
*.dicom
*.nii
*.nii.gz
*.xlsx
*.xls
*.ods
*.pdf
!docs/**/*.pdf
*.heic
*.jpg
*.jpeg
*.tif
*.tiff
apple_health_export/
export.xml
*.fit
*.tcx
*.gpx
.env
.env.*
*.pem
*.key
```

Notes: `*.pdf` is blocked by default and only allowed under `docs/`. `*.png` is not blocked wholesale because the repo uses a banner image, so the guard checks image paths instead.

### `scripts/guard-no-personal-health.sh` (health repo; pre-commit hook and CI step)

```bash
#!/usr/bin/env bash
# Fails if staged (or, with --all, tracked) files look like personal health records or secrets.
set -euo pipefail
mode="${1:---staged}"
if [ "$mode" = "--all" ]; then files=$(git ls-files); else files=$(git diff --cached --name-only --diff-filter=ACMR); fi
bad=0
deny='(^|/)(_local|vault|private)/|-records?\.|\.(dcm|dicom|nii|nii\.gz|xlsx?|ods|heic|tiff?|fit|tcx|gpx|pem|key)$|(^|/)(export\.xml|apple_health_export/)|(^|/)\.env(\.|$)'
while IFS= read -r f; do
  [ -z "$f" ] && continue
  if printf '%s' "$f" | grep -Eiq "$deny"; then echo "BLOCKED path: $f"; bad=1; fi
  case "$f" in *.pdf) case "$f" in docs/*) ;; *) echo "BLOCKED pdf outside docs/: $f"; bad=1;; esac;; esac
done <<< "$files"
secret='(AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{30,}|github_pat_|sk-ant-|sk-[A-Za-z0-9]{20,}|-----BEGIN [A-Z ]*PRIVATE KEY)'
if [ "$mode" = "--all" ]; then
  git grep -nEI "$secret" -- . ':!scripts/guard-no-personal-health.sh' && bad=1 || true
else
  git diff --cached -U0 -- . ':!scripts/guard-no-personal-health.sh' | grep -E "^\+.*$secret" && bad=1 || true
fi
# Content heuristic: first-person medical facts, identifiers, lab-value lines in non-template text
pii='\b(MRN|DOB|date of birth)\b *[:=]|\b(my|his|her) (diagnosis|oncologist|biopsy|pathology) (is|was|showed)|\bI was diagnosed\b|\b(HbA1c|PSA|eGFR)\b *[:=] *[0-9]'
if [ "$mode" = "--all" ]; then
  git grep -nEIi "$pii" -- . ':!templates/' ':!prompts/' ':!docs/' ':!scripts/' && bad=1 || true
else
  git diff --cached -U0 -- . ':!templates/' ':!prompts/' ':!docs/' ':!scripts/' | grep -Ei "^\+.*($pii)" && bad=1 || true
fi
[ "$bad" -eq 0 ] || { echo "Guard failed: remove the data, or move it to a private vault outside this repo."; exit 1; }
```

Install (health repo, owner to run):

```bash
chmod +x scripts/guard-no-personal-health.sh
printf '#!/usr/bin/env bash\nexec scripts/guard-no-personal-health.sh --staged\n' > .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit
```

CI step to add to a workflow (runs on every PR):

```yaml
- uses: actions/checkout@v4
- run: scripts/guard-no-personal-health.sh --all
- uses: gitleaks/gitleaks-action@v2
  with: { args: "detect --log-opts=--all" }
```

The guard script is untested against edge cases. It should be run once against the current tree with `--all` before relying on it, and expect false positives in docs. Enable GitHub push protection and secret scanning in repo settings as well.

## 5. Owner actions, in priority order

None of these were run. No history rewrite and no visibility change is needed on current evidence.

1. **Keep the repo public, and do not rewrite history.** Nothing was found that would justify it. Closing the 2026-09-01 "might need to be private" item with this report is reasonable.
2. **Add the guard and ignore rules (section 4)** via a PR to the health repo, and enable push protection and secret scanning:
   ```bash
   gh api -X PATCH repos/frankxai/health-intelligence-system \
     -f 'security_and_analysis[secret_scanning][status]=enabled' \
     -f 'security_and_analysis[secret_scanning_push_protection][status]=enabled'
   ```
3. **Keep real subject-zero data out of this repo entirely.** Use a separate private repo or a local vault outside any git work tree, and point `BIOS_VAULT`-style paths there. Never use `_local/` inside a public repo's working directory without the ignore rules in place.
4. **Optional: stop publishing the personal e-mail (S1).** For future commits only:
   ```bash
   git config user.email "132689939+frankxai@users.noreply.github.com"
   ```
   and enable "Block command line pushes that expose my email" in GitHub, under Settings > Emails. Rewriting past commits (`git filter-repo --mailmap`, then force-push) is possible, but I do not recommend it for an address that is already public and not health-related.
5. **Optional hygiene (S4).** Remove `release-manifest.json` from the index without deleting the file: `git rm --cached release-manifest.json`. Fix the description typo:
   ```bash
   gh repo edit frankxai/health-intelligence-system --description "<corrected text>"
   ```
6. **If a real record is ever found in a future audit** (not the case today): rotate any exposed credentials first, then `git filter-repo --path <file> --invert-paths`, force-push all refs, contact GitHub Support to purge cached views and PR refs (`refs/pull/*`), and treat the data as disclosed.

## 6. Limits of this audit

- The wiki and forks pages returned 403 from this environment. The API reports `forks_count: 0`, and the wiki is unverified.
- Issue and PR comment bodies and review comments were not read. PR descriptions were read, and there are 0 issues.
- Actions logs and artifacts were not inspected.
- Release assets: v0.1.0, v0.1.1, v0.2.0 and v0.2.1 main ZIPs were listed. The v0.2.1 ZIP and agent pack were also scanned for secrets and e-mails. `release-manifest.json` and `agent-pack-manifest.json` were not diffed against the ZIPs.
- GitHub may retain unreachable objects (force-pushed or deleted refs) that git clone cannot see. Only live branches and `refs/pull/*/head` were scanned.
- Secrets scan was regex-based, with no entropy scanner (gitleaks/trufflehog unavailable offline here). Binary PNG/ICO content was not inspected. The PNG is a generated banner according to release notes.
- The content scan is heuristic. Free-text personal facts phrased in unusual ways could be missed, which is why 141 current files were also classified by path and the flagged text files were spot-read, not every line of all 225.
