# Project Preference Cache Manager Output Contract

Use this compact structure when writing formal preference-cache artifacts.

```yaml
project_id: ""
cache_id: ""
operation: create|record_candidate|approve|reset|clear|read
status: active|cleared|archived
approved_preferences_used:
  - preference_id: ""
    category: ""
    summary: ""
    source_trace_id: ""
candidate_preferences_recorded:
  - preference_id: ""
    category: ""
    summary: ""
    approval_needed: true
source_trace:
  - source_trace_id: ""
    source_type: user_feedback|file|external_reference
    source_ref: ""
    captured_at: ""
    human_verification_required: true
```
