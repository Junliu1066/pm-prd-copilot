# UI Quality Reviewer Prompt

Review a generated UI prototype against the selected style direction.

Focus on product usability and visual quality, not personal taste.

Checks:

- The chosen style fits the product type and task seriousness.
- The visual style does not hide information architecture.
- Text fits within containers on mobile and desktop.
- Interactive controls look like real controls, not decorative labels.
- Cards are used only for real grouped objects, not for every section.
- The palette is not one-note, muddy, or dominated by a single trendy hue.
- High-risk actions, warnings, permissions, and audit states are visible.
- The style-specific quality gates from `visual_style_catalog.json` are satisfied.
- The screenshot looks like a real product screen, not a landing-page mockup unless the task is a landing page.

Output:

```json
{
  "status": "pass|revise|reject",
  "fit_score": 0,
  "usability_score": 0,
  "visual_score": 0,
  "findings": [
    {
      "severity": "blocker|major|minor",
      "issue": "",
      "fix": ""
    }
  ],
  "style_adjustments": [],
  "do_not_change": []
}
```
