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

An agent harness is the small support structure around the agent: rules, templates, checks, and handoff notes. It does not replace judgment. It makes the work easier to inspect and resume.

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

Common values:

- `approval: "auto-safe"` means the write is narrow, sourced, and reversible.
- `approval: "needs-review"` means a human should look first.
- `confidence` can be `high`, `medium`, or `low`.
- `expiry: "daily"` means the item belongs in daily notes, not permanent memory.

## Step 3: Use A Tracker Update Proposal

For task changes, keep the shape smaller:

```json
{
  "id": "TUP-YYYYMMDD-001",
  "task_id": "TASK-001",
  "type": "task_status_update",
  "source": "User chat YYYY-MM-DD HH:MM",
  "status_change": "ACTIVE to READY_FOR_REVIEW",
  "summary": "Short summary of work ready for review.",
  "next_step": "Request human review before marking complete.",
  "evidence": ["path/or/source"],
  "approval": "needs-review",
  "review_state": "pending",
  "expected_validator_result": "pass"
}
```

The most important rule:

> Do not mark unreviewed work complete.

After review, use a separate completion update:

```json
{
  "id": "TUP-YYYYMMDD-002",
  "task_id": "TASK-001",
  "type": "task_status_update",
  "source": "Human review YYYY-MM-DD HH:MM",
  "status_change": "READY_FOR_REVIEW to COMPLETE",
  "summary": "Reviewed and accepted.",
  "next_step": "Archive or publish according to the project workflow.",
  "evidence": ["review note", "validation output"],
  "approval": "reviewed",
  "review_state": "reviewed",
  "reviewed_by": "Human reviewer",
  "review_reference": "Review note or approval message",
  "expected_validator_result": "pass"
}
```

The validator checks that a completion record includes a review trail. It cannot prove who performed the review, so do not treat `reviewed_by` as authentication.

## Step 4: Add Checkpoint/Resume Records

Use a checkpoint after interruption, compaction, delegation, or any meaningful pause.

```json
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
```

The `do_not_redo` field matters. It stops future agents from wasting time and accidentally breaking finished work.

Resume procedure:

1. Read the latest checkpoint.
2. Check whether the evidence and validation are still current.
3. Do the `next_action`.
4. Update the checkpoint before another pause or handoff.
5. Re-verify if files, dependencies, or assumptions changed.

`do_not_redo` is not a command to skip all verification. It means “do not repeat finished work unless something changed or the evidence is stale.”

## Step 5: Keep Validation Small

You do not need a big test system at first.

Start with a simple checker that confirms:

- required files exist
- example JSON is valid
- memory proposals include a source
- checkpoint records include next action and do-not-redo notes
- public package files pass a limited hygiene marker scan

Then add real examples when something goes right or wrong.

The included validator is a small starter checker, not a full security scanner. It can catch missing fields, invalid JSON, unsafe completion defaults, and a few obvious private markers. It cannot prove that a repo contains no secrets.

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
