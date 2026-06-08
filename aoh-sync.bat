@echo off
cd /d "%~dp0"
del /f /q ".git\index.lock" 2>nul
(
  git add -A
  git commit -m "feat: AGENTS.md source-of-truth + multi-format sync + ecosystem positioning" -m "- Repoint sync engine: AGENTS.md is canonical, fan out to .cursor/rules/*.mdc, .clinerules/, copilot-instructions.md, ACOS SKILL.md with tamper-evident headers" -m "- Add --check (CI drift gate) and --legacy modes" -m "- CLAUDE.md becomes thin @AGENTS.md shim" -m "- README: exact Agentic Ops vs AIOps table + FrankX ecosystem layer map" -m "- docs/layering.md: what-goes-where decision table"
  git push origin main
) > aoh-sync.log 2>&1
echo done >> aoh-sync.log
