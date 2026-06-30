---
name: fh6-telemetry-analyze
description: Analyze and compare Forza Horizon 6 Data Out telemetry captures locally using the project parser instead of doing token-heavy math in chat. Use when Codex needs to inspect FH6 JSONL/CSV telemetry pulls, compare downloaded/shared tunes, fingerprint tune behavior, review launch/drift/recovery/cornering data, or explain what telemetry can and cannot reveal about tune sliders.
---

# FH6 Telemetry Analyze

## Purpose

Use local parsing first. FH6 Data Out captures do not include installed tuning
slider values, so never claim telemetry can dump a full tune. Use telemetry to
fingerprint behavior: speed, gear, throttle, brake, steering, body slip,
combined slip, slip ratio, tire temperature, suspension travel, bottoming,
airborne proxy, and launch timing.

Telemetry can still justify drivetrain direction decisions such as `FWD`,
`RWD`, and `AWD` when repeated pulls show a clear entry, sustain, recovery, or
launch pattern. Keep drivetrain conclusions separate from claims about the
current installed slider state.

## Workflow

1. Work from `C:\Users\EmpressAlae\Documents\ffh6`.
2. Read `AGENTS.md` and `TUNING.md` before making tune recommendations.
3. Confirm Xbox controller rear trigger stops are at full throw before
   diagnosing throttle, gearing, launch, drift wheelspin, or power delivery.
4. Prefer the local analyzer over manual math:

```powershell
.\tools\fh6_telemetry.ps1 analyze <capture1.jsonl> <capture2.jsonl> --baseline <baseline.jsonl>
```

5. For many captures, keep stdout quiet and write machine data under `tmp/`:

```powershell
$null = New-Item -ItemType Directory -Force -Path tmp
.\tools\fh6_telemetry.ps1 analyze telemetry\*.jsonl --baseline <baseline.jsonl> --json tmp\fh6-telemetry-analysis.json
```

6. Consume the JSON yourself. Do not ask the user to read generated files.
   Report only the translated result, with the few numbers that change the
   tuning decision.
7. Use `--full` only when the brief JSON lacks a needed field.
8. For capture identity, trust analyzer `identity_slug` and the `car` fields
   over filenames or raw `row_label`. Old captures may have been renamed or
   repaired after stale labels such as `miata-drag`.

## Delegation

Raw JSONL and long listen logs must be reduced locally, not read through main
chat. When multi-agent tools are available and the task asks for pull review,
log review, phase splitting, or breakaway timing, spawn one read-only telemetry
review agent. The review agent should run bounded parser commands, return only
compact evidence, and avoid final tune recommendations. If multi-agent tools
are unavailable, run the same parser commands locally and state that delegation
was unavailable.

Use the breakaway reducer when the question is about when a drift car finally
lets go:

```powershell
.\tools\fh6_telemetry.ps1 breakaway <capture.jsonl> --json tmp\breakaway.json
```

## Comparison Targets

For shared/top-rated tune comparison, capture the same scenario for each tune:

- Standing launch or short drag pull.
- Clean mid-smoke drift hold.
- Direction-change or recovery pull.
- Cornering/braking pull for grip tunes.

Label captures with car/tune/creator context when possible. Compare against the
current local baseline using `--baseline`; judge deltas before recommending
slider changes.

If using `telemetry\latest-fh6-capture.txt`, parse it as key/value metadata
with `ConvertFrom-StringData`. Only analyze `CapturePath` when `Status` is
`complete`; otherwise report the error, usually `NoPackets`, and ask for a
fresh capture.

## Interpretation Rules

- More rear combined slip, rear slip ratio, and rear tire temp usually means
  looser rear behavior or more throttle abuse.
- More front combined slip during steering lock points to front saturation or
  asking too much angle/speed from the front contact patch.
- More body slip with controlled rear slip can be healthy drift angle; more
  body slip with rear runaway flags over-rotation.
- A repeated "resists release, then runs away" or "kicks early, then settles
  into front push" pattern can justify trying or rejecting a drivetrain
  direction such as `FWD`, `RWD`, or `AWD`.
- Bottoming or airborne proxy means suspension/ride-height changes are more
  relevant than differential changes.
- Brake and handbrake rates matter because driver input can explain behavior
  that is not actually in the tune.
- Gear is a raw FH6 Data Out field. For the FD #117 captures, verify against
  driver context because the field appeared offset from the visible gear.

## Reporting

Keep the user-facing answer short. Do not paste raw JSON unless explicitly
asked. Say what changed relative to baseline, what it implies, and the next
single useful test or tune adjustment. If telemetry supports a drivetrain
direction change, say that explicitly. If the current installed slider state is
unknown, say so explicitly and avoid phrasing any specific diff, alignment, or
spring value as already confirmed. If full slider values are needed, ask for
tuning-menu screenshots or manual values in FH6 menu order.
