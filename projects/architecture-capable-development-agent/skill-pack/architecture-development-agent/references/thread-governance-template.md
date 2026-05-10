# Threaded Development Testing Template

## Activation

Use threaded development only when work can be split by independent write scopes and integration gates. Keep single-thread work single-thread.

## Thread Matrix

| Thread | Development goal | Allowed writes | Forbidden writes | Dependencies | Risk | Status |
|---|---|---|---|---|---|---|
| T-A |  |  |  |  | low / medium / high | planned |

## Contract Freeze

| Contract | Status | Owner | Change policy |
|---|---|---|---|
| API | missing / draft / frozen / none | upstream | report blocker if not frozen |
| DB schema | missing / draft / frozen / none | upstream | stop unless approved |
| AI output | missing / draft / frozen / none | upstream | report blocker if unclear |
| permissions | missing / draft / frozen / none | upstream | report blocker if unclear |
| page state | missing / draft / frozen / none | upstream | report blocker if unclear |

## Startup Package

```text
Thread:
Branch:
Development goal:
Context:
Inputs:
Allowed writes:
Forbidden writes:
Dependencies:
Steps:
Validation:
Acceptance:
Rollback:
Evidence:
Approval points:
```

## State Machine

```text
planned -> ready -> running -> self_checked -> reviewed
-> gate_passed -> integration_pending
-> integration_passed / integration_failed
-> fix_required / blocked / closed
```

## Integration

- Do not merge directly to main unless explicitly authorized.
- Integrate only threads that are `gate_passed`.
- Locate failures by responsible thread.
- Send fixes back to the responsible thread or a scoped fix thread.
- Close every thread with checks, files, rollback, risk, and upstream blocker status.
