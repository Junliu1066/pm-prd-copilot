# Source Collector Output Contract

Use this compact structure when writing a formal source brief.

```yaml
source_summary: ""
explicit_requirements:
  - requirement: ""
    source: ""
inferred_requirements:
  - requirement: ""
    rationale: ""
constraints:
  - constraint: ""
    source: ""
unknowns:
  - question: ""
    why_it_matters: ""
source_trace:
  - source_id: ""
    type: user_input|file|web|mcp|inference
    location: ""
    verification_status: user_provided|unverified_external|inferred
```
