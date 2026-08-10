# Screenshot capture protocol

## Why

Ship gates and the pattern library need **rendered evidence**, not vibes.

## Naming

```text
{product}-{surface}-{viewport}-{state}-{YYYYMMDD}.{png|webp}
```

Examples:

- `acme-job-home-390-empty-20260811.png`
- `acme-job-result-1280-success-20260811.png`

## Required pack (MVP ship)

| # | Surface | Viewports |
| --- | --- | --- |
| 1 | Marketing or app home | 390, 1280 |
| 2 | Primary job in progress | 390, 1280 |
| 3 | Primary job success | 390, 1280 |
| 4 | Empty state | 390 |
| 5 | Error state | 390 |
| 6 | Settings | 390 |

Store apps add: 6.7" and 5.5" frames (or Expo screen size equivalents).

## How to capture

### Local web

```bash
# Playwright one-off (if project has it)
npx playwright screenshot http://localhost:3000 docs/evidence/home-1280.png --viewport-size=1280,800

# Or Hermes computer_use / dogfood skill with save path
```

### Expo

- iOS Simulator + Android emulator screenshots  
- Or EAS build → device  

### Estate agent path

```text
Load dogfood or computer_use.
Visit {{url}}.
Capture required pack to {{repo}}/docs/evidence/{{date}}/.
Return file list + short notes per frame.
```

## Quality bar

- Real content (no lorem)  
- No debug borders / unfinished hover  
- Light **or** dark consistent with product default  
- Personal data redacted  
- File < 2MB preferred (webp ok)  

## Cataloguing into App Factory library

1. Keep binaries in **product repo** `docs/evidence/`  
2. Add a row to `examples/screenshots/INDEX.md` with relative or GitHub URL  
3. If pattern is novel and winning, create `patterns/P-….md` + link shots  

## INDEX format

```md
| Date | Product | Files | Pattern IDs | Notes |
| --- | --- | --- | --- | --- |
| 2026-08-11 | example | link | P-JOB-01 | first pack |
```
