# Low-Fi Prototype Designer Output Contract

Use this compact structure when writing formal prototype artifacts.

```yaml
prototype_mode: preview|full
approval_status: draft|approved|required
source_flow_id: ""
reference_ids: []
screen_list:
  - screen_id: ""
    screen_name: ""
    included_in_preview: true
screen_specs:
  - screen_id: ""
    goal: ""
    entry_point: ""
    key_regions: []
    primary_cta: ""
    secondary_actions: []
    next_step: ""
    exception_states: []
transition_annotations:
  - from_screen: ""
    action: ""
    to_screen: ""
    system_feedback: ""
feedback_application_log:
  - feedback: ""
    classification: business_logic|page_structure|copy|visual_style|exception_state
    files_or_sections_updated: []
    product_flow_updated: true
prototype_artifact:
  format: markdown|html_svg|json
  path_or_inline: ""
delivery_artifacts:
  - artifact_type: png|svg|html|markdown
    path: ""
    purpose: direct_review|editable_source|documentation
visual_qa_checklist:
  text_overlap_checked: true
  centered_text_checked: true
  clipping_checked: true
  contrast_checked: true
  png_matches_source_checked: true
open_review_questions:
  - question: ""
```
