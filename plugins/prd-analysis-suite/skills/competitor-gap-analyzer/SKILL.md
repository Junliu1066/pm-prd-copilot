---
name: competitor-gap-analyzer
description: Analyze competitor products, user complaints, feature patterns, positioning, and opportunity gaps from sourced evidence. Use when PRD work needs market context, product differentiation, competitor comparison, app-store review synthesis, or evidence-backed advantage discovery before scenario ranking or MVP scoping.
---

# Competitor Gap Analyzer

## Overview

Turn competitor research into product judgment. The purpose is not to list features; it is to explain how competitors solve the problem, where users still struggle, and how our product can amplify a practical advantage.

## Workflow

1. Identify direct competitors, adjacent alternatives, manual workarounds, and platform-native substitutes.
2. For each competitor, capture target user, core loop, key features, pricing or monetization signal, onboarding burden, and review complaints.
3. Separate sourced facts from assumptions. External data is unverified until the user checks it.
4. Extract patterns: what everyone offers, what users complain about, what is expensive to build, and what is easy to differentiate.
5. Convert each meaningful gap into an advantage hypothesis and explain how the product can amplify that advantage.
6. Translate gaps into opportunity areas tied to user needs and scenarios.
7. Provide a verification checklist for the user before any market claim is treated as true.

## Accepted Teaching Rules

- `LESSON-20260423-003`: Competitor analysis must explain competitor approach, gap, opportunity, advantage, and amplification strategy. A plain feature table is insufficient.

## Evidence Standard

- Record source name, URL or file path, collection date, and confidence.
- Prefer primary surfaces when available: official product pages, app listings, changelogs, pricing pages, support docs, and app reviews.
- Mark blogs, rankings, AI summaries, and MCP outputs as secondary signals.
- Remind the user to verify source date, product version, region, pricing, and feature availability.

## Output Contract

Read [references/output-contract.md](references/output-contract.md) for the formal artifact shape. Always include:

- `competitor_map`
- `common_solution_patterns`
- `user_complaint_themes`
- `opportunity_gaps`
- `advantage_hypotheses`
- `advantage_amplification_plan`
- `verification_checklist`

## Guardrails

- Do not present unverified external data as truth.
- Do not stop at a feature comparison table.
- Do not recommend copying a competitor feature without explaining user value and cost.
- Do not decide MVP scope; provide inputs for ranking and scoping.
