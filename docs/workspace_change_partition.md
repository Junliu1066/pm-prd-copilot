# Workspace Change Partition

- Date: 2026-04-29
- Snapshot command: `git status --short`
- Snapshot size: 147 status entries
- Status mix: `67 M`, `4 D`, `76 ??`
- Purpose: make the mixed workspace reviewable before cleanup, archive, staging, or further architecture work.
- Rule: this file is an audit map only. It does not approve cleanup, deletion, move, archive, staging, commit, push, PR creation, plugin promotion, skill promotion, harness promotion, or stable architecture acceptance.

## Root Distribution

| Root | Status entries |
|---|---:|
| `.agents` | 1 |
| `.github` | 2 |
| `AGENTS.md` | 1 |
| `README.md` | 1 |
| `agent.md` | 1 |
| `ai-intel` | 9 |
| `docs` | 16 |
| `evals` | 1 |
| `governance` | 2 |
| `harness` | 15 |
| `memory-cache` | 1 |
| `plugins` | 5 |
| `pm-prd-copilot` | 26 |
| `prd_pm_2026_playbook.md` | 1 |
| `prd_skill_kit_2026.zip` | 1 |
| `prd_template_2026.md` | 1 |
| `projects` | 43 |
| `registry` | 4 |
| `shared` | 1 |
| `skill_suite_overview.md` | 1 |
| `stewards` | 7 |
| `teaching` | 4 |
| `workflow` | 3 |

## Partition Summary

| Partition | Count | Status mix | Default audit action | Treatment |
|---|---:|---|---|---|
| stable-framework | 48 | modified / untracked | `keep_in_architecture` | Architecture candidate set. Review and validate as framework work; do not stage together with project artifacts. |
| project-artifacts | 44 | modified / untracked | `keep_as_project_artifact` | Project outputs, runs, prototypes, archives, and caches. Keep separate; use project closeout before cleanup. |
| docs-governance-teaching | 19 | modified / untracked | `keep_in_architecture` | Governance docs and teaching records. Review for current wording, but keep in documentation layer. |
| harness-eval | 10 | untracked | `needs_user_decision` | Existing validation/eval expansion. Must pass “no unnecessary harness” review before stabilization. |
| automation-ai-intel | 9 | modified / untracked | `needs_user_decision` | AI intel and automation-supporting records. Keep separate from PM core until automation review is complete. |
| steward-protocols | 7 | untracked | `keep_in_architecture` | Protocol docs for existing stewards; these are not new stewards. Review wording, then keep with governance docs. |
| archive-root-cleanup | 5 | deleted / untracked | `archive_candidate` | Root historical files and archive folder. Archive first; hard delete only after 30 days and exact approval. |
| unconfirmed-new-capabilities | 5 | untracked | `needs_user_decision` | New plugin suites. Must prove necessity and removability before becoming stable architecture. |

## Audit Action Table

| Audit action | Meaning | Current items |
|---|---|---|
| `keep_in_architecture` | Candidate stable architecture or governance asset. Keep, but validate and stage separately if later approved. | stable framework files, governance docs, teaching records, steward protocol docs |
| `keep_as_project_artifact` | Project-local evidence, generated output, prototype, run state, or cache. Do not mix into architecture commits. | `projects/*`, `memory-cache/` |
| `archive_candidate` | Candidate to move into an archive location after exact approval. | root historical PRD files, root zip, root overview, `docs/archive/` |
| `delete_after_30_days_candidate` | Only after archive, lesson extraction, retention window, and exact user approval. | none approved in this snapshot |
| `needs_user_decision` | Cannot be classified as stable until the user reviews necessity, ownership, and replacement path. | new plugin suites, untracked harness/eval expansion, AI intel records |
| `do_not_touch` | Protected roots or sensitive runtime inputs. No cleanup without explicit per-path approval. | `.env`, stable framework roots, closeout audit records, raw inputs, final human edits |

## Stable Framework Bucket

Includes:

- `.agents/`, `.github/`
- `README.md`, `agent.md`, `AGENTS.md`
- `pm-prd-copilot/`
- `workflow/`, `registry/`, `governance/`, `shared/`
- modified existing `harness/` files

Current role: architecture repair set. It includes PRD generator repairs, pipeline default-governed repairs, workflow/action/artifact contract repairs, harness check-only/write-report repairs, docs references, and policy updates.

Handling rule: keep as a separate future review/staging unit. Do not mix with `projects/*`, archive candidates, or generated reports.

## Project Artifacts Bucket

Includes:

- `projects/demo-project/` generated artifacts and `pipeline-latest` run files.
- `projects/fitness-app-mvp/` analysis and run files.
- untracked project folders including `_archives`, `ai-collaboration-efficiency-platform`, `graduation-defense-agent`, `jiaxiaoqian-ai-invest-research`, `prompt-optimization-workbench`, `santoip-ai-brand-video`, and `taxi-hailing-prd-test`.
- `memory-cache/`.

Current role: project evidence and regression fixtures. `demo-project` is currently used by regression/harness; `taxi-hailing-prd-test/02_prd.final.md` is the PRD structure golden sample.

Handling rule: keep as project artifacts. Run closeout before any archive or cleanup. Do not treat project generated files as stable framework changes.

## Project Closeout Scan Index

本索引是归档前扫描结果，不代表项目已归档，也不批准删除、移动、清空偏好缓存或写入长期记忆。`projects/_archives` 是归档区，本轮不当作 active 项目扫描。

| Project | Current judgment | Evidence / role | Final human version | Prototype / UI / development / AI / B package | Preference cache | Architecture feedback | Cleanup candidates | User decision needed |
|---|---|---|---|---|---|---|---|---|
| `demo-project` | active test fixture | Regression and governance fixture with latest pipeline run. | Yes: final PRD and final user stories. | Prototype PNGs and UI style direction exist; no AI/B package. | No | Yes, 19 checklist items. | Yes: 5 generated metadata cleanup candidates after archive/review. | Keep as regression fixture by default; do not archive unless a replacement fixture exists. |
| `fitness-app-mvp` | active / closeout candidate | Real project evidence with analysis, prototype preview, and preference cache. | Yes: final PRD and final user stories. | Product flow and prototype preview exist; no B package detected. | Yes, 5 project-memory files require review. | Yes, 14 checklist items. | Yes: 5 generated metadata cleanup candidates after archive/review. | Decide whether project is still active; review project preference cache before any archive. |
| `taxi-hailing-prd-test` | closeout candidate | 0-1 PRD quality sample; generated draft exposed PRD regression issues. | Yes: final PRD. | PRD final includes page specs, navigation, and prototype layer; no PNG/HTML/UI. | No | Yes, 26 checklist items; generic architecture inbox already created separately. | Yes: 2 cleanup candidates after archive/review. | Decide whether final PRD becomes a golden sample; keep project name as evidence only, not rule title. |
| `ai-collaboration-efficiency-platform` | closeout candidate | Sparse historical PRD artifact, no run evidence. | No final marker detected. | Single PRD file only; no prototype/UI/development package detected. | No | Yes, 7 checklist items. | No automatic cleanup candidates; 1 manual-review file. | Decide whether to keep as historical PRD evidence or archive candidate after review. |
| `graduation-defense-agent` | closeout candidate | AI solution, delivery planning, Codex development, and prototype outputs exist. | No final marker detected. | AI plan, delivery docs, Codex development docs, and prototypes exist. | No | Yes, 7 checklist items. | No direct delete candidates; 53 files require archive/distillation before cleanup. | Review complete package and decide active vs archive candidate. |
| `jiaxiaoqian-ai-invest-research` | active | AI-heavy project with PRD, development docs, B package, prototype, governance notes, and zips. | No final marker detected. | Prototype HTML/screenshots, development docs, B docs, AI model selection, and zip packages exist. | No | Yes, 13 checklist items. | 9 archive/distillation candidates and 25 manual-review files. | Keep active by default; old PRD wording is history-sweep candidate, not cleanup approval. |
| `prompt-optimization-workbench` | closeout candidate | HTML prototype package evidence. | No final marker detected. | Prototype HTML source and zip package exist. | No | Yes, 7 checklist items. | 11 archive/distillation candidates and 1 manual-review file. | Decide whether prototype package should be archived after review. |
| `santoip-ai-brand-video` | closeout candidate | HTML prototype package evidence. | No final marker detected. | Prototype HTML source and zip package exist. | No | Yes, 7 checklist items. | 11 archive/distillation candidates and 1 manual-review file. | Decide whether prototype package should be archived after review. |

Closeout scan rules:

- Closeout reports are review materials only.
- Do not move projects into `projects/_archives` in this pass.
- Do not delete project files or generated runs in this pass.
- Do not clear project preference cache without user review.
- Do not promote project feedback into long-term memory, templates, prompt rules, skill behavior, harness checks, workflow, or registry without a separate approved plan.
- If project status is uncertain, treat it as active or closeout candidate, never as delete-ready.

## Unconfirmed Capability Bucket

Includes:

- `plugins/ai-solution-planning-suite/`
- `plugins/delivery-planning-suite/`
- `plugins/prd-prototype-suite/`
- `plugins/preference-memory-suite/`
- `plugins/quality-evaluation-suite/`
- untracked harness/eval files under `harness/` and `evals/`

Current role: capability expansion candidates already present in the workspace.

Handling rule: no new Skill, harness, plugin, or long-term rule should be accepted by default. Before stabilizing, each item needs a short review: what problem it solves, which existing component could have covered it, whether it is removable, and which tests prove value.

## Archive / Cleanup Bucket

Current archive-root-cleanup items:

| Item | Status | Default action | Notes |
|---|---|---|---|
| `prd_pm_2026_playbook.md` | deleted from root | `archive_candidate` | Canonical copy appears under `pm-prd-copilot/references/`; verify archived copy before accepting deletion. |
| `prd_template_2026.md` | deleted from root | `archive_candidate` | Canonical template appears under `pm-prd-copilot/templates/`; verify archived copy before accepting deletion. |
| `prd_skill_kit_2026.zip` | deleted from root | `archive_candidate` | Binary package should not live at root; archive or external backup only after review. |
| `skill_suite_overview.md` | deleted from root | `archive_candidate` | Merge useful content into `docs/repository_map.md` or archive. |
| `docs/archive/` | untracked | `archive_candidate` | Review archive contents before treating root deletions as safe. |

Root deletion approval details:

| Item | root_status | canonical_copy | archive_copy | recommended_action | delete_after_30_days_candidate | needs_user_approval | notes |
|---|---|---|---|---|---|---|---|
| `prd_pm_2026_playbook.md` | deleted from root | `pm-prd-copilot/references/prd_pm_2026_playbook.md` | `docs/archive/root-files/prd_pm_2026_playbook.md` | Keep canonical and archive copies; accept root deletion only after user review. | No, unless later archive policy approves root historical record cleanup. | Yes | Root copy is redundant if canonical and archive are accepted. Do not restore by default. |
| `prd_template_2026.md` | deleted from root | `pm-prd-copilot/templates/prd_template_2026.md` | `docs/archive/root-files/prd_template_2026.md` | Keep canonical and archive copies; accept root deletion only after user review. | No, unless later archive policy approves root historical record cleanup. | Yes | Root copy is redundant if canonical and archive are accepted. Do not restore by default. |
| `prd_skill_kit_2026.zip` | deleted from root | none stable | `docs/archive/root-files/prd_skill_kit_2026.zip` | Keep archive copy only; do not return binary package to repository root. | Yes, after archive retention window and exact approval. | Yes | Binary package should stay out of root. Confirm whether an external backup is needed before any hard delete. |
| `skill_suite_overview.md` | deleted from root | none stable | `docs/archive/root-files/skill_suite_overview.md` | Keep archive copy; later decide whether useful content should be extracted into `docs/repository_map.md`. | Yes, after archive retention window and exact approval. | Yes | Do not merge into repository map in this pass; review content first. |

Current pass explicitly does not:

- restore root files
- delete archive copies
- move archive directories
- put `prd_skill_kit_2026.zip` back in root
- merge `skill_suite_overview.md` into `docs/repository_map.md`
- stage, commit, push, or create a PR

Handling rule: archive first. Do not hard-delete during this pass. Hard delete eligibility starts only after 30 days and exact user approval.

## Historical PRD Old-Wording Risks

These are recorded for a later history sweep only. Do not batch-fix them in this workspace收口 pass.

| File | Old wording found | Current classification | Next action |
|---|---|---|---|
| `projects/taxi-hailing-prd-test/02_prd.generated.md` | `PRD 可视化层`, `原型图 / 线框图`, default `AI 模型选型` | `keep_as_project_artifact` | Historical generated draft. Keep final golden sample as source of truth; do not repair now. |
| `projects/taxi-hailing-prd-test/02_prd.generated.json` | default non-AI `AI 模型选型` text | `keep_as_project_artifact` | Historical generated JSON. Do not mix into generator repair. |
| `projects/jiaxiaoqian-ai-invest-research/01_prd.md` | `原型图 / 线框图`, `AI 模型选型` | `history_sweep_candidate` | AI selection may be valid because the product is AI-heavy; only the old prototype wording needs contextual review. |
| `projects/jiaxiaoqian-ai-invest-research/11_visual_prd_preview.md` | references old placement before `原型图 / 线框图` | `history_sweep_candidate` | Review when updating this project’s PRD visuals. |
| `projects/jiaxiaoqian-ai-invest-research/02_development_design.md`, `03_mvp_release_plan.md`, `10_开发文档.md`, `10_开发文档_review.md` | old “流程图、原型图、AI 模型选型” input wording | `history_sweep_candidate` | Treat as historical project delivery docs, not stable templates. |
| `projects/ai-collaboration-efficiency-platform/AI协作效率平台_PRD_完整测试版_v1.0.md` | `页面级原型图 / 线框图` | `history_sweep_candidate` | Historical project PRD; review only if project is reactivated. |

Non-risk mentions:

- `pm-prd-copilot/templates/prd_template_2026.md` still contains conditional `AI 模型选型（涉及 AI 能力时必备）`; this is intentional.
- `docs/proposals/prd_structure_change_impact_review.md` mentions old wording as a recorded issue; this is not a live template defect.

## Current Policy

- Do not clean by filename alone.
- Do not mix project-generated artifacts into stable framework commits.
- Do not accept new plugins, harness checks, or long-term rules without necessity review.
- Do not hard-delete archived items until the 30-day retention window passes and the user approves an exact delete list.
- Use this partition before staging, summarizing architecture changes, or choosing a cleanup target.

## Recommended Next Review Order

1. Review stable-framework as one architecture repair set.
2. Review unconfirmed-new-capabilities and harness-eval for “necessary vs. removable”.
3. Review archive-root-cleanup exact move/archive list.
4. Run project closeout for active project artifacts before cleanup.
5. Run historical PRD sweep only after the current architecture set is stable.

## Next User Decision Checklist

This checklist is for supervision only. It does not approve any action.

| Decision | Recommended default | Reason | Risk if deferred | User confirmation needed |
|---|---|---|---|---|
| Which eval / harness checks may become stable architecture? | Approved: `eval_suite`, `real_output_eval`, `skill_generalization`, `prototype_preview_gate`, and `external_redaction`. | These directly protect PRD quality, anti-leakage, prototype supervision, and B-package redaction. | Too many checks may violate “no unnecessary harness”; too few checks may let PRD regression recur. | No further decision for this exact set; future additions still require approval. |
| Should candidate plugins stay visible as marketplace `AVAILABLE`? | Approved if explicitly marked candidate / requires review / non-stable. | Keeps exploration available without pretending it is stable. | Agents may use candidate suites without understanding review boundaries if labels drift. | Only future plugin promotion or hidden/visible policy changes need approval. |
| Should the B-package script become a stable packager? | Approved after hard-coded project content is replaced with project input and redaction policy. | B packages are needed for protected outside delivery. | Packages may carry project-specific assumptions if generic regression fails. | Review real output before using as a delivery package. |
| Should preference memory become stable? | Approved only as project-local cache. | It improves project continuity while blocking cross-project leakage. | Premature long-term learning can pollute other projects. | Long-term memory updates still need explicit item-by-item approval. |
| Should root deleted files be accepted as deleted? | Not yet. | Canonical and archive copies must be verified first. | Accepting deletions too early can lose historical context. | Confirm exact root deletion / archive list. |
| Should historical project PRDs be swept for old wording? | Defer until architecture set is stable. | Historical project artifacts should not be mixed into framework repair. | Old project docs may confuse future readers if reused. | Confirm which projects are active enough to update. |
| Should project artifacts enter closeout? | Approved for all projects before archive. | Closeout extracts useful lessons before cleanup or archive. | Cleanup before closeout loses learning signals. | Confirm project-by-project closeout order and archive timing. |
