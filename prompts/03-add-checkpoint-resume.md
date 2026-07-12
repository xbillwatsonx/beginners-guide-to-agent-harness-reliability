# Prompt 03: Add Checkpoint/Resume Rules

Copy this into your agent chat:

```text
Please add a checkpoint/resume pattern for interrupted work.

The checkpoint should include:
1. Goal.
2. Current status.
3. Decisions already made.
4. Paths changed.
5. Validation already completed.
6. Blockers.
7. Next action.
8. What not to redo.
9. Evidence paths or sources.

Use this JSON shape:

{
  "id": "CRP-YYYYMMDD-001",
  "task_id": "OP-001",
  "source": "Session checkpoint",
  "goal": "Concrete goal being resumed.",
  "status": "in_progress",
  "decisions": ["Decision already made."],
  "changed_paths": ["path/changed.md"],
  "validation_done": ["Command or check that passed."],
  "blockers": [],
  "next_action": "The next concrete action.",
  "do_not_redo": ["Work already verified."],
  "evidence": ["path/or/source"],
  "expected_validator_result": "pass"
}

Do not create automation. Start with a manual template and one example.
```
