# Prompt 02: Create Memory Write Rules

Copy this into your agent chat after the audit:

```text
Please draft simple memory write rules for this workspace.

The rules should explain:
1. What belongs in long-term memory.
2. What belongs in daily/session notes.
3. What belongs in project docs or reports.
4. What should be rejected or kept temporary.
5. When to ask me before writing durable rules.
6. How to avoid copying private or sensitive content into broad memory.

Also create a memory write proposal template based on this shape:

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

Do not edit memory yet. Show me the proposed rules first.
```
