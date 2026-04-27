# Security Control Rules

## Purpose

Make security-sensitive development artifacts testable and consistent, especially for systems that manage credentials, tokens, local agents, or machine-level commands.

## Required Security Checks

| Area | Control |
|---|---|
| Passwords | Store only password hashes |
| Sessions | Use HttpOnly cookies; require Secure cookies in HTTPS production |
| Enrollment tokens | Return plaintext only once; store only hash |
| Agent tokens | Do not log plaintext tokens |
| Private keys | Never store Agent private key in Controller |
| Logs | Redact tokens, private keys, Authorization headers |
| Audit events | Store only necessary, redacted metadata |
| RBAC | Enforce permissions in backend handlers |
| Last admin | Prevent disabling, deleting, or demoting the last Admin |
| Local commands | Use argument arrays, not shell string concatenation |
| Test execution | Use dry-run or fake runner where real system changes are unsafe |

## Review Triggers

Run safety review when:

- A document mentions token creation, storage, display, or copying.
- An Agent calls local system tools.
- A page or API exposes logs, errors, or audit metadata.
- A role or permission changes.
- A deployment document mentions HTTPS, services, or credentials.

## Blocking Issues

The artifact must not be finalized if it:

- Says token plaintext can be retrieved after creation.
- Allows Controller to store Agent private keys.
- Relies on frontend-only permission enforcement.
- Logs raw command output without a redaction rule.
- Tests destructive system behavior without dry-run, fake runner, or explicit isolation.
