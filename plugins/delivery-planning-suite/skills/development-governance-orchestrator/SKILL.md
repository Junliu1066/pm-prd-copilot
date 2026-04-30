---
name: development-governance-orchestrator
description: Build the operating-system layer for semi-automated development by integrating chief and sub-stewards, random audit, efficiency review, teaching absorption, preference memory, skill update proposals, harness checks, and human supervision. Use when Codex-style development must be governed as a scalable manager system rather than a single coding task list.
---

# Development Governance Orchestrator

## Purpose

Turn the manager system into a development operating system. This skill answers "who governs the work, who audits it, who learns from feedback, and what blocks unsafe automation?"

## Inputs

- capability enablement plan
- skill/MCP routing plan
- delivery and AI plans
- registry, steward policy, teaching policy, and harness policy

## Workflow

1. Define chief steward and sub-steward responsibilities.
2. Add random-audit, efficiency, and teaching roles to the development flow.
3. Define how project preference memory and generic skill learning are separated.
4. Define required harness checks before and after coding.
5. Define escalation when steward capacity is exceeded.
6. Define feedback absorption: project cache, open lesson, accepted lesson, skill proposal, or harness proposal.

## Output Contract

Read [references/output-contract.md](references/output-contract.md). Always include `chief_steward`, `sub_stewards`, `random_audit`, `efficiency_audit`, `teacher`, `preference_cache`, `skill_update_proposal`, `harness`, and `escalation`.

## Guardrails

- The teacher proposes learning; it does not directly update skills.
- The efficiency role proposes optimization; it does not lower quality thresholds.
- The random auditor reports findings; it does not modify artifacts.
- Human approval is required for new stewards, skill updates, MCP integrations, destructive actions, and Git operations.
