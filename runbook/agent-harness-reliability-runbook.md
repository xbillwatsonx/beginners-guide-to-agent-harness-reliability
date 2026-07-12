# Agent Harness Reliability Runbook

## Who This Is For

This runbook is for people using AI agents for real work: coding, business operations, research, writing, customer support, or project management.

You may need this if your agent:

- forgets where a decision came from
- writes too much into long-term memory
- repeats work after a pause
- loses track of which task is active
- treats an unreviewed draft like finished work
- guesses where notes should go

## The Main Idea

An agent is more reliable when important work leaves a trail.

That trail does not need to be complicated. A useful first version has:

1. a memory write rule
2. a task update rule
3. a checkpoint/resume rule
4. a few examples the agent can validate

## Step 1: Decide What Counts As Important

Not everything belongs in permanent memory.

Good durable memory candidates:

- explicit user preferences
- standing operating rules
- project decisions
- recurring mistakes and fixes
- important blockers
- links to durable project docs

Poor durable memory candidates:

- one-off chat details
- temporary ideas
- raw logs
- private secrets
- long task closeouts that belong in a report or daily note

## Step 2: Use A Memory Write Proposal

Before writing important memory, ask the agent to make a small proposal:

```json
{
  "id": "MWP-YYYYMMDD-001",
  "type": "project_decision",
  "destination": ["memory/YYYY-MM-DD.md"],
  "source": "User chat YYYY-MM-DD HH:MM",
  "summary": "Short write-ready summary.",
  "confidence": "high",
  "approval": "auto-safe",
  "reason": "Why this route is correct.",
  "expiry": "daily",
  "expected_validator_result": "pass"
}
```

This makes the agent answer a few boring but important questions:

- What kind of information is this?
- Where should it go?
- Who said it?
- Is it durable or temporary?
- Is it safe to write automatically?

## Step 3: Use A Tracker Update Proposal

For task changes, keep the shape smaller:

```json
{
  "id": "TUP-YYYYMMDD-001",
  "task_id": "OP-001",
  "type": "task_status_update",
  "source": "User chat YYYY-MM-DD HH:MM",
  "status_change": "ACTIVE to COMPLETE",
  "summary": "Short task closeout.",
  "next_step": "What happens next.",
  "evidence": ["path/or/source"],
  "approval": "auto-safe",
  "review_state": "not-needed",
  "expected_validator_result": "pass"
}
```

The most important rule:

> Do not mark unreviewed work complete.

## Step 4: Add Checkpoint/Resume Records

Use a checkpoint after interruption, compaction, delegation, or any meaningful pause.

```json
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
```

The `do_not_redo` field matters. It stops future agents from wasting time and accidentally breaking finished work.

## Step 5: Keep Validation Small

You do not need a big test system at first.

Start with a simple checker that confirms:

- required files exist
- example JSON is valid
- memory proposals include a source
- checkpoint records include next action and do-not-redo notes
- public package files do not contain private paths or secrets

Then add real examples when something goes right or wrong.

## Step 6: Review Before Automating

Manual first. Automation later.

Do not wire this into cron, background jobs, or automatic memory writes until:

- you have real examples
- warning/failure cases catch actual mistakes
- the workflow does not annoy you
- you know what it is allowed to block

## What To Do After This

After this first setup, your agent should know how to:

- ask before writing uncertain durable rules
- keep long-term memory short
- put detailed closeouts in daily notes or reports
- resume after interruption
- avoid redoing verified work
- preserve a review trail for task changes
