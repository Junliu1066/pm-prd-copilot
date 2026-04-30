# Interactive HTML Prototype Builder Output Contract

Use this compact structure in `prototype_manifest.json` and summarize the same information in `prototype_notes.md`.

```yaml
prototype_type: interactive_html
input_mode: requirement_to_html|preview_to_html|image_to_html|modify_existing_html
fidelity: low|mid
target_surface: mobile|desktop|responsive
source_artifacts:
  - type: prd|user_story|product_flow|prototype_preview|reference_image|existing_html|user_feedback
    path_or_description: ""
screen_inventory:
  - screen_id: ""
    screen_name: ""
    purpose: ""
    entry_points: []
    primary_actions: []
    states: []
multi_page_structure:
  source_sequence_preserved: true
  shared_shell: true
  route_map:
    - nav_or_action: ""
      target_screen: ""
interaction_inventory:
  - interaction_id: ""
    trigger: ""
    from_screen: ""
    result: navigate|modal|drawer|tab|filter|form_feedback|state_change|toast
    target: ""
route_context_transfer:
  - route_id: ""
    trigger: ""
    from_screen: ""
    to_screen: ""
    transferred_context: []
    return_path: ""
inline_editing:
  enabled: true
  trigger: double_click_text
  save_behavior: enter_or_blur
  cancel_behavior: escape
  persistence: local_storage|none
editable_files:
  - path: ""
    purpose: structure|styles|interactions|manifest|notes|asset
platform_compatibility:
  supported_platforms: [macOS, Windows]
  path_strategy: relative_paths_only
  requires_server: false
  requires_dependencies: false
  open_entry: index.html
  single_file_entry: standalone.html
  zip_package: ""
  helper_launchers: []
  handoff_rule: "Recommended handoff is the zip package; unzip it and open index.html. For one-file sharing use standalone.html."
feedback_application_log:
  - feedback: ""
    classification: copy|page_structure|interaction|state|visual_style|business_logic
    files_updated: []
    product_flow_updated: true
validation_checklist:
  local_files_exist: true
  navigation_targets_checked: true
  dead_clicks_checked: true
  overlay_close_checked: true
  viewport_fit_checked: true
  text_clipping_checked: true
open_review_questions:
  - question: ""
```
