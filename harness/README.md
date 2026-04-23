# Harness

The harness validates PM Copilot governance before workflow stages advance.

## First-version checks
- `registry`: skills, MCP tools, stewards, and artifacts are registered consistently.
- `steward_contract`: trace entries do not call unregistered capabilities or produce undeclared artifacts.
- `workflow_gate`: stage gates and human approvals are respected.
- `source_trace`: MCP-derived external data includes trace fields and human verification requirement.
- `scaling_policy`: chief steward and sub-steward load stays within the dynamic scaling policy.
- `teaching_absorption`: accepted lessons are structured, assigned to affected components, and ready to be absorbed.
- `random_audit`: risk-weighted random audit of trace calls and boundaries when `--audit` is passed.
- `efficiency`: artifact size, Skill/MCP call count, repeated output, and token-like waste when `--efficiency` is passed.

## Usage
```bash
python3 harness/run_harness.py --base-dir . --project fitness-app-mvp --mode advisory
```

Use `--mode strict` when warnings should block advancement.

Run the random audit inspector:

```bash
python3 harness/run_harness.py --base-dir . --project fitness-app-mvp --mode advisory --audit
```

Run the efficiency auditor:

```bash
python3 harness/run_harness.py --base-dir . --project fitness-app-mvp --mode advisory --efficiency
```
