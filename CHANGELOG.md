# Changelog

## v0.1.1 - 2026-07-12

- Changed task-update defaults from direct completion to `READY_FOR_REVIEW`.
- Added a separate reviewed completion example.
- Strengthened validator coverage for templates, starter-kit JSON, and examples.
- Added clean JSON parse errors, field quality checks, allowed values, explicit checkpoint types, and safer completion validation.
- Clarified that the public marker scan is limited hygiene checking, not secret detection.
- Added a dependency-free Python release zip builder.
- Documented Windows/Python command options and `just` shell limitations.
- Replaced internal task identifiers with generic `TASK-*` placeholders.

## v0.1.0 - 2026-07-12

- Started first public release package.
- Added beginner README, quick-start card, runbook, prompts, templates, starter kit, examples, validator, justfile, and MIT license.
- Added warning/failure examples and expected-result validation.
- Added agent editing rules for local review before any public release.
- Added missing task-update proposal template so the templates match the full runbook.
