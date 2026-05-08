# Product Value Gate V0.1 Regression Cases

These cases verify that the product value gate remains an independent pre-PRD decision layer. They are intentionally lightweight and do not require network evidence, financial modeling, new skills, or new harnesses.

| Case | Expected decision | Purpose |
|---|---|---|
| Vague AI platform idea | `E_RESEARCH_REQUIRED` | Missing key value facts must not enter full PRD. |
| Strong paid business case | `A_ENTER_PRD` | Strong payment evidence, complete input, and controlled risk can enter PRD. |
| Low-cost lead follow-up MVP | `B_LOW_COST_MVP` | Direction is plausible, but no budget or payment proof yet. |
| Custom client reporting project | `C_CLIENT_PROJECT_VALIDATION` | Client project value exists, but productization is not proven. |
| Internal delivery quality check | `D_INTERNAL_EFFICIENCY` | Internal cost/error reduction should route to internal efficiency, not external PRD by default. |
| Heavy custom portal with weak profit | `F_NOT_RECOMMENDED` | Weak profit, heavy delivery, and hard acquisition should stop PRD flow. |
| Investment return assistant | `G_BLOCKED_BY_REDLINE` | Financial return promises or stock recommendation must block. |

Acceptance requirements:

- Every case produces `00_value_gate.json` and `00_value_gate.md` in a temporary fixture.
- Every JSON output validates against `shared/schemas/value_gate.schema.json`.
- Every case includes `decision_gate`, `blocked_reasons`, `input_completeness`, and `prd_input_package`.
- Non-A cases must set `can_enter_full_prd=false`.
- Formal PRD pipeline must reject non-A decisions.
- `--fast-draft` may bypass only as a labeled draft path and must record `value_gate_bypassed=true`.
