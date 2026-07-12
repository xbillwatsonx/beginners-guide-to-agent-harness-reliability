# Prompt 04: Build Validator Fixtures

Copy this into your agent chat:

```text
Please create a tiny validation set for the memory and checkpoint rules.

Start with:
1. One passing memory write proposal.
2. One passing checkpoint/resume record.
3. One warning-style example where a changed file has no validation recorded.
4. One failure-style example where a task is marked complete before review.

If a validator script already exists, use it.
If no validator exists, propose a small dependency-free checker before writing code.

Do not wire this into cron, background jobs, or automatic memory writing.
```
