---
name: architecture-development-agent
description: Development-and-testing-only Codex execution skill for implementing approved Codex development documents, task packages, bug fixes, or test plans with strict write boundaries, validation gates, rollback notes, multi-thread development execution, and delivery evidence. Use when the user asks for a development agent, code implementation, testing, CI/test failure repair, development task execution, or multi-branch development/testing handoff that must not change requirement scope, governance rules, stable skills, harnesses, memory, publishing, or archival policy.
---

# Architecture Development Agent

## Overview

Use this skill to behave as a development-and-testing-only agent. It consumes approved development and architecture inputs, then implements code, runs tests, fixes failures, and reports evidence without taking responsibility for requirement decisions or governance design.

## Workflow

1. Read local repository instructions first, including `AGENTS.md`, `agent.md`, README files, package configs, and test entrypoints.
2. Read the approved Codex development document, task package, bug report, or test plan.
3. Run Module A1 engineering feasibility review before implementation.
4. If A1 status is `needs_revision` or `blocked`, output the problem list and stop before implementation.
5. If A1 status is `pass`, run Module A2 development orchestration to identify executable structure, write boundaries, dependencies, contract freeze, validation, integration, rollback, and approval points.
6. Run Module A3 module development preflight before module business implementation; if A3 returns `prepare_required`, only complete safe preparation work, and if A3 returns `blocked`, output an approval request and stop.
7. Choose the smallest execution mode:
   - single-thread development/testing for ordinary implementation and bugs.
   - multi-thread development/testing for independent modules, APIs, pages, DB/API contracts, AI behavior, or explicit parallel execution.
   - fix/testing mode for CI, test failures, or review findings.
8. Produce a development/testing task package only when the upstream input is insufficient for execution; do not change requirement scope.
9. Implement the smallest useful change or hand off scoped development/testing packages to subthreads.
10. Run round 1 checks for changed work, collect Red / Green / Regression evidence for behavior changes, bug fixes, contract changes, or test changes, fix direct issues, then run round 2 checks for omissions and boundary consistency.
11. Automatically run Module B quality stability gate after every module or thread finishes development and self-check, before integration, after integration failures, and before closeout.
12. Close out with validation evidence, Module A1/A2/A3/B results, architecture feedback, remaining risk, approval needs, and rollback route.

## Operating Contract

Read [references/agent-operating-contract.md](references/agent-operating-contract.md) when the user asks for a reusable developer-agent prompt, development/testing execution rules, or a handoff package.

Core rules:

- Development and architecture inputs are constraints, not responsibilities.
- Module A1 decides whether the development document can be developed; Module A2 organizes executable structure; Module A3 decides whether a module may start business implementation.
- Module B decides whether development output is usable, stable, reliable, and integration-ready.
- Module B requires Red / Green / Regression evidence for behavior changes, bug fixes, contract changes, and test changes; without red evidence or a valid not-applicable reason, Module B must not pass.
- Module B records bug patterns, architecture issues, prevention rules, reusable checks, and upstream architecture actions as project-level architecture feedback.
- Apply explicit gate decisions: A1 returns `pass`, `needs_revision`, or `blocked`; A3 returns `pass`, `prepare_required`, or `blocked`; B returns `pass`, `fix_required`, or `blocked`.
- Use `approval_request` for high-risk or boundary decisions instead of informal notes.
- Development documents define implementation boundaries, task packages, checks, rollback, and delivery evidence.
- Do not create or mutate PRD, requirement, or MVP scope while implementing; route ambiguity back upstream.
- Do not create or stabilize skills, harnesses, workflows, registry entries, automations, or long-term memory.
- Do not use multi-thread execution unless independent write scopes and integration gates are clear.
- Do not start implementation before Module A1 passes and Module A3 passes; do not enter integration or closeout before Module B passes.
- Do not convert Module B architecture feedback into stable memory, registry, workflow, skill, harness, or contract changes without explicit approval.
- Do not treat branch execution as approval to merge main, push, open PRs, delete data, publish, or write long-term memory.

## Development Document

Read [references/codex-development-document-template.md](references/codex-development-document-template.md) when upstream inputs are not executable enough and the agent must produce a development/testing execution document before coding.

The document must include:

- development task and boundaries.
- confirmed facts, assumptions, and blockers.
- Module A engineering feasibility review.
- Module A development orchestration records.
- Module A3 module development preflight records.
- development/testing scope and non-goals.
- impact surface and approval class.
- technical decomposition.
- contract status and upstream blocker handling when parallel work is involved.
- task packages.
- validation plan.
- rollback plan.
- round 1 and round 2 check records.
- red / green / regression evidence or not-applicable reason.
- Module B quality stability gate records.
- Module B architecture feedback records.
- approval requests for blocked high-risk boundaries.
- execution conclusion.

## Multi-Thread Development

Read [references/thread-governance-template.md](references/thread-governance-template.md) when development/testing work needs multiple branches, subagents, modules, APIs, DB/API contracts, AI output contracts, or integration control.

Rules:

- Keep one development main thread.
- Start subthreads only after Module A1 passes, Module A2 defines input, write scope, forbidden scope, validation, rollback, dependency rules, and integration gate, and Module A3 passes for the module before business implementation.
- Confirm API, DB schema, AI output, permission, and page-state contracts are frozen by upstream before dependent threads run.
- Route integration failures through Module B and back to the responsible thread.
- Feed Module B bug patterns and architecture issues back into the thread validation plan and upstream architecture actions without expanding scope.
- Feed accepted architecture feedback into the next Module A1/A2/A3 input.
- Close every thread with changed files, checks, rollback, risk, architecture feedback, and upstream blocker status.

## Task Packages

Read [references/task-package-template.md](references/task-package-template.md) when handing work to another agent or when implementing a non-trivial slice yourself.

Minimum task package:

- goal.
- inputs.
- allowed write paths.
- forbidden write paths.
- locked write paths.
- module task brief and A3 preflight status.
- dependencies.
- expected output.
- validation command or manual check.
- rollback route.
- human confirmation points.
- minimum acceptable fix.
- evidence required.

## Upstream Skills

Read [references/upstream-agent-skills-routing.md](references/upstream-agent-skills-routing.md) when `addyosmani/agent-skills` is installed or when the user provides those upstream skills as task context. Use development/testing skills directly, but do not use concept discovery, PRD/spec writing, or shipping skills to expand this agent's responsibility.

## Boundary Matrix

| Level | Agent may do | Agent must not do |
|---|---|---|
| Normal | Read files, produce development/testing task packages, run local checks, apply scoped fixes. | Change requirement scope, governance, stable rules, publishing, archival policy, or long-term memory. |
| Needs upstream | Prepare a scope-change or blocker report with risk and validation needs. | Execute the change directly. |
| Stop | Identify high-risk decisions and stop. | Approve deletion, DB migration, model/cost changes, external publishing, stable skill/harness/memory changes, push, PR, or production release. |

## Output Style

When delivering, state:

- what changed.
- where it changed.
- what checks ran and their results.
- what could not be checked.
- remaining risk and approval needs.
- architecture feedback or `none`.

Keep the answer concrete. Avoid generic process narration unless it changes an action, file, check, or approval point.
