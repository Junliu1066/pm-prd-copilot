# Upstream Agent Skills Routing

Source: https://github.com/addyosmani/agent-skills

Use upstream skills directly when they are installed or provided as task context. Do not register them as stable local skills unless the user explicitly approves.

## Default For Development And Testing

| Skill | Use for | Boundary |
|---|---|---|
| `incremental-implementation` | multi-file implementation or non-trivial fixes | implement small vertical slices; do not commit or push |
| `test-driven-development` | behavior changes, bug fixes, test coverage | tests are proof; do not skip validation |
| `debugging-and-error-recovery` | failing tests, broken builds, unexpected behavior | reproduce, localize, reduce, fix, guard |
| `code-review-and-quality` | review before handoff | find bugs, regressions, missing tests, maintainability issues |
| `code-simplification` | working but complex code | preserve behavior; avoid unrelated refactors |
| `source-driven-development` | framework/library uncertainty | use official sources; mark unverified claims |

## Conditional

| Skill | Trigger | Boundary |
|---|---|---|
| `frontend-ui-engineering` | UI work | implement approved UI only |
| `browser-testing-with-devtools` | browser runtime testing/debugging | inspect and test; do not change release config |
| `api-and-interface-design` | API or module boundary work | consume or refine approved contracts; report contract changes |
| `security-and-hardening` | user input, auth, permissions, data, external integrations | report high-risk findings upstream |
| `performance-optimization` | explicit performance goal or regression | measure before optimizing |
| `ci-cd-and-automation` | CI/test pipeline failure | deployment pipeline changes require upstream approval |
| `documentation-and-adrs` | implementation docs are required | document implementation why; do not write governance policy |
| `deprecation-and-migration` | approved migration/removal | data/user-impacting migration requires upstream approval |

## Do Not Use As Development Agent Duties

| Skill | Reason |
|---|---|
| `idea-refine` | product discovery |
| `spec-driven-development` | PRD/spec authorship |
| `shipping-and-launch` | release ownership |
| `git-workflow-and-versioning` | commit/push/versioning risk; use only for atomic-change thinking |

`planning-and-task-breakdown` may be used only to fill missing development/testing task packages without changing product scope.
