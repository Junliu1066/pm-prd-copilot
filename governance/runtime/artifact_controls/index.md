# Artifact Controls Index

Use these controls when producing, revising, or finalizing reusable project development artifacts. They apply to PRDs, staged plans, technical designs, implementation handoff docs, test plans, deployment notes, and generated project packages.

Policy metadata lives in `control_manifest.yaml`.

Apply the modules in this order:

1. `policy_lifecycle.md`
2. `source_of_truth.md`
3. `steward_routing.md`
4. `review_gates.md`
5. `change_controls.md`
6. `security_controls.md`
7. `test_controls.md`
8. `efficiency_checks.md`
9. `learning_feedback.md`

Runtime rule:

- Keep the user-facing artifact concise and implementation-focused.
- Keep coordination, review, efficiency, and learning controls in this policy layer unless the user explicitly asks to expose them in the artifact.
- If a project artifact includes a quiet internal pointer to this index, treat that pointer as an instruction to apply these controls while editing, not as content to expand for readers.
- Treat this as a long-term reusable policy layer. Do not duplicate it into individual project documents.
