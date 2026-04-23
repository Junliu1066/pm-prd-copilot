---
name: source-collector
description: Normalize rough product inputs, notes, PDFs, meeting records, screenshots, and external source snippets into a traceable source brief for PRD work. Use when a PM request is still raw, mixed with assumptions, or needs source boundaries before user analysis, competitor analysis, MVP scoping, or PRD drafting.
---

# Source Collector

## Overview

Turn messy inputs into a small, traceable requirement brief. Preserve what the user actually said, separate inference from evidence, and mark missing information instead of inventing it.

## Workflow

1. Inventory all available inputs: user statements, uploaded files, prior project artifacts, external links, screenshots, and known constraints.
2. Classify each point as `explicit`, `inferred`, `external_signal`, or `missing`.
3. Normalize the product intent into problem, target surface, platform, user value, business value, constraints, open questions, and source notes.
4. Preserve source traceability. If evidence comes from a file, link the file and section when possible. If evidence comes from web or MCP output, mark it as unverified external signal.
5. Do not decide MVP scope, target user priority, or PRD modules. Hand those to downstream skills.

## Output Contract

Read [references/output-contract.md](references/output-contract.md) when writing a formal artifact. The output should include:

- `source_summary`
- `explicit_requirements`
- `inferred_requirements`
- `constraints`
- `unknowns`
- `source_trace`

## Guardrails

- Never treat external data as verified truth; remind the user to verify.
- Do not overwrite user intent with competitor or model assumptions.
- Keep the brief compact enough for downstream skills to consume without repeated raw-context loading.
