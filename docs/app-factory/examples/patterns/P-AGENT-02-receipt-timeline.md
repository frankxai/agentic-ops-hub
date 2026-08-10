# P-AGENT-02 — Receipt timeline

- **ID:** P-AGENT-02
- **Name:** Receipt timeline
- **Best for:** Any AaaS / generative side effects
- **Anti-for:** Read-only content sites

## Problem

Users do not trust agents they cannot audit.

## Structure

```text
Timeline (newest first)
· 12:04 Generated draft → View
· 12:05 Proposed publish → [Confirm] [Dismiss]
· 12:06 Published URL → Open · Undo window
```

## Must include

- Timestamp  
- Human label of action  
- Link to artifact  
- Status chip  

## Must avoid

- Raw JSON as UI  
- Silent successes  

## Components

- shadcn: badge, button, separator  
