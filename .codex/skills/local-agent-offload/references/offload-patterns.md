# Offload Patterns

## Investigation Router

Use this decision table before spawning agents:

| Problem shape | Local work | Agent split |
| --- | --- | --- |
| Large logs | `rg`, timestamp extraction, count/group locally | one agent per log family |
| Crash or process diagnosis | process snapshot, ports, event logs, dumps | one agent on OS evidence, one on app logs |
| Unknown repo | `rg --files`, manifest discovery, test inventory | one agent per subsystem |
| Slow build/test | run smallest repro, collect versions/cache state | one agent on failure logs, one on likely code path |
| User asks for more local load | measure first, then parallelize useful sweeps | agents must return evidence, not vibes |

## Output Contract

Ask agents and scripts to return:

- `finding`: short claim
- `evidence`: path, line, timestamp, command, or exact process id
- `confidence`: high, medium, or low
- `next`: one concrete action or test

## Local Summary Files

When raw output is large, create a temporary artifact in the project:

```text
tmp/codex-local-offload/<timestamp>-<topic>.txt
```

Keep it compact:

- command run
- input files searched
- counts or top matches
- selected lines with timestamps
- unanswered questions

## Parallelism Limits

Use enough concurrency to shorten wall time without making evidence noisy:

- 2-4 parallel shell reads for ordinary repo/log work.
- 3-5 subagents for independent investigation slices.
- One writer per file area.
- Prefer longer waits on agents over frequent polling.

Stop fanning out once the remaining questions are no longer independent.
