# 1962 Lincoln Continental - Drift-Drag Couch Opener

## Context

- Game: FH6
- Car identity: ordinal `1586`
- Class: `S1 738`
- Drivetrain: RWD
- Build: drag tires, drag 4-speed, adjustable aero, drift-drag tooling.
- Purpose: laid-back sweeping drift setup for a heavy car that should step out
  without feeling like a snap trap.
- Controls: Xbox controller, simulation steering, manual for drift, ABS off,
  traction control off, stability control off.
- Status: safe opener after the 2026-06-28 evening pulls. Treat it like a tank,
  not a tin can; final knob fiddling can wait for a matched follow-up pull.

## Useful Current Snapshot

These are the known useful values from the last applied direction. Values not
listed here were not part of the final useful note for the night.

### 1. Tires

- Front: `28.0 PSI`
- Rear: `17.0 PSI`

### 2. Gearing

- Final drive: `3.40`

### 3. Alignment

- Front camber: `-2.0 deg`
- Front toe: `+0.2 deg`
- Front caster: `7.0 deg`

### 4. Antiroll Bars

- Front: `24.0`
- Rear: `22.5`

### 5. Springs

- Rear ride height: `6.3 in`

### 6. Damping

- Front rebound: `8.4`
- Front bump: `5.4`
- Rear rebound: `7.8`
- Rear bump: `3.6`

### 7. Aero

- Front: `323 lb`
- Rear: `560 lb`

### 9. Differential

- Rear acceleration: `60%`
- Rear deceleration: `0%`

## Measured Slider Ranges

Screenshots were endpoint measurements only, not installed tune values.

| Setting | Front minimum | Front maximum | Rear minimum | Rear maximum |
| --- | ---: | ---: | ---: | ---: |
| Springs | 403.8 | 2,019.0 | 403.8 | 2,019.0 lb/in |
| Ride height | 4.3 | 8.3 | 5.5 | 9.5 in |
| Downforce | 194 | 323 | 360 | 601 lb |

## Telemetry Notes

- `telemetry/20260628-220422-car-1586-s1-738-rwd-10s-fh6-telemetry.jsonl`:
  intentional slow throttle roll-in. The car did not fail during the roll-in.
  Breakaway began at `5.844 s`, `64.8 mph`, `100%` throttle, with rear slip
  ratio jumping from a pre-kick average of `0.67` to `2.44` in the kick window.
  Pre-kick front slip averaged `1.37` vs rear `0.80`, so the car was still
  resisting release before the tire cliff.
- `telemetry/20260628-221552-car-1586-s1-738-rwd-10s-fh6-telemetry.jsonl`:
  wall-slide pull. Telemetry showed full front-end input, not low input:
  moving steering lock was `95.0%`. The problem was front wash. Front combined
  slip averaged `3.17` vs rear `1.08`, understeer proxy was `94.7%`, and exit
  understeer was `96.9%`. Pre-kick was `100%` throttle, `100%` steer, front
  slip `4.18`, rear slip `0.57`, and beta only `1.83 deg`.
- Latest wall-slide kick began at `7.657 s`, `76.9 mph`, `100%` throttle,
  `100%` steer, with beta only `-1.9 deg` at the marker. Rear slip spike after
  that looked secondary to the car already being pinned at full lock and
  sliding wide.
- Contamination was low: no brake during the key windows, no handbrake until
  after the kick/slowdown, no bottoming or airborne proxy. Three minor
  smashable-hit packets appeared near `76-77 mph`, with tiny velocity loss.

## Next Useful Test

Run a matched sweeping entry with the current opener and treat the steering
like a heavy car: set the front once, feed throttle, and do not ask it to flick.
If it still washes at full lock before rotation, the next correction should
favor front authority and entry speed control before chasing more rear looseness.
