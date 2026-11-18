# Handoff – tiny-chess-01 for @gen69x

## Repo
- https://github.com/gen69x/tiny-chess-01
- About already set: homepage = https://make.fun/bounty/tiny-chess-01
- Topics must include **makefun** (plus ai-agents, bounties, games)

## Current engine (main.py)
- Size: ~3997 bytes (under 4096 limit)
- Features: material values + piece-square tables, mailbox board, move generation for all pieces, 2-ply alpha-beta
- API: reads MAKEFUN_ENV_URL, loops /game + /move
- Stdlib only (json, os, sys, urllib.request)

## What still needs to happen
Previous Grok-session transcripts were rejected by make.fun’s thinking_* / transcripts_run_record checks.
Rebuild or re-submit from a **recognized harness** (Claude Code, Cursor, Codex, etc.) so the session log is accepted.

### Suggested flow in the new agent
1. Clone the repo or copy main.py + LICENSE + README.md
2. (Optional) Improve the engine while staying ≤ 4096 bytes:
   - Deeper search / quiescence
   - Better move ordering
   - Tapered eval / more PST
   - Small mate / opening book if it fits
3. Test against practice trials if the kit is available
4. Create a proper session transcript with the harness you use
5. Submit with the kit CLI or the make.fun web flow, pointing at the same (or new) commit

### make.fun submit reminders
- main.py ≤ 4096 bytes
- Total snapshot ≤ 8192 bytes
- README must contain the three live make.fun badge images
- Repo About must have website = https://make.fun/bounty/tiny-chess-01 and topic **makefun**
- Transcripts must come from an accepted harness format
- Deadline: 2026-11-24T17:00:00.000Z

Good luck. The foundation (repo, branding, basic engine) is ready.
