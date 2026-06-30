# FH6 Vibe Tuning

Codex-first tuning notes, telemetry helpers, and project instructions for a
Forza Horizon 6 tuning workflow.

Got Codex, a strange desire to turn a 1962 Lincoln Continental into a drift
couch, and a wish to learn without torching your context window? Come on in.

This repo is a public snapshot of the working loop: ask Codex to reason from
local tuning conventions, capture short telemetry pulls, record what changed,
and keep the results readable enough that another player can try the same
experiment without feeling like they need a lab coat.

## What is here

- `AGENTS.md` and `AGENT.md`: the project rules Codex should follow in this
  workspace.
- `TUNING.md`: the main tuning reference, menu-order conventions, measured
  baselines, and current vehicle notes.
- `tunes/`: per-car tune entries that are easier to share or revise than the
  main reference file.
- `tools/`: PowerShell and Python helpers for short FH6 telemetry captures,
  router setup, launch checks, and local analysis.
- `docs/`: telemetry schema notes, source notes, and controller-specific setup
  notes.
- `.codex/skills/`: local Codex skills that keep repeated FH6 workflows compact.

## What is intentionally not here

Raw telemetry captures, temp files, local agent scratch space, cloned upstream
tools, downloaded releases, and generated carlist asset scans are ignored. Those
are useful locally, but the public repo is meant to stay focused on Codex
interactions and reusable tuning workflow.

If someone wants to port this setup to another assistant, they can use these
files as source material and cook that adapter on their own.

## How to use it with Codex

1. Clone the repo and open it as a Codex workspace.
2. Ask Codex to read `AGENTS.md` and `TUNING.md` before giving tune values.
3. Keep tune values in FH6 menu order: Tires, Gearing, Alignment, Antiroll
   Bars, Springs, Damping, Aero, Brake, Differential.
4. Put reusable tune entries under `tunes/<vehicle-slug>/`.
5. Keep raw telemetry under `telemetry/`; it is ignored by git on purpose.

The default driving context in this project is Xbox controller, simulation
steering, automatic transmission for race, manual for drift, ABS off, traction
control off, and stability control off.

## Notes

This is an unofficial fan project and is not affiliated with Microsoft, Xbox,
Playground Games, Turn 10, or the Forza Horizon franchise.
