# Efficiency Check Rules

## Purpose

Prevent project work from expanding into unnecessary skills, repeated documents, oversized artifacts, or conflicting outputs.

## Triggers

Run efficiency review when:

- More than 7 skills or steward roles are active for one project.
- The same scope appears in more than 3 artifacts.
- A final document repeats entire sections from phase documents.
- Review output creates new artifacts without merging decisions.
- The user asks for packaging or handoff and artifact count has grown.

## Checks

- Are there duplicate documents serving the same purpose?
- Can phase content be summarized in the final document instead of copied fully?
- Is each skill or steward still needed?
- Are old generated drafts clearly superseded by final artifacts?
- Are acceptance criteria and tests repeated with conflicting wording?
- Is the final package small enough for a developer to use without reading everything?

## Actions

- Recommend merging duplicated sections.
- Prefer an index README over long repeated summaries.
- Keep final documents concise and point to phase details when needed.
- Do not reduce security, review, or test coverage solely to reduce size.
- Do not delete artifacts without explicit user request.
