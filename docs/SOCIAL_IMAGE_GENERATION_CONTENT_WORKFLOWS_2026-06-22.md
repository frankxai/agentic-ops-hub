# Social And Image Generation Content Workflows

Created: 2026-06-22  
Purpose: build a high-performance content production system for FrankX, Starlight, Arcanea, GenCreator, AI CoE, Mind Intelligence, and client/community templates.

## Current Platform Read

### Instagram

Current signal:

- Instagram is pushing original content harder, including photos and carousels, not just Reels.
- Reposted, low-effort, or unmodified third-party content is a risk for recommendations.
- Carousels can carry deeper educational content and can now include up to 20 photos/videos in a single feed post.
- Reels still matter for reach; Stories matter for relationship and retention.

Operating conclusion:

- Use original AI-assisted visuals, not reposted screenshots.
- Use carousels for frameworks, guides, diagrams, and educational sequences.
- Use Reels for reach and personality.
- Use Stories for behind-the-scenes, polls, proof, and community signal.

Sources:

- https://creators.instagram.com/blog/rewarding-original-creators-on-instagram
- https://help.instagram.com/269314186824048/
- https://help.instagram.com/1631821640426723/

### YouTube

Current signal:

- YouTube is investing heavily in AI creation tools, Shorts remixing, auto-dubbing, AI-assisted creation, and AI labeling.
- YouTube's 2026 search/discovery direction is moving toward more conversational discovery and structured answers.
- AI-generated or significantly altered realistic content needs disclosure; YouTube is rolling out stronger automatic AI detection signals.
- YouTube still rewards packaging clarity: titles, descriptions, thumbnails, and viewer intent alignment matter.

Operating conclusion:

- Build every long-form idea with Shorts derivatives from day one.
- Treat YouTube as the highest-leverage trust engine: long-form proof, Shorts discovery, Community posts for relationship.
- Use AI for ideation, scripts, visual concepts, clips, translations/dubbing, and thumbnail variants, but keep creator POV and original framing.
- Store AI disclosure notes in the approval packet.

Sources:

- https://blog.youtube/inside-youtube/the-future-of-youtube-2026/
- https://blog.youtube/news-and-events/youtube-news-google-io-2026/
- https://blog.youtube/news-and-events/improving-ai-labels-viewers-creators/
- https://support.google.com/youtube/answer/12948449

### LinkedIn

Current signal:

- Document/carousel posts remain strong for educational B2B content.
- Recommended carousel dimensions are usually 1080x1080 or 1080x1350.
- PDF is the practical publishing format for LinkedIn document carousels.
- Professional clarity, strong first slide, mobile-safe text, captions, and proof matter.

Operating conclusion:

- Use LinkedIn carousels for systems architecture, prompt guides, setup walkthroughs, AI CoE frameworks, Codex/Claude/ChatGPT tutorials, and executive thought leadership.
- Use one idea per carousel.
- Build all carousels as reusable content atoms: LinkedIn PDF, Instagram carousel, blog/guide, YouTube script, and newsletter section.

Sources:

- https://www.heyorca.com/blog/linkedin-social-media-specs-best-practices-2026
- https://www.linkedin.com/pulse/linkedin-image-size-guide-2026-jan-van-musscher-wslwe

### OpenAI Image Generation

Current signal:

- GPT image models are suited for production-quality visuals, iterative design workflows, edits, and professional creative tasks.
- The recommended workflow is not "one prompt and publish"; it is prompt, generate, critique, edit, brand QA, export, approve.

Operating conclusion:

- Use image generation as the visual concept and asset engine.
- Use design QA before publishing: text legibility, brand consistency, factual accuracy, icon accuracy, spacing, platform crop, and public/private risk.
- For technical guide carousels, use AI for covers, diagrams, metaphors, backgrounds, and scene compositions; use deterministic tools for final text-heavy slides when exact typography matters.

Sources:

- https://developers.openai.com/api/docs/guides/image-generation
- https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide

## Content Pillars

### 1. Agentic Workflows

Examples:

- "How to set up Codex as your daily operating partner"
- "Claude Code vs Codex vs Hermes: who does what"
- "How to run Slack as an agent cockpit"
- "The guarded 24/7 agent OS"
- "What agents may do, what humans must approve"

Best formats:

- LinkedIn carousel
- YouTube explainer
- X/Threads thread
- Instagram carousel
- short-form video

### 2. AI Architecture

Examples:

- "Personal AI CoE architecture"
- "Agentic Organization OS"
- "Founder command center"
- "University/lab AI operating system"
- "Enterprise AI CoE workflow"

Best formats:

- LinkedIn carousel
- architecture diagram
- long-form YouTube
- downloadable PDF
- blog guide

### 3. Prompt And Setup Guides

Examples:

- "ChatGPT setup for founders"
- "Codex setup for repo automation"
- "Claude Code setup for agentic development"
- "How to create AGENTS.md"
- "How to design approval gates for AI teams"

Best formats:

- step-by-step carousel
- short tutorial video
- repo template
- newsletter
- lead magnet

### 4. Research And Mind Intelligence

Examples:

- "How to build a research intelligence OS"
- "How to turn papers into content"
- "How to label claims before posting"
- "The mind palace for AI-native work"

Best formats:

- source-backed carousel
- YouTube explainer
- newsletter essay
- Instagram carousel
- visual framework

### 5. Arcanea Creative IP

Examples:

- "How to build an AI-native creative universe"
- "Character/canon production workflow"
- "Visual intelligence loop"
- "Anime Legends launch map"

Best formats:

- Instagram/Reels
- YouTube Shorts
- visual carousel
- behind-the-scenes Stories
- community posts

## Canonical Production Pipeline

```text
Signal
  -> #research-intel or brand room
  -> content brief
  -> #content-film-prep
  -> visual plan / carousel storyboard
  -> image generation / diagram generation
  -> design QA
  -> platform variants
  -> #social-carousels for LinkedIn/Instagram carousel decks
  -> #social-command
  -> #social-* platform rooms
  -> #social-approvals
  -> publish / schedule
  -> proof + performance learning
```

## Asset Types To Produce

| Asset | Primary Channel | Reuse |
| --- | --- | --- |
| LinkedIn carousel PDF | LinkedIn | Instagram carousel, blog, newsletter |
| Instagram carousel | Instagram | LinkedIn cropped variant, Stories |
| YouTube thumbnail | YouTube | newsletter hero, X image |
| YouTube Shorts visual pack | YouTube Shorts | Reels, TikTok |
| Architecture diagram | LinkedIn, blog | webinar slide, PDF |
| Prompt guide visual | LinkedIn, Instagram | lead magnet, repo README |
| Social quote card | X, LinkedIn, Instagram | Stories |
| Proof screenshot | `#daily-report`, brand rooms | case study |

## LinkedIn Carousel Blueprint

Recommended dimensions:

- 1080x1350 for mobile-first portrait
- 1080x1080 for square systems diagrams
- export as PDF for LinkedIn document post

Slide structure:

1. Big promise / category name
2. Problem or old way
3. New mental model
4. Architecture or workflow
5. Step-by-step process
6. Tools / agents / channels
7. Approval or safety gate
8. Example output
9. Implementation checklist
10. CTA: comment, save, download, join, or watch

Quality bar:

- one idea per slide
- large readable text
- strong hierarchy
- mobile-safe margins
- no unverified claims
- source/proof note when factual
- final text QA outside image generator when exactness matters

## Image Generation Prompt Pattern

Use this structure:

```text
Create [asset type] for [platform] targeting [audience].
Topic: [single idea].
Visual metaphor: [system, map, cockpit, workflow, lab, studio].
Composition: [hero title, modules, arrows, proof/approval gate].
Style: [brand style, color palette, density, mood].
Constraints: no clutter, legible text only, no fake logos unless provided, no private data.
Output: [aspect ratio], [safe zone], [slide number if carousel].
```

Example:

```text
Create a LinkedIn carousel cover for AI founders.
Topic: Agentic Content OS.
Visual metaphor: command center workflow from idea to proof to publish.
Composition: Slack signals, Codex research, Hermes routing, image generation assets, social approvals, platform outputs.
Style: premium editorial-tech, dark neutral, cyan/green/amber accents, crisp system modules.
Constraints: only include title text "Agentic Content OS" and subtitle "From idea to proof to publish". No tiny labels.
Output: 4:5 portrait, mobile-safe.
```

## Recommended Weekly Rhythm

Monday:

- pick 3 flagship ideas
- assign brand lanes
- create briefs

Tuesday:

- produce carousels and video scripts
- generate visuals

Wednesday:

- record and edit
- create platform variants

Thursday:

- social approval batch
- schedule/publish approved content

Friday:

- proof, analytics, learning, and next hooks

Weekend:

- long-form essay/video, weekly digest, evergreen asset cleanup

## Workflow Automations To Add

### Content Idea Intake

Destination: `#work-queue` or `#research-intel`

Fields:

- idea
- brand
- source
- audience
- platform
- urgency
- proof/source
- suggested format

### Carousel Builder

Destination: `#social-carousels`

Fields:

- title
- audience
- slide count
- platform
- source
- CTA
- generated visual prompt
- design QA checklist
- deck path
- PDF path
- approval packet

### Visual QA Gate

Destination: `#design-intelligence`

Checks:

- text legibility
- brand consistency
- crop safety
- claim accuracy
- icon/logo accuracy
- AI artifacts
- public/private data risk

### Social Approval

Destination: `#social-approvals`

Fields:

- final text
- final media
- platform
- account/profile
- source/proof
- AI disclosure if needed
- proposed publish window
- risk

### Performance Learning

Destination: `#daily-report` and brand room

Fields:

- post link
- impressions/views
- saves
- comments
- watch time/retention
- clicks
- what worked
- next iteration

## Codex / Agent Responsibilities

| Agent/Profile | Role |
| --- | --- |
| `starlight` | route content into brand lanes and enforce proof/approval |
| `frankx` | authority posts, founder POV, audience hooks |
| `gencreator` | creator OS tutorials, templates, client/community packaging |
| `arcanea` | premium visuals, creative IP, visual intelligence |
| `mind` | source-backed research, claims, frameworks |
| `research` | citations, trend scans, market/source checks |
| `tooling` | Codex/Claude/ChatGPT setup guides, repo templates |
| Codex heartbeat | daily synthesis, content-to-film prep, execution queue |
| Image generation | covers, diagrams, visual metaphors, platform variants |

## Immediate Build List

1. Add `#content-film-prep` workflow form for film/carousel briefs.
2. Add `#social-approvals` form for final publish approval.
3. Add `#design-intelligence` visual QA template.
4. Create reusable carousel templates:
   - AI architecture overview
   - ChatGPT setup guide
   - Codex setup guide
   - Claude Code setup guide
   - Agentic Slack OS
   - Personal AI CoE
5. Use `#social-carousels` as the dedicated carousel production lane.
6. Create a weekly content calendar list if Slack plan supports lists.
7. Add daily Codex output section: "Image/Carousel Concepts".
8. Keep publishing manual until approval flow has passed at least one full loop.
