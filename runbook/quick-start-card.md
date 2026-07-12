# Quick Start Card

Use this when your agent is useful but starts losing track of decisions, repeating work, or stuffing too much into long-term memory.

## The Simple Setup

Ask your agent to build three things:

1. Memory write rules.
2. Checkpoint/resume rules.
3. A few validated examples.

## Prompt Order

Copy each prompt into your agent chat in order:

1. `prompts/01-audit-current-memory.md`
2. `prompts/02-create-memory-write-rules.md`
3. `prompts/03-add-checkpoint-resume.md`
4. `prompts/04-build-validator-fixtures.md`
5. `prompts/05-review-agent-loop.md`

## What To Tell The Agent First

```text
Please use this runbook to help me make your work more reliable. Start by inspecting how you currently store memory, tasks, notes, and handoffs. Do not change files yet. First explain what you found and what small reliability layer you recommend.
```

## What Good Looks Like

- important decisions are written down
- tiny chat details do not bloat durable memory
- task status changes have a clear source
- interrupted work has a resume note
- the resume note says what not to redo
- examples can be checked with a simple validator

## Safety Boundary

Do not ask the agent to automate every memory write on day one. Start manual. Prove the examples first.
