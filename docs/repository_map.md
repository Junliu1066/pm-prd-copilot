# Repository Map

This repository is organized around one principle:

```text
stable framework and reusable skills stay outside projects;
project-specific inputs, drafts, prototypes, runs, and closeout records stay inside projects/<project>/.
```

## Canonical Areas

| Path | Role | Keep Long Term | Notes |
| --- | --- | --- | --- |
| `pm-prd-copilot/` | Stable PM Copilot skill, templates, scripts, memory, UI design layer, proposals | Yes | Main product framework. Do not store project-specific outputs here except supervised proposals. |
| `plugins/` | Detachable plugin suites and plugin-owned skills | Yes | Plugin bundles should be removable through registry changes. |
| `registry/` | Canonical registry for artifacts, skills, plugins, MCPs, and stewards | Yes | Use this to understand what the system officially knows. |
| `workflow/` | Workflow stages, actions, and approval policies | Yes | Describes the governed PM pipeline. |
| `governance/` | Steward policies, scaling rules, audits, teaching policy | Yes | Rules for safe operation and escalation. |
| `harness/` | Governance and quality checkers | Yes | Validation layer for registry, workflows, proposals, source traces, and project gates. |
| `shared/schemas/` | Shared JSON schemas | Yes | Contracts reused by pipeline outputs and checks. |
| `stewards/` | Active steward operating protocols | Yes | Responsibility definitions for sub-stewards. |
| `teaching/` | User teaching, open lessons, accepted lessons, preferences | Yes | Human-supervised learning record. |
| `ai-intel/` | AI source tracking, events, decision docs, and reports | Yes | Separate from PM project generation. |
| `evals/` | Cross-project evals and real-output evaluation reports | Yes | Used to prevent regressions and overfitting. |
| `docs/error_reports/` | Process error logs, overnight test reports, and bug index | Conditional | Record failures and bug candidates; do not store secrets. |
| `memory-cache/` | Project-scoped preference caches | Conditional | Never read across projects; clear only after supervised closeout. |
| `projects/` | Project inputs, generated artifacts, final edits, runs, prototypes, closeout packages | Conditional | Treat as project workspaces. Archive or clean through closeout, not ad hoc deletion. |
| `.agents/` | Local Codex plugin marketplace metadata | Yes | Tooling metadata. |
| `.github/` | GitHub workflows | Yes | Automation entry points. |

## Root File Policy

The root should stay small. Keep only:

- `README.md`
- `requirements.txt`
- `.gitignore`
- `.github/`
- `.agents/`
- high-level operator docs such as `agent.md`

Root-level historical docs and zip packages are allowed temporarily, but they should eventually move to an archive or canonical folder after review.

## Product Pipeline

Typical project flow:

```text
projects/<project>/00_raw_input.md
 -> requirement brief
 -> PRD
 -> user stories
 -> risk check
 -> tracking plan
 -> prototype / UI style direction
 -> harness runs
 -> closeout report
 -> architecture feedback draft
 -> supervised cleanup
```

Canonical commands:

```bash
python3 pm-prd-copilot/scripts/router.py --base-dir . init-project --project demo-project --title "..."
python3 pm-prd-copilot/scripts/run_pipeline.py --base-dir . --project demo-project --stage all --mode rule
python3 pm-prd-copilot/scripts/router.py --base-dir . ui-style --project demo-project
python3 pm-prd-copilot/scripts/router.py --base-dir . closeout --project demo-project
python3 pm-prd-copilot/scripts/run_regression.py --base-dir . --strict
python3 harness/run_harness.py --base-dir . --project demo-project --mode advisory --check-only
```

## UI Design Layer

UI design support lives in:

```text
pm-prd-copilot/ui-design/
```

It contains:

- `data/visual_style_catalog.json`: supervised style catalog, including concrete/cement, Swiss utility, refined SaaS, brutalist, glass depth, AI lab dark, editorial, Bauhaus, minimal luxury, warm humanist, retro terminal, neo clay, and data newsroom.
- `prompts/ui_style_selector.md`: style selection prompt.
- `prompts/ui_quality_reviewer.md`: visual QA prompt.

Style direction outputs belong in:

```text
projects/<project>/prototype/ui_style_direction.md
projects/<project>/prototype/ui_style_direction.json
```

## Closeout Layer

Project closeout support lives in:

```text
pm-prd-copilot/scripts/closeout_project.py
```

Closeout outputs belong in:

```text
projects/<project>/closeout/
```

The closeout command is report-only. It must not delete, move, commit, push, or merge anything.
Project lifecycle states are defined in `docs/project_lifecycle.md`.

## Rules For Future Cleanup

- Do not clean by filename alone.
- Use `projects/<project>/closeout/manifest.json` as the review inventory.
- Keep final human-edited artifacts until lessons are distilled.
- Keep raw inputs under explicit human supervision because they may include sensitive project context.
- Keep project preference caches separate from reusable skill memory.
- Do not promote a project-specific UI style, market default, label, or workflow into stable skills without human approval.
- Archive before deletion. Archived items are only eligible for hard deletion after 30 days and still require an exact user-approved delete list.
