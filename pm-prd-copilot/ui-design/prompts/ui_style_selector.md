# UI Style Selector Prompt

You are selecting a visual design language for a product prototype.

Do not generate the screen yet. First decide whether the product needs a restrained operational style, a brand-forward style, or an expressive material/editorial style.

Inputs:

- Product brief or PRD
- Target users
- Core jobs-to-be-done
- Information density
- Usage frequency
- Trust, compliance, and accessibility risks
- Explicit user style request, if any

Output:

```json
{
  "recommended_style_id": "",
  "backup_style_ids": [],
  "why_this_style": [],
  "why_not_more_expressive": [],
  "design_tokens": {
    "palette": [],
    "typography": "",
    "radius": "",
    "density": "",
    "texture": "",
    "layout": "",
    "motion": ""
  },
  "component_bias": [],
  "avoid": [],
  "quality_gates": []
}
```

Rules:

- If the product is an internal tool, dashboard, finance workflow, compliance workflow, or high-frequency operations surface, start with `swiss_utility` or `refined_saas`.
- If the user explicitly asks for concrete/cement/industrial style, consider `concrete_editorial`, but warn when the product has dense tables or sensitive workflows.
- If the user asks for "cool", "AI", "future", or "agent", consider `ai_lab_dark` or `glass_depth`; choose the one that preserves readability.
- If the product is content-led, research-led, or report-led, consider `editorial_magazine` or `data_newsroom`.
- Do not pick brutalist, cyber, clay, glass, or concrete styles just to avoid a generic-looking UI.
- Every expressive style needs an explicit reason and a risk note.
