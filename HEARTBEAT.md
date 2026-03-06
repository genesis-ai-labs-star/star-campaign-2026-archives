# HEARTBEAT.md - Periodic Check-in

Runs every 60m.

## Every Heartbeat
- System load: `top -l 1 -n 0 -s 0 | head -5` — alert if load>8 or free mem<200MB
- **Campaign Archive Check**: Ensure `scripts/archive-results.sh` runs if significant milestones are reached.

- If nothing notable → reply `HEARTBEAT_OK`

## Evening (~22:30, last heartbeat)
1. Brief recap if notable events occurred
2. **Daily learning summary (mandatory):** write 3-8 bullets on what I learned today (mistakes, new facts, new prefs, new workflows)
3. Write/update `memory/YYYY-MM-DD.md` with: topics, decisions, preferences, lessons
4. Update `USER.md` if new preferences discovered
5. Weekly (Sunday): review daily logs → distill into `MEMORY.md`

## Rules
- Don't spam. System alerts always worth sending.
- Memory updates are silent — don't announce them.
- Track: explicit prefs, implicit patterns, corrections (most valuable signal)
- Skip: private convos, temp moods, exact message contents (summarize instead)
