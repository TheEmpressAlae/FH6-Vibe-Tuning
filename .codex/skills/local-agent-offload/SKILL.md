---
name: local-agent-offload
description: Use when the user asks Codex to "lock in", use more local CPU/RAM, spawn agents, parallelize an investigation, diagnose why Codex is not using local resources, or offload token-heavy reasoning into local file/log/test/build/tool work. Guides Codex to fan out independent subagents when available, run parallel local sweeps, compact evidence before summarizing, and avoid pointless synthetic CPU burn.
---

# Local Agent Offload

## Overview

Use this skill to turn broad, token-heavy investigation into concrete local work: file scans, log parsing, process snapshots, tests, builds, and focused subagent tasks. Be explicit that local CPU does not run the remote model; local resources are used only through tools, subprocesses, browser automation, builds, tests, and scripts.

## Workflow

1. Confirm the work can be parallelized. Split only independent questions, artifacts, or hypotheses.
2. Take a baseline snapshot when resource usage matters:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File <skill-dir>\scripts\local_resource_snapshot.ps1
```

3. Fan out local discovery with `multi_tool_use.parallel` for independent read commands such as `rg`, `rg --files`, `Get-ChildItem`, `git status`, log tailing, test discovery, process snapshots, and small parsers.
4. If multi-agent tools are not visible, use `tool_search` for `spawn_agent`, `wait_agent`, and `close_agent`. Spawn agents only for bounded, independent work.
5. Give every agent an evidence contract: paths to inspect, what to ignore, expected output shape, and whether it may edit files. Prefer read-only agents unless a write boundary is clear.
6. Keep local command outputs compact. Use local scripts, parsers, `Select-String`, `rg --json`, `Measure-Object`, and generated summaries instead of pasting huge logs into context.
7. Synthesize only after local commands and agents return useful evidence. Close completed agents when their results are no longer needed.

## Agent Prompts

Use this shape for subagents:

```text
You are investigating one slice only: <slice>.
Workspace: <absolute path>.
Read-only unless explicitly told otherwise.
Collect concrete evidence from files/logs/processes/tests. Prefer commands over speculation.
Return: findings, exact paths/commands used, confidence, and next action.
Do not solve adjacent slices.
```

Good slices:

- "Mine logs for exact timestamps, exit codes, and recurring signatures."
- "Inspect wrapper/config code paths and identify mutation or launch-order risks."
- "Run tests/builds and isolate the first deterministic failure."
- "Inventory docs/configs and produce a short map of relevant files."

Bad slices:

- "Figure everything out."
- "Do the same investigation as the main agent."
- "Edit shared files while another agent edits the same area."

## Local Work Patterns

Prefer useful local load:

- Broad file discovery: `rg --files`, `rg --files -g "*.log"`, `rg --json "<pattern>"`
- Log reduction: parse locally into counts, timestamps, top errors, and latest matching entries.
- Verification: run the smallest relevant test/build first, then broaden if needed.
- Runtime diagnosis: process snapshots, port ownership, recent event logs, and CPU deltas.
- Artifact creation: write compact summaries or generated reports under project `tmp/` when outputs are too large for chat.

Avoid fake load:

- Do not run CPU heaters or meaningless loops.
- Do not spawn agents for non-independent work.
- Do not claim "multi-agent" uses local CPU for model reasoning.
- Do not bury the user in raw output; report the few facts that changed the decision.

## Escalation

Use normal sandbox and approval rules. If read-only Windows diagnostics such as process, CIM, event log, or cross-directory inspection are blocked by the sandbox, rerun with escalation and state that the command is read-only.

## Reference

For more detailed routing examples and output contracts, read `references/offload-patterns.md`.
