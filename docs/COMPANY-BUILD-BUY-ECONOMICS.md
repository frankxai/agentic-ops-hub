# Company software: staged build and buy economics

TL;DR: Start with existing products and inexpensive tools, own the recurring workflows that distinguish the business, and admit a full CRM or DAM only after measured need pays for development and maintenance.

Prepared 11 October 2026. This is a reusable proposal, with engineering estimates and example workloads. It is not an invoice audit, a promise of vendor parity, or a measured savings result. The founder-specific baseline and repo observations stay in private research.

## What to count

Compare a job of equal scope, volume and quality through four options: existing subscription/free plan; paid SaaS plus a bounded adapter; adopted maintained software; proprietary implementation. A generated dashboard is an interface candidate. Authentication, authorization, migrations, data quality, recovery, support and upkeep still require engineering.

First-year cash = incremental licenses + runtime/API/data usage + migration/purchase + external engineering. Existing subscriptions belong in the baseline. Show optional API use separately: subscription-covered local work may add no invoice, while an unattended cloud runtime commonly uses separately billed provider credentials. Verify account terms and quotas before routing. Do not price every subscription token again as incremental cash.

Economic cost = first-year cash + founder hours valued at an explicit scenario rate + expected incident/support effort. A pre-revenue founder's time rate is a sensitivity input, not earned revenue. An unbought enterprise plan is not an avoided expense. Track opportunity cost without inventing lost sales.

Payback applies only if matched-scope monthly avoided cost exceeds owned operation plus maintenance. Otherwise record no cost-saving payback. Product differentiation is a separate investment hypothesis requiring customer evidence.

## Current pricing anchors

USD list/reference rates retrieved 11 October 2026; taxes, promotions, extra seats and credits can change the invoice. Confirm checkout before buying.

| Tool | Reference price and boundary | Decision at low volume |
| --- | --- | --- |
| Notion | Existing plan and entitlements must be inspected; no price assumed here | Keep a small relationship list when already paid; use exportable fields and stable IDs |
| HubSpot Sales | Free for up to two users; Professional $90/seat/month on annual billing plus $1,500 required onboarding; current Starter displays $7 promotion against $20 | Use free/basic features before Professional; Sales is not the complete marketing suite |
| Attio | Free up to three seats and 50,000 records; paid plan/additional credit checkout must be verified | Consider Free if communication sync and relationship activity save recurring work |
| Clay | FAQ: Launch starts $185/month, Growth $495/month; displayed annual effective rates $167/$446; Actions and Data Credits are separate | Defer recurring paid plan before an acquisition workflow is proven; BYOK still uses Actions |
| Eagle | Latest published price adjustment: $34.95 one-time; store states two devices and lifetime updates; 30-day trial | Trial as an optional local browser; preserve authoritative asset IDs/rights elsewhere |
| R2 Standard | $0.015/GB-month; free 10 GB-month, 1M Class A and 10M Class B operations; Internet egress free | Good private object store where already accepted; previews, metadata, backup and compute are extra |
| Cloudinary Image/Video API | Free 25 monthly credits; Plus $99/month or $89 effective on annual billing | Use a bounded free experiment if useful; pay only for a measured transformation/delivery job |
| Firecrawl | Free 1,000 refreshed monthly credits; Hobby $19 monthly/$16 annual effective for 5,000 credits | Crawl only sources needed for the experiment; extraction and agent use can have different meters |
| Apify | Free $5/month usage; Starter $19 prepaid usage plus PAYG; Free/Starter compute $0.20 per GB-RAM-hour | Choose a specific actor, count actor/proxy/storage charges, set an actual spending limit |

Sources: [HubSpot](https://www.hubspot.com/pricing/sales?pql-source=sales-case-studies-page), [Attio](https://attio.com/pricing), [Clay](https://www.clay.com/pricing), [Clay credits](https://university.clay.com/docs/actions-data-credits), [Eagle price notice](https://www.eagle.cool/blog/post/price-adjustment-notice-2024), [Eagle store](https://en.eagle.cool/store), [R2](https://developers.cloudflare.com/r2/pricing/), [Cloudinary pricing](https://cloudinary.com/pricing), [Cloudinary metering](https://cloudinary.com/documentation/billing_and_plans), [Firecrawl](https://www.firecrawl.dev/pricing), [Apify](https://apify.com/pricing).

R2 example: 500 GB stored throughout the month uses 490 billable GB-month after the allowance: 490 × $0.015 = $7.35. A second complete 500 GB copy in the same billed account makes 990 billable GB-month, $14.85 total. Independent backup storage, database, preview generation, Workers, monitoring and requests above allowances are excluded. R2's operation rounding can matter beyond allowances.

Cloudinary credits combine transformations, storage and bandwidth. A 500 GB master library does not fit the 25-credit free plan merely because it has few visitors. Keep archive masters and delivery derivatives in the deliberately selected tiers. The published rates concern Image/Video API plans; do not assume an enterprise DAM subscription has that price.

## Build estimates and token scenarios

Hours include design, implementation, relevant authorization tests, integration, failure/recovery, review repairs and handoff. They are total focused human engineering/review effort assisted by agents, not machine runtime. They assume existing compatible foundations and a capable engineer. Estimates have low confidence until a 10-20 hour measured slice supplies actual throughput.

The token ranges count aggregated billed input and output, including reasoning when billed and failed attempts. They are planning assumptions, not predictions from lines of code. They exclude image/video generation, tool charges, licensed contact data and provider/broker uplifts. No caching discount is assumed.

[OpenAI Standard short-context reference prices](https://developers.openai.com/api/docs/pricing): gpt-6.1-sol $2 input/$10 output and gpt-6-astra $10 input/$50 output per million tokens. An illustrative 70% Sol/30% Astra mix by input and output token volume costs $4.40 input/$22 output per million. This is a comparison scenario, not an instruction to route every job that way. Long-context rates differ. Subscription-covered usage has a different cash treatment.

| Scope | Founder/engineer hours | Input/output million tokens | API-equivalent USD at illustrative mix | Calendar at 20 focused h/week |
| --- | ---: | --- | ---: | --- |
| Existing CRM setup | 2-8 | Not estimated; manual setup can dominate | Not asserted | Under one week |
| Deploy and verify a maintained OSS CRM | 24-80 | 2-10 / 0.3-1.5 | $15.40-$77 | 1.2-4 weeks |
| Three proven agent actions over an existing app | 12-40 | 2-8 / 0.3-1.2 | $15.40-$61.60 | 0.6-2 weeks |
| Extend existing VIS DAM workflow | 40-120 | 8-30 / 1.2-4.5 | $61.60-$231 | 2-6 weeks |
| Connect existing CMS to approved assets | 24-80 | 4-16 / 0.6-2.4 | $30.80-$123.20 | 1.2-4 weeks |
| Focused research/enrichment workflow | 40-100 | 6-25 / 0.9-3.75 | $46.20-$192.50 | 2-5 weeks |
| Focused owned CRM | 120-300 | 20-80 / 3-12 | $154-$616 | 6-15 weeks |
| Commercial CRM with bounded feature set | 800-2,000 | 200-800 / 30-120 | $1,540-$6,160 | 40-100 weeks |
| New commercial DAM with bounded feature set | 1,200-3,000 | 300-1,200 / 45-180 | $2,310-$9,240 | 60-150 weeks |
| Customer-owned install/update/export package | 40-140 | 8-35 / 1.2-5.25 | $61.60-$269.50 | 2-7 weeks |

A focused CRM means contacts/companies, one pipeline, notes/tasks, import/export, scoped permissions and an audit trail. It excludes full email/calendar sync, enterprise reporting, campaigns, telephony, deliverability, a marketplace and HubSpot parity. The commercial CRM estimate adds multi-user onboarding, subscription integration, operating/support work, migration and upgrades, while retaining that bounded scope. A full incumbent suite can take substantially longer.

A new commercial DAM estimate covers ingest/versioning, catalog search/preview, authorization, browser workflow, restore/export, updates and operation. It excludes building a design editor, a video codec platform or every enterprise integration. Extending existing VIS avoids much of that replacement work.

At 10 h/week, double the calendar figures; at 40 h/week, halve them only if those focused hours are actually available. More agents do not remove sequential integration, customer feedback and founder review. Shared foundations overlap: do not add every table row as a fleet total.

Example focused-CRM work breakdown: domain/import 16-40 h; authentication/permissions 20-50; usable pipeline/search/tasks 32-80; integration and agents 20-50; recovery/export/security 20-50; review/handoff 12-30. Sum 120-300 h. Measure each component after the first slice.

At an illustrative €75/h, focused CRM time is €9,000-€22,500, excluding USD API/runtime costs. At €25/h it is €3,000-€7,500; at €150/h €18,000-€45,000. These figures price constrained founder attention; they are not lost revenue forecasts. Keep USD and EUR separate until an explicit FX input and tax treatment are recorded.

## When buying wins

Adopting a maintained OSS CRM avoids much of the domain/UI implementation but still needs installation, authentication, backup/restore, import/export, upgrades and any agent adapter. The 24-80 hour adoption estimate covers a supported community deployment and verification, not custom email synchronization or a commercial product fork. Budget an illustrative 3-8 maintenance hours/month until measured; hosting and any required commercial license are additional. Compare that with an existing free/paid service before operating another database and worker stack.

For a $44/month example SaaS seat, $528/year buys substantial ready-made behavior. A $20/month owned runtime plus 2 maintenance hours/month valued at an illustrative $75/h has $170/month economic operation, before build cost. The vendor checkout rate and equivalent scope must be verified; this example is a sensitivity case.

For a $495/month Clay-style workflow, an illustrative owned pipeline might use $50 hosting, $25 crawling/actors, $100 licensed data/verification and $40 inference each month: $215 cash. Add four maintenance hours at an illustrative $75/h: $515/month economic operation. Cash is lower, but no economic cost-saving payback exists under those assumptions. Email quality and data coverage are still unproven. At higher volumes or materially less maintenance the result can reverse; calculate again with measured data.

Scraping replaces a specific acquisition/extraction step. It does not automatically replace licensed datasets, email verification, provider waterfalls, suppression/consent, identity matching, delivery and debugging. Track cost per usable accepted record, including duplicates and unsuccessful requests.

## Stage policy

Calendar windows are review dates, not revenue promises or automatic build permission.

| Window | Business priority | Software admission |
| --- | --- | --- |
| Weeks 0-6 | Finish a credible sellable artifact, delivery and distribution; collect real customer feedback | Existing CRM; one useful VIS/CMS path; prove a small shared action set; no full CRM |
| Months 2-3 | First repeatable purchases or repeated active customer use; compare activation and support burden | Add the repeat workflows observed in delivery; consented activity adapters and cost telemetry |
| Months 4-6 | Repeatable creation/delivery and evidence that operators want the workflow | Package one customer-owned install with updates/export/restore; consider adopted CRM only for demonstrated pain |
| Months 7-12 | Distribution and retention of the chosen product; sustainable support and operation | Modular installation recipes, selected connectors, stronger tenant/update controls; owned CRM only with a specific case |
| Year 2 | Decide which repeatable capability deserves a standalone commercial product | Broader proprietary CRM/DAM only with customer evidence, maintainable margins and a funded roadmap |

Suggested initial time policy: 70% on sellable outcomes, activation and distribution; 20% on shared creation/delivery improvements; 10% on speculative infrastructure/R&D. Preserve the existing portfolio and its owners. Limit simultaneous revenue builds and shared primitives according to the current accepted Registry. Rebalance after measured bottlenecks, not enthusiasm for a tool.

Build when repeated customer/operator use, inability of a serious alternative to do the job, realistic maintenance and a valuable owned product justify it. Buy when the vendor removes more distraction than it costs. Adopt OSS when its supported extension/API and license fit the proposed operation and distribution. Defer when no customer task needs the layer.

## OSS and template choices

Keep current Git/MDX CMS until editorial collaboration needs a structured editor. Payload is a candidate for a selected Next.js CMS migration, with a current [MIT license](https://github.com/payloadcms/payload/blob/main/LICENSE.md); benchmark the existing editor before introducing it.

Evaluate Twenty for an eventual existing-CRM alternative through its documented APIs/application interfaces. Its current [license](https://github.com/twentyhq/twenty/blob/main/LICENSE) includes AGPL, explicitly marked commercial enterprise files, MIT packages and an application exception. Do not label the entire product permissive or assume an embedded proprietary fork has the same terms. Frappe CRM is another candidate where the Frappe ecosystem fits; do not deploy both to compare a spreadsheet job.

n8n can help a business operate internal workflows. Its [Sustainable Use License](https://docs.n8n.io/sustainable-use-license/) requires a separate check for customer-facing hosting, redistribution and embedding. “Self-hosted” does not grant unlimited resale rights or remove maintenance. Keep one authoritative workflow owner when using it as an adapter.

Use v0/templates for a fast interface draft, then integrate the existing domain operations and prove permissions, failed states, import/export and upgrades. Selectively buy a good component instead of paying to reproduce it. Do not turn a generated UI into a claim that a CRM is production ready.

## Monthly decision routine

Use the existing decision log and issues. Each proposed purchase/build records job, owner/source revision, matched alternatives, observed demand, included/excluded functionality, licenses, forecast/actual hours, token/cash meters, maintenance, exit cost, verdict, next review date and evidence confidence.

Run a 10-20 hour bounded experiment before a large build. Change one relevant capability, measure accepted usable results and repair effort, and preserve negative results. The [swarm programme](COMPANY-SWARM-BUILD-PROGRAMME.md) makes this economic check part of admission.
