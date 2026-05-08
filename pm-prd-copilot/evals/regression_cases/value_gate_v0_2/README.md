# Product Value Gate V0.2 Regression Cases

V0.2 verifies that the value gate is no longer only a coarse `A/B/C/D/E/F/G` classifier. It must also produce a usable pre-PRD analysis package.

Required V0.2 sections:

- `value_object_detail`
- `measurability_judgment`
- `attribution_judgment`
- `value_quality_judgment`
- `true_profit_judgment`
- `resource_fit_judgment`
- `acquisition_judgment`
- `project_to_product_judgment`
- `low_cost_mvp_judgment`
- `counter_evidence`

Key acceptance cases:

| Case | Expected decision | Extra V0.2 requirement |
|---|---|---|
| GEO with MVP experiment and paid peer signal | `A_ENTER_PRD` | External commercial product intent, GEO metrics, project-to-product risk. |
| GEO idea without payment proof | `B_LOW_COST_MVP` or `E_RESEARCH_REQUIRED` | Must not be promoted to full PRD. |
| Strong custom client project | `C_CLIENT_PROJECT_VALIDATION` | Must separate project value from product value. |
| Internal cost reduction | `D_INTERNAL_EFFICIENCY` | Must not be packaged as external product by default. |
| Weak profit and heavy delivery | `F_NOT_RECOMMENDED` | Must provide stop reasons and counter-evidence. |
| Financial return promise or medical diagnosis | `G_BLOCKED_BY_REDLINE` | Must block full PRD. |

V0.2 remains rule-based. It does not fetch network evidence, perform complex financial modeling, create new skills, or create new harnesses.
