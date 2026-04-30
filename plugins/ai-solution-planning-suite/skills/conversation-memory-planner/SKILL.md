---
name: conversation-memory-planner
description: Plan AI conversation memory and data retention boundaries, including session cache, long-term profile, user-controlled clearing, sensitive data handling, and cross-session personalization. Use when an AI product needs to remember context or user progress.
---

# Conversation Memory Planner

## Purpose

Design what the AI remembers, for how long, why, and how the user can inspect or clear it.

## Workflow

1. Separate memory into short-term session context, project-level state, long-term user preference, and capability profile.
2. Define retention, deletion, consent, sensitivity, and access rules.
3. Define what must never be stored long-term by default.
4. Define cache invalidation and memory update triggers.
5. Hand user ability signals to `learner-profile-modeler`.

## Output Contract

Read [references/output-contract.md](references/output-contract.md). Always include `memory_layers`, `retention_policy`, `clear_controls`, `sensitive_data_rules`, and `profile_update_triggers`.

## Guardrails

- Do not store secrets, credentials, or sensitive personal data.
- Do not make long-term memory implicit; user consent and clear controls are required.
- Do not mix memories between projects or users.
