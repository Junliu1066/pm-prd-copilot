# Prototype Reference Analyzer Output Contract

Use this compact structure when writing a formal reference-analysis artifact.

```yaml
reference_inventory:
  - reference_id: ""
    source_type: user_provided_reference|external_reference|inferred_reference_need
    source_path_or_url: ""
    collected_at: ""
    relevant_for: ""
    human_verification_required: true
borrowable_patterns:
  - pattern: ""
    why_useful: ""
    target_output: product_flow|prototype_preview|full_prototype
do_not_copy:
  - element: ""
    reason: ""
recommended_prototype_style:
  fidelity: low_fi|mid_fi
  canvas_style: ""
  screen_style: ""
  annotation_style: ""
  review_notes: ""
style_directives:
  - directive: ""
    interpretation: ""
    applies_to: palette|typography|layout|components|annotations
    guardrail: ""
trace_notes:
  - note: ""
```
