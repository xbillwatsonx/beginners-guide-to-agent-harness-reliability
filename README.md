# Beginner's Guide to Agent Harness Reliability

`beginners-guide-to-agent-harness-reliability` helps non-technical users make their AI agents more reliable with simple rules, checklists, examples, and copy-paste prompts.

The goal is not to build a complicated software platform. The goal is to help people teach an agent to:

- write down important decisions
- avoid bloating long-term memory
- pause safely when interrupted
- resume without redoing finished work
- validate important memory and task updates before making them permanent
- keep public/private boundaries clear

This package is based on a real reliability-hardening workflow, but it is written for ordinary users who want practical setup help.

## What This Does

This runbook gives you a lightweight reliability layer for agent work:

1. Memory write rules so important things are stored in the right place.
2. Checkpoint/resume records so interrupted work can continue cleanly.
3. Simple validator fixtures so examples can be checked instead of trusted blindly.
4. Copy-paste prompts for asking your agent to audit and improve its workflow.
5. Starter templates you can adapt to your own workspace.

## What Is Included

- `runbook/agent-harness-reliability-runbook.md` - full beginner-friendly guide.
- `runbook/quick-start-card.md` - one-page starter flow.
- `AGENTS.md` - editing and release rules for agents working in this package.
- `prompts/` - copy-paste prompts for walking an agent through setup.
- `templates/` - reusable JSON templates for memory proposals, task updates, and checkpoint records.
- `starter-kit/` - small starter rules and checkpoint files.
- `examples/` - passing, warning, and failure examples for the validator.
- `validate-agent-harness-reliability.py` - dependency-free package checker.
- `CHANGELOG.md` - package history.
- `LICENSE` - MIT License.

## Quick Start

1. Open `runbook/quick-start-card.md`.
2. Copy the prompt from `prompts/01-audit-current-memory.md` into your agent chat.
3. Let the agent inspect your current memory/task setup before it changes anything.
4. Continue through the prompt files in order.
5. Ask the agent to validate this package:

```bash
python3 validate-agent-harness-reliability.py .
```

If you have `just` installed, you can also run:

```bash
just agent-verify
```

## Success Looks Like

You are done with the first setup when:

- your agent knows what belongs in long-term memory
- your agent knows what belongs in daily notes, reports, or task trackers
- important task status changes use a simple proposal shape first
- interrupted work has a checkpoint/resume record
- future agents know what not to redo
- validator examples pass
- nothing public, destructive, or sensitive is automated without review

## Safety Rule

This runbook does not ask your agent to delete files, publish content, send messages, expose credentials, or automate every memory write.

Start manual. Let the workflow prove itself. Add automation only after you trust the examples.

## License

MIT. Use it, share it, adapt it, and improve it.
