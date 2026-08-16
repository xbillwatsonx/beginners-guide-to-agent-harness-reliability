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
  "type": "checkpoint_resume",
  "task_id": "TASK-001",
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

In addition to the template, install the full checkpoint/resume behavior:

1. **When to create a checkpoint**: after an interruption, compaction, delegation, or before a meaningful pause.
2. **When to update a checkpoint**: after completing the next_action, when new decisions are made, when validation results change, or before another pause or handoff.
3. **How to resume from a checkpoint**: read the latest checkpoint, check whether the evidence and validation are still current, do the next_action, and update the checkpoint before pausing again. Re-verify if files, dependencies, or assumptions changed. Do not redo work listed in do_not_redo unless something changed or the evidence is stale.

Create a short resume procedure the agent can follow every time it starts a new session or resumes after a pause.
```
