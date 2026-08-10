# Pattern library — UI/UX recipes for rapid genius apps

**Purpose:** reusable **interaction + layout recipes**, not skin clones.  
**How to use:** pick ≤5 IDs into DESIGN-CONTRACT. Implement with local tokens + shadcn.  
**Evidence:** link screenshots under `screenshots/` when captured; external refs are research.

Legend: **P** = product app · **M** = marketing · **A** = agentic · **S** = store mobile

| ID | Name | Best for | Core rules | Refs |
| --- | --- | --- | --- | --- |
| P-JOB-01 | **Single-job home** | Micro-SaaS | One H1 job, one primary CTA, secondary links quiet | Linear-style focus; estate operator rule |
| P-JOB-02 | **Wizard 3-step** | Onboarding / generators | Steps named by outcome not tech; back always safe | SaaS onboarding 2026 |
| P-JOB-03 | **Result canvas** | Gen tools | Input dock + large result + regenerate/edit/export | Creator tools |
| P-JOB-04 | **Inbox zero ops** | Ops AaaS | Queue of tasks, status chips, bulk safe actions | Support tools |
| P-DASH-01 | **5-metric command** | B2B home | ≤5 KPIs, one attention list, no fake charts | SaaS dashboard practice |
| P-DASH-02 | **Role home switch** | Multi-role | Persona-based default layout | Enterprise SaaS |
| P-TABLE-01 | **Filterable work table** | Lists | Sticky header, density toggle, row action menu | Linear/Notion tables |
| P-DETAIL-01 | **Split list-detail** | Desktop productivity | URL-selected detail; mobile becomes stacked | |
| P-CHAT-01 | **Agent sidekick** | AaaS | Chat is side panel; main canvas is the work | Not full-screen chat-only |
| P-CHAT-02 | **Structured agent turn** | Tools | Show tool cards, confirmations, receipts under message | assistant-ui patterns |
| P-AUTH-01 | **Calm auth** | All | Email magic or OAuth; no dark patterns; legal links | |
| P-SET-01 | **Settings islands** | All | Group by risk; danger zone separate | |
| P-EMPTY-01 | **Empty = next action** | All | Illustration optional; one CTA that starts job | |
| P-ERR-01 | **Recoverable error** | All | What happened, what to do, retry, support | |
| P-PAY-01 | **Upgrade moment** | SaaS | Triggered by value limit, not random modal | |
| P-NAV-01 | **Left rail desktop / tab mobile** | Apps | ≤5 primary nav items | |
| P-NAV-02 | **Command palette** | Power users | Cmd-K actions + navigation | |
| P-MKT-01 | **Problem→proof→CTA** | Marketing | Hero job statement, proof strip, single CTA | FrankX clear mode |
| P-MKT-02 | **Interactive demo stub** | Marketing | Fake-data demo of job without signup wall first screen | |
| P-MOB-01 | **Thumb-zone primary** | Expo | Primary CTA bottom-safe; nav reachable | Store apps |
| P-MOB-02 | **Permission just-in-time** | Expo | Ask when needed with benefit copy | |
| P-A11Y-01 | **Focus ring system** | All | Visible focus; skip link; form errors tied to fields | harness A11Y |
| P-MOTION-01 | **Cause→effect only** | All | 150–250ms; reduced-motion = instant state | SDI motion gates |
| P-AGENT-01 | **Allowlist tool tray** | AaaS | Tools visible; pending confirmations queue | MCP-era UX |
| P-AGENT-02 | **Receipt timeline** | AaaS | Every side effect listed with undo/support path | Trust |
| P-STORE-01 | **Store screenshot narrative** | Listings | 1 value, 2 job, 3 result, 4 social proof, 5 settings | Play/iOS |

## Estate before/after examples (owned)

| Path | Lesson |
| --- | --- |
| `starlight-design-intelligence/examples/frankx-hero-before-after.md` | Clear founder hierarchy |
| `starlight-design-intelligence/examples/sis-dashboard-before-after.md` | Ops density without noise |
| `starlight-design-intelligence/examples/arcanea-academy-before-after.md` | Mythic without fog |

## External research libraries (do not vendor wholesale)

- https://www.saasui.design/ — live SaaS pattern museum  
- https://ui.shadcn.com/ — component foundation  
- https://github.com/garrytan/gstack — cognitive review modes  
- assistant-ui / shadcn chat kits — only if chat is required  

## Adding a pattern

1. Copy `examples/patterns/_TEMPLATE.md`  
2. ID convention `P-AREA-##`  
3. Add screenshot paths when available  
4. One PR / commit note why it earned a slot  

## Screenshot index

See `screenshots/README.md`. Binary screenshots may live in product repos; this library stores **metadata + links**.  
