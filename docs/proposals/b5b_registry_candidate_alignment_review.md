# B5b Registry And Candidate Alignment Review

- Date: 2026-04-30
- Status: alignment review only
- Scope: marketplace, registry, and candidate plugin source sequencing
- Rule: this file does not approve staging, commit, push, PR, plugin promotion, skill creation, harness creation, archive, cleanup, deletion, or stable-policy adoption.

## Conclusion

Do not commit the currently staged marketplace change by itself.

The staged `.agents/plugins/marketplace.json` change is correctly labeled as candidate visibility, but it references candidate plugin folders that are still untracked in the current repository state. Committing marketplace visibility alone would make the stable repository advertise candidate plugins whose source directories are not yet present.

The safer long-term path is:

1. Keep marketplace candidate visibility as B5b staging only for now.
2. Review registry/plugin-source alignment before any B5b commit.
3. Commit candidate visibility only in a coordinated batch that includes the minimum registry and source files needed to avoid broken references.
4. Keep all entries candidate / non-stable / detachable / user-review-required.

## Current Staged State

Staged file:

```text
.agents/plugins/marketplace.json
```

Staged purpose:

- Make 6 plugin suites visible in the local marketplace.
- Mark every visible suite as candidate, non-stable, detachable, and requiring user review before stable use.

Current risk:

- 5 referenced plugin suite directories are still untracked.
- Matching registry updates are not staged.
- A marketplace-only commit can create a stable-repo drift between visible capabilities and committed candidate source.

## Alignment Findings

### Marketplace Entries

Marketplace currently lists 6 candidate plugins:

```text
prd-analysis-suite
prd-prototype-suite
preference-memory-suite
quality-evaluation-suite
delivery-planning-suite
ai-solution-planning-suite
```

All entries include the required governance fields:

```json
{
  "status": "candidate",
  "stable": false,
  "detachable": true,
  "reviewLabel": "candidate / requires review / non-stable capability",
  "requiresUserReviewBeforeStableUse": true
}
```

### Registry Plugins

`registry/plugins.yaml` in the working tree has matching entries for all 6 candidate plugins.

Important detail:

- `registry/plugins.yaml` is plugin-level alignment.
- It references `owns_skills`.
- Those skill names must stay aligned with `registry/skills.yaml` and the actual plugin source folders.

### Registry Skills

`registry/skills.yaml` in the working tree contains skill-level candidate contracts for:

| Plugin | Candidate skill count |
|---|---:|
| `prd-analysis-suite` | 6 |
| `prd-prototype-suite` | 4 |
| `preference-memory-suite` | 1 |
| `quality-evaluation-suite` | 1 |
| `delivery-planning-suite` | 11 |
| `ai-solution-planning-suite` | 9 |

It also includes related existing-skill contract edits, such as source intake, market signals, success metrics, and pre-development questions.

Because `registry/skills.yaml` is much broader than marketplace visibility, it should not be blindly bundled into B5b without a dedicated skill-contract review.

### Candidate Plugin Source

Committed source currently exists for:

```text
plugins/prd-analysis-suite/
```

New untracked source currently exists for:

```text
plugins/prd-prototype-suite/
plugins/preference-memory-suite/
plugins/quality-evaluation-suite/
plugins/delivery-planning-suite/
plugins/ai-solution-planning-suite/
```

Alignment check result:

```text
marketplace entries: 6
registry plugin entries: 6
plugin folders in working tree: 6
registry owns_skills vs registry/skills plugin mapping: aligned
skill registry paths vs plugin SKILL.md files: aligned
issues: none
```

The alignment is clean in the working tree, but not yet safe to commit as independent pieces.

## Decision Options

| Option | Effect | Risk | Recommendation |
|---|---|---|---|
| A. Commit marketplace only now | Fast; visible candidate plugins appear immediately | Stable repo can reference uncommitted plugin folders and unstaged registry contracts | Do not choose |
| B. Stage and commit marketplace + `registry/plugins.yaml` only | Plugin-level registry aligns with marketplace | Registry can reference uncommitted plugin source and skill contracts | Do not choose yet |
| C. Create one coordinated candidate-visibility commit including marketplace, plugin registry, skill registry, and minimum plugin source | Stable repo has no broken references; candidate boundary is explicit | Larger commit; needs careful review to avoid promoting unstable behavior | Preferred after review |
| D. Unstage marketplace until the coordinated candidate batch is ready | Lowest accidental-commit risk | Slightly slower; loses current staged checkpoint | Best if we pause before candidate source review |

Recommended path:

- Keep B5b staged only if we are immediately continuing to the coordinated candidate review.
- If work pauses or another batch needs staging, unstage `.agents/plugins/marketplace.json` first to avoid accidental marketplace-only commit.
- Do not commit marketplace until the candidate source and registry batch is approved.

## Proposed Next Batch

Create a dedicated D1 candidate plugin source and registry staging review.

Suggested scope for review:

```text
.agents/plugins/marketplace.json
registry/plugins.yaml
registry/skills.yaml
plugins/prd-prototype-suite/
plugins/preference-memory-suite/
plugins/quality-evaluation-suite/
plugins/delivery-planning-suite/
plugins/ai-solution-planning-suite/
```

Potentially include existing `plugins/prd-analysis-suite/` only if there are uncommitted changes under that folder. Current tracked source already exists for it.

Must exclude:

```text
harness/*
ai-intel/*
projects/*
docs/proposals/*
docs/archive/*
memory-cache/*
root deleted files
```

## Approval Needed

The user needs to choose one of these next actions:

| Decision | Result | My recommendation |
|---|---|---|
| Continue directly to D1 coordinated candidate review | Keeps momentum and prevents marketplace/registry/source drift | Recommended |
| Unstage B5b marketplace now and review D1 later | Safest if another unrelated batch must be handled first | Acceptable |
| Commit marketplace only | Fast, but can create broken candidate references | Not recommended |

## Validation Plan For D1 Review

Before any D1 staging or commit:

```bash
git diff --check
python3 pm-prd-copilot/scripts/run_regression.py --base-dir . --strict
python3 harness/run_harness.py --base-dir . --project demo-project --mode advisory --check-only --audit --efficiency
git diff --cached --name-only
```

Additional D1-specific checks:

- Every marketplace plugin must exist in `registry/plugins.yaml`.
- Every `registry/plugins.yaml` `owns_skills` entry must exist in `registry/skills.yaml`.
- Every candidate skill path in `registry/skills.yaml` must contain `SKILL.md`.
- Every candidate plugin must remain `status: candidate`.
- No candidate plugin can be marked stable.
- No plugin source can reference project-specific paths, `.env`, `.venv`, `/Users/`, or host-only internal files.

## Current Recommendation

Do not commit B5b yet.

Next best step is D1 coordinated candidate review. That review should decide whether the candidate marketplace, registry, and plugin source can be committed together as a candidate-only batch, or whether some candidate suites should remain uncommitted until more evidence exists.

