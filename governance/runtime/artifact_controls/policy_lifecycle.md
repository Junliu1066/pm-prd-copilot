# Policy Lifecycle Controls

## Purpose

Keep the artifact control layer reusable across future development projects without turning project-facing documents into governance manuals.

## Long-Term Contract

- The control layer is project-agnostic.
- Project artifacts may point to the control layer, but should not expand it into visible content by default.
- Policy files should use ordinary operational names, not product-specific or user-specific names.
- New development projects should be able to reuse this layer without copying it into their project folder.
- When the user identifies a rule as long-term or reusable, classify it through learning feedback before treating it as stable behavior.

## Versioning

- `control_manifest.yaml` owns the policy version.
- Backward-compatible updates may add checks, examples, or modules.
- Breaking updates are changes that remove a required gate, change the quiet pointer pattern, or alter source-of-truth hierarchy.
- Breaking updates require an explicit review note and user approval when they affect stable behavior.

## Discovery Rules

- `agent.md` is the primary shallow entry.
- `index.md` is the deep policy entry.
- `control_manifest.yaml` records scope, owners, triggers, and compatibility.
- Project artifacts may include the quiet pointer comment when future model runs should apply the policy.

## Upgrade Flow

1. Capture user feedback through `learning_feedback.md`.
2. Decide whether the feedback is project-specific or reusable.
3. If reusable, propose a policy update.
4. Update the smallest relevant module.
5. Update `control_manifest.yaml` only when scope, version, triggers, owners, or compatibility change.
6. Run formatting and registry checks when registry entries change.

## Anti-Patterns

- Do not copy the full control system into every development document.
- Do not hide the policy so deeply that model runs cannot discover it.
- Do not store project-specific decisions in the generic policy layer.
- Do not let the policy layer override explicit user instructions.
- Do not silently convert a one-off correction into stable memory.
