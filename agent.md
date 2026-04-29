# Project Working Notes

Use these notes when planning, editing, or packaging work in this repository.

## Layer 1: Basic Rules

### 1. Know The Reader

Before preparing a document or package, identify who will read it:

- Core team: include the full working notes needed to execute the project well.
- Outside reader: include only what they need to build, review, or accept the work.

If the reader is unclear, prepare the simpler sharing version first.

### 2. Keep Documents In Their Lane

- Product documents explain users, value, scope, flows, acceptance, metrics, and risks.
- Development documents explain implementation, task boundaries, checks, and delivery steps.
- Working notes and process details stay out of customer-facing or vendor-facing files.

### 3. Start With Clarity

Before implementation, separate:

- confirmed facts
- working assumptions
- blocking questions
- non-blocking questions

Do not start work if a blocking question changes the direction of the build.

## Layer 2: Work Rules

### 4. Prepare Before Editing

Before writing files:

- read the task brief
- confirm the input documents
- look for existing local instructions, templates, scripts, and examples
- prefer existing project patterns over creating new ones
- confirm which files may be changed
- confirm which files must not be changed
- identify decisions that need approval

### 5. Task Brief Format

Each implementation task should state:

- goal
- inputs
- files allowed to change
- files not allowed to change
- expected output
- check to run
- approval points
- smallest acceptable fix
- follow-up note, if something should be reused next time

### 6. Work Sequence

Use this sequence for substantial work:

```text
review inputs
-> check blockers
-> prepare task brief
-> implement
-> round 1: check changed work
-> fix found issues
-> round 2: check omissions and consistency
-> simplify where possible
-> record useful follow-up
-> summarize delivery
```

If checks cannot run, state why and provide a substitute check.

### 7. Mid-Work Corrections

When the user corrects an error, adds a requirement, or changes priority while work is in progress:

- pause and re-read the latest instruction
- re-check affected files before continuing
- update the plan or checklist
- decide whether previous edits still apply
- rerun checks for any affected path
- report the correction and the resulting change in the delivery summary

## Layer 3: Deeper Checks

### 8. Fit Check

Before choosing a solution, ask:

- Does this match the current product scope?
- Does it reuse an existing project pattern?
- Does it avoid adding unnecessary moving parts?
- Can the issue be solved by an existing skill, check, script, template, or documentation update instead of adding a new stable component?
- Does it keep user-facing behavior separate from working notes?
- Does it leave a clear path for review and rollback?

### 9. Quality Check

Before delivery, check:

- the changed files are within the allowed range
- the main user path still works
- empty, loading, error, and permission states are handled where relevant
- data has source, time, and status where relevant
- AI output has source, confidence, risk note, and fallback where relevant
- risk-sensitive wording has been reviewed
- tests or substitute checks are recorded
- round 1 and round 2 self-check results are recorded

### 10. Efficiency Check

Before finalizing, ask:

- Was an existing template, script, or pattern available?
- Was any work repeated unnecessarily?
- Could a smaller change solve the same problem?
- Are there files or outputs that should not be included?
- Is the result easy for the next worker to continue?

## Layer 4: Sharing Rules

### 11. Short-Name Package

For files that may be shared outside the core team:

- use short file names selected by the project, such as `A.md`, `B.md`, `C.md`
- include only execution requirements, quality checks, acceptance rules, and delivery boundaries
- use plain terms such as preparation check, quality check, independent review, efficiency review, and retrospective
- do not include private working notes, internal role maps, reusable rule paths, or automation details
- run the final content review before delivery

### 12. Sharing Review

Before sharing a package outside the core team:

- remove files that are only useful to the core team
- remove comments about how the project owner works
- remove reusable process details
- keep enough detail for the receiver to build and verify the project
- prefer the short-name package when unsure

## Layer 5: Approval And Follow-Up

### 13. Approval Points

Ask before:

- changing product scope
- changing database structure
- connecting a new outside data source
- changing model provider or high-cost model usage
- changing publishing or deployment behavior
- deleting or migrating data
- pushing to a remote repository or opening a public review
- changing persistent project rules

### 14. Reuse And Learning

User corrections should be handled carefully:

- one-time correction: fix only the current artifact
- project preference: record only for the current project after approval
- general rule: present a concrete recommendation plan and wait for approval
- reusable system change: present a concrete recommendation plan and wait for approval

Do not silently turn one correction into a permanent rule.

### 14.5 Stable Change Recommendation Plan

Before changing persistent project rules, stable preferences, Skill behavior, harness checks, workflow stages, steward rules, plugin rules, automation rules, or other long-lived system behavior, first provide a concrete recommendation plan for user review.

The recommendation plan must include:

- problem background
- recommended change
- advantages
- disadvantages and risks
- alternatives
- recommended conclusion: do, defer, one-time only, or do not do
- execution scope and expected file paths
- validation method
- approval points

Only implement after explicit user approval. After approval, implement only the approved scope. Do not treat vague agreement, discussion, or correction as permission to write a stable rule.

### 15. Minimal Governance Additions

Do not add a new skill, harness checker, steward, plugin, workflow stage, registry category, long-lived rule, or automation unless it is necessary.

Before proposing or adding one:

- try to reuse or extend an existing component
- explain why documentation, a template, a script option, or an existing check is insufficient
- state the smallest acceptable change
- list the ongoing maintenance cost
- identify the user approval required before it becomes stable

When unsure, create a proposal or note instead of adding a permanent component.

### 16. Version And Model Update Pruning

After any version update, model update, model provider change, SDK/API update, pricing change, deprecation notice, or major architecture change:

- run the required checks before trusting the update
- audit whether existing skills, harness checkers, stewards, plugins, workflow stages, registry categories, long-lived rules, automations, templates, or package paths are still necessary
- identify duplicate, unused, model-obsoleted, project-specific, or high-maintenance components
- propose deprecate, archive, or delete candidates with evidence and replacement paths
- do not hard-delete stable components without exact user approval
- prefer deprecate or archive before hard deletion

## Layer 6: Delivery Self-Check

### 17. Round 1: Changed Work

Before delivery, verify the files just changed:

- syntax, formatting, or schema checks
- targeted scripts or tests
- relevant project checks
- no new unexplained warnings or failures

### 18. Round 2: Omissions And Consistency

After round 1 passes, check for missing follow-through:

- re-read the latest user request
- inspect the diff and changed-file scope
- check whether related docs, templates, reports, generated files, or configuration need updates
- check whether any new skill, harness checker, steward, plugin, workflow stage, registry category, long-lived rule, or automation was truly necessary
- after version or model updates, check whether any existing stable component should become a deprecate, archive, or delete candidate
- check whether any user-created work was overwritten or ignored
- list remaining approval decisions

If a check finds a problem, fix it and rerun the affected check before delivery.

### 19. Delivery Summary

When finishing work, report:

- what changed
- where it changed
- round 1 checks and results
- round 2 checks and results
- what could not be checked
- which package is safe to share, if packaging was requested
