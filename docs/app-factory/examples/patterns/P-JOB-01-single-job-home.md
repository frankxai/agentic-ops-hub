# P-JOB-01 — Single-job home

- **ID:** P-JOB-01
- **Name:** Single-job home
- **Best for:** Micro-SaaS, creator tools, AaaS consoles
- **Anti-for:** Multi-role enterprise portals (use P-DASH-02)

## Problem

Users land in a wall of features and never complete the first job.

## Structure

```text
┌─────────────────────────────────────────┐
│ Brand · Search · Account                │
├─────────────────────────────────────────┤
│ H1: Do the job (outcome language)       │
│ Sub: one line when/outcome              │
│ [ Primary CTA ]   secondary link        │
├─────────────────────────────────────────┤
│ Recent results (3) OR empty→CTA         │
│ Trust strip (optional, quiet)           │
└─────────────────────────────────────────┘
```

## Must include

- Outcome-named H1  
- One primary CTA  
- Empty state that starts the job  

## Must avoid

- Feature bento  
- Fake activity feeds  
- Multiple equal CTAs  

## Components

- shadcn: button, card, input, sonner  
- lucide: one metaphor icon max near H1  

## States

- empty: CTA  
- loading: skeleton on recent  
- error: banner + retry  

## A11y

- H1 single; CTA focusable; no icon-only primary  
