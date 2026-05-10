# Package Manifest

## Package

- Name: `development-test-agent-package`
- Purpose: self-contained handoff package for a development-and-testing-only Codex agent with A1/A2/A3 feasibility, orchestration, module preflight governance, Module B quality gates, architecture feedback, dynamic skill/harness planning, and approval requests.
- Source folder: `projects/architecture-capable-development-agent`
- Stable registry status: not registered.

## Included Files

| Path | Purpose |
|---|---|
| `README.md` | Package usage guide. |
| `00_source_notes.md` | Source and design notes. |
| `01_agent_prompt.md` | Development Test Agent prompt. |
| `02_codex_development_document_template.md` | Execution document template. |
| `03_thread_governance.md` | Threaded development/testing rules. |
| `04_task_cards.md` | Copy-ready task cards. |
| `05_handoff_packet.md` | Full handoff packet. |
| `06_upstream_agent_skills.md` | Routing for addyosmani/agent-skills. |
| `skill-pack/architecture-development-agent/SKILL.md` | Candidate Codex skill. |
| `skill-pack/architecture-development-agent/agents/openai.yaml` | Skill UI metadata. |
| `skill-pack/architecture-development-agent/references/*.md` | Skill references. |

## Excluded

- `.DS_Store`
- registry changes
- stable policy changes
- harness / workflow / automation changes
- git staging, commits, push, PR
