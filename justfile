# Beginner's Guide to Agent Harness Reliability repo tasks

default:
    just --list

# Show available repo commands.
help:
    just --list

# Open command menu.
menu:
    @if command -v justx >/dev/null 2>&1; then justx; else just --list; fi

# Validate package structure and examples.
validate:
    python3 validate-agent-harness-reliability.py .
    python3 -m py_compile validate-agent-harness-reliability.py
    rm -rf __pycache__

# Build downloadable zip package.
package:
    mkdir -p downloads
    rm -f downloads/beginners-guide-to-agent-harness-reliability-v*.zip
    zip -r downloads/beginners-guide-to-agent-harness-reliability-v0.1.0.zip . -x './.git/*' './downloads/*' './__pycache__/*'

# Quick context check for agents before editing.
agent-preflight:
    @echo "Repo: beginners-guide-to-agent-harness-reliability"
    @if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then git status --short; else echo "No git history (local draft package)."; fi
    @find . -maxdepth 2 -type f | sort

# Verification after edits.
agent-verify:
    @if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then git diff --check; else echo "No git history (local draft package); running validation only."; fi
    just validate

# Show current repo status.
agent-status:
    @if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then git status --short; git log --oneline -5; else echo "No git history (local draft package)."; fi
