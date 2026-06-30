# 1962 Lincoln Continental - AWD Telemetry Review

## Context

- Game: FH6
- Car identity: ordinal `1586`
- Class during this test sequence: `S1 768`
- Drivetrain under test: AWD conversion
- Purpose: compare AWD behavior against the prior RWD late-kick / rear-runaway
  signature and document what telemetry did and did not prove.
- Controls: Xbox controller, simulation steering, manual for drift, ABS off,
  traction control off, stability control off.
- Status: experimental review written from the 2026-06-29 telemetry sequence.
  Telemetry justified trying AWD, but the latest AWD pulls still settled into
  front-limited sustain rather than a comfortable held slide.

## Capture Sequence

| Capture | Configuration | Read |
| --- | --- | --- |
| `telemetry/20260629-222343-car-1586-s1-757-rwd-10s-fh6-telemetry.jsonl` | `S1 757`, RWD, 10 s | Reference pull that justified the AWD experiment. The car resisted release, then roasted itself once it finally let go. |
| `telemetry/20260629-222926-car-1586-s1-768-awd-5s-fh6-telemetry.jsonl` | `S1 768`, AWD, 5 s | Mid-run-only pull. More controlled than the RWD reference, but not launch comparable because it began already moving. |
| `telemetry/20260629-223350-car-1586-s1-768-awd-5s-fh6-telemetry.jsonl` | `S1 768`, AWD, 5 s | Standing-ish AWD check. Still front-limited; no real drift window formed. |
| `telemetry/20260629-223732-car-1586-s1-768-awd-10s-fh6-telemetry.jsonl` | `S1 768`, AWD, 10 s | Full launch and settle read. Early kick, then a clear front-led moving phase. |
| `telemetry/20260629-224423-car-1586-s1-768-awd-5s-fh6-telemetry.jsonl` | `S1 768`, AWD, 5 s | Max-pin, max-throttle church run. Earliest kick yet, but still Sunday tame after the kick window. |

## Compact Stats

| Capture | Avg mph | Max mph | Full throttle | Moving lock | Avg body slip | Front slip avg | Rear slip avg | Drift samples |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `222343` RWD 10 s | `46.95` | `71.92` | `49.0%` | `87.7%` | `13.41 deg` | `2.75` | `1.81` | `200` |
| `222926` AWD 5 s | `55.78` | `59.31` | `100.0%` | `100.0%` | `9.12 deg` | `0.85` | `0.77` | `63` |
| `223350` AWD 5 s | `53.51` | `59.37` | `100.0%` | `82.6%` | `3.95 deg` | `1.30` | `0.54` | `0` |
| `223732` AWD 10 s | `46.22` | `59.43` | `81.4%` | `89.5%` | `5.12 deg` | `1.49` | `0.80` | `67` |
| `224423` AWD 5 s | `51.21` | `58.55` | `100.0%` | `84.1%` | `4.13 deg` | `1.24` | `0.61` | `19` |

## Breakaway Findings

### RWD reference: `20260629-222343`

- Kick: `7.156 s`, `51.88 mph`, reason `power_oversteer`.
- Before kick, the car was strongly front-limited:
  - front combined slip `2.80` avg vs rear `0.57` avg
  - `front_gt_rear_pct 93.8`
- In the pre-kick second just before release:
  - front combined slip `1.39` avg vs rear `0.67` avg
  - throttle only `30.7%` avg
- After kick, the car flipped hard into rear runaway:
  - avg body slip `40.02 deg`
  - rear combined slip `5.23` avg / `8.27` p95
  - rear slip ratio `3.86` avg / `7.84` p95

This was the core reason to try AWD. The RWD signature was not just "needs
more angle"; it was "resists release, then goes binary once it finally breaks."

### AWD full read: `20260629-223732`

- Launch detected at `0.984 s`.
- Time to speed:
  - `5 mph`: `0.391 s`
  - `20 mph`: `0.828 s`
  - `30 mph`: `1.078 s`
  - `40 mph`: `1.641 s`
  - `50 mph`: `1.953 s`
- Kick: `2.500 s`, `37.57 mph`, reason `power_oversteer`, throttle `57.3%`.
- Before kick, AWD did what it was supposed to do for the experiment:
  - rear combined slip led on `81.6%` of samples
  - the car no longer needed the same late violent release as the RWD pull
- After kick, the moving phase went front-led:
  - avg body slip `4.60 deg`
  - front combined slip `1.59` avg vs rear `0.47` avg
  - `front_gt_rear_pct 100.0`

### AWD max-pin church run: `20260629-224423`

- Kick: `1.062 s`, `47.38 mph`, reason `rear_slip_dominant`, throttle `100%`.
- No brake, no handbrake, no bottoming, no airborne proxy.
- The kick itself was cleaner and earlier than the RWD reference, but it did
  not survive into a comfortable held slide:
  - kick-window body slip `5.50 deg` avg
  - after-kick body slip `4.75 deg` avg
  - after-kick front combined slip `1.46` avg vs rear `0.50` avg
  - `front_gt_rear_pct 100.0`

### AWD standing-ish check: `20260629-223350`

- Kick: `1.969 s`, `58.74 mph`, reason `body_angle`.
- No usable drift window was recorded.
- After kick, it still settled front-led:
  - front combined slip `1.52` avg vs rear `0.46` avg
  - `front_gt_rear_pct 100.0`

## Findings

1. Telemetry did justify drivetrain direction work.

   The RWD reference pull showed a split personality: front-limited before
   breakaway, then excessive rear runaway after breakaway. That is valid
   telemetry evidence for trying AWD instead of continuing to chase only rear
   diff changes on the same RWD state.

2. AWD improved onset timing and removed the worst of the binary release.

   Compared with the RWD reference, the AWD captures kicked much earlier and
   did not show the same post-kick rear slip explosion. The experiment itself
   was justified.

3. AWD still remained front-limited once the car was moving.

   The good AWD captures all settled into front-led sustain after the kick:
   `223732`, `223350`, and `224423` all ended with front combined slip greater
   than rear on `100%` of after-kick samples.

4. Therefore AWD was a valid experiment, not a proven final answer.

   The latest AWD result is better at getting loose than the earlier polite
   AWD checks, but it is still not the relaxed held-slide behavior wanted for
   this car. The telemetry verdict at the end of this sequence is "front-limited
   sustain," not "AWD solved it."

## Interpretation Limits and Chat Correction

- Telemetry can support drivetrain direction decisions such as `FWD`, `RWD`,
  and `AWD`.
- Telemetry cannot reveal the installed tuning sliders directly.
- Because no current AWD Lincoln tune note was on disk during this review, any
  statement that treated a specific installed diff value as already known was
  overconfident.
- In particular, the chat should not have treated front differential
  `0% accel / 0% decel` as confirmed unless that value had been read from the
  tuning menu, a screenshot, or an on-disk tune note.
- The clean interpretation is:
  - telemetry supported testing AWD relative to the RWD reference;
  - telemetry did not prove that AWD must stay in the car;
  - telemetry did not prove the current front diff setting;
  - recommendations that depend on present slider state must be anchored to a
    written tune note or a fresh tuning-menu read.

## Practical Read for Future Work

- If continuing AWD development, treat the problem as a sustain issue, not a
  "make it step out at all" issue.
- If returning to RWD, do it because the driver prefers the character after
  review, not because telemetry somehow exposed or hid a current slider value.
