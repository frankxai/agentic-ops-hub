# P-CHAT-01 — Agent sidekick

- **ID:** P-CHAT-01
- **Name:** Agent sidekick
- **Best for:** AaaS products where work is a canvas
- **Anti-for:** Pure chatbots (different product)

## Problem

Full-screen chat hides the artifact and trains users to ramble instead of finish work.

## Structure

```text
┌──────────────────────────┬──────────────┐
│ Work canvas / job UI     │ Agent panel  │
│ (source of truth)        │ messages     │
│                          │ tool cards   │
│                          │ confirmations│
└──────────────────────────┴──────────────┘
Mobile: canvas first; agent as sheet
```

## Must include

- Canvas owns the object  
- Tool receipts under turns  
- Confirm for irreversible tools  

## Must avoid

- Chat as only surface  
- Hidden side effects  
- Auto-run delete/pay/publish  

## Components

- shadcn: sheet, scroll-area, badge, button  
- optional assistant-ui primitives if already justified  

## States

- agent thinking (non-blocking)  
- tool pending confirm  
- tool failed with retry  
