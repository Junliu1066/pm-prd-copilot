---
name: development-governance-orchestrator
description: Build the operating-system layer for semi-automated development by integrating stewardship, audit, efficiency review, teaching absorption, preference memory, skill update proposals, harness checks, and human supervision. Use only when Codex-style development explicitly needs a scalable manager system rather than a single coding task list.
---

# Development Governance Orchestrator

## Purpose

Turn an approved manager system into a development operating system. This skill answers "who governs the work, who audits it, who learns from feedback, and what blocks unsafe automation?" It should not expand an ordinary Codex development document into full governance mechanics by default.

## Inputs

- capability enablement plan
- skill/MCP routing plan
- delivery and AI plans
- registry, steward policy, teaching policy, and harness policy

## Workflow

1. Confirm the user or approved plan requested full governance orchestration. If not, return a lightweight governance note instead of a full operating-system plan.
2. Define chief steward and sub-steward responsibilities only for the requested governance scope.
3. Add random-audit, efficiency, and teaching roles when they reduce concrete delivery risk.
4. Define how project preference memory and generic skill learning are separated.
5. Define required harness checks before and after coding, reusing existing checks first.
6. Define escalation when steward capacity is exceeded.
7. Define feedback absorption: project cache, open lesson, accepted lesson, skill proposal, harness proposal, or no persistent learning.

## Output Contract

Read [references/output-contract.md](references/output-contract.md). In full governance mode, include `chief_steward`, `sub_stewards`, `random_audit`, `efficiency_audit`, `teacher`, `preference_cache`, `skill_update_proposal`, `harness`, and `escalation`. In lightweight mode, include only the governance notes, human approvals, validation, and escalation points needed for the current implementation.

## Guardrails

- The teacher proposes learning; it does not directly update skills.
- The efficiency role proposes optimization; it does not lower quality thresholds.
- The random auditor reports findings; it does not modify artifacts.
- Human approval is required for new stewards, skill updates, MCP integrations, destructive actions, and Git operations.
