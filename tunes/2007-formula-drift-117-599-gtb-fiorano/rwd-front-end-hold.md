# 2007 Formula Drift #117 599 GTB Fiorano - RWD Front-End Hold

## Context

- Game: FH6
- Drivetrain: RWD
- Purpose: off-road drift challenge tune with the front end tuned to hold the
  car together while the rear stays lively.
- Controls: Xbox controller, Standard steering, ABS off, traction control off,
  stability control off.
- Shifting: manual, 2nd gear as compact-zone scoring gear.
- Status: pending field test after full trigger throw was restored and RWD
  drift practice improved throttle confidence.

## Tune

### 1. Tires

- Compound: `Offroad Race Tire Compound`
- Front: `22.0 PSI`
- Rear: `40.0 PSI`

Offroad race gives the front loose-surface bite now that AWD is no longer
pulling the nose through the slide. The high rear pressure keeps the rear
willing to bloom.

### 2. Gearing

- Final drive: `5.00`
- 1st: `3.10`
- 2nd: `2.60`
- 3rd: `2.15`
- 4th: `1.72`
- 5th: `1.42`
- 6th: `1.18`

Keep 2nd as the compact-zone scoring gear for this test. Do not revise gearing
again until the new tire and front-end setup has been driven.

### 3. Alignment

- Front camber: `-4.5 deg`
- Rear camber: `-0.7 deg`
- Front toe: `+0.8 deg` toe-out
- Rear toe: `-0.2 deg` toe-in
- Front caster: `7.0 deg`

Backs away from maximum front camber and heavy toe-out to give the front tires
a broader dirt contact patch while keeping fast steering response.

### 4. Antiroll Bars

- Front: `5.5`
- Rear: `10.5`

### 5. Springs

- Front: `390.0 lb/in`
- Rear: `440.0 lb/in`
- Front ride height: `8.1 in`
- Rear ride height: `8.5 in`

Lowering and softening the nose helps it take a set; the higher rear keeps
rotation available without relying only on throttle violence.

### 6. Damping

- Front rebound: `4.8`
- Rear rebound: `5.6`
- Front bump: `2.3`
- Rear bump: `2.8`

### 7. Aero

- Front: `55 lb`
- Rear: `20 lb`

### 8. Brake

- Balance: `68% front`
- Pressure: `90%`

### 9. Differential

- Rear acceleration: `88%`
- Rear deceleration: `18%`

## Adjustment Cues

- If the rear lights instantly and rotates past recoverable angle, lower rear
  acceleration to `82%`.
- If it feels lazy or one-wheel-ish under throttle, raise rear acceleration to
  `94-100%`.
- If entry rotation pushes the nose wide, lower rear deceleration to `12-15%`.
- If lift-off entries feel nervous, raise rear deceleration to `20-22%`.

## Telemetry Review - 2026-06-27 Sloppy 10s Run

Source: `telemetry/20260627-212410-miata-drag-10s-fh6-telemetry.jsonl`

### Summary

- Duration: `10.0 s`, `720` packets.
- Drivetrain: RWD telemetry (`DrivetrainType: 1`).
- Gear: `2` for the entire run.
- Speed: `21.1 mph` average, `34.4 mph` maximum.
- Throttle: `72.8%` average; `100%` throttle for `280` packets.
- Brake and handbrake: unused throughout the capture.
- Steering: full or near-full lock for `504` of `563` moving samples above
  `10 mph`.
- Rear combined slip: `22.1` average, `40.2` maximum.
- Front combined slip: `2.46` average, `9.77` maximum.
- Rear tire temperature: approximately `275-315 F` during the capture.

### Diagnosis

The gearing target is working: 2nd gear stayed in a compact-zone speed window
and never exceeded approximately `34 mph`. The tire problem does not look like
the whole car needs to be slicker. The rear is over-blooming and cooking while
the front only saturates badly during high-angle/full-lock moments. That points
to rear over-rotation and steering saturation more than pure front-end grip
loss.

### Next Small Test

Keep `Offroad Race Tire Compound` if this run was already on the RWD front-end
revision. Do not move to a looser compound yet.

Change only these first:

- Front pressure: `20.5 PSI`
- Rear pressure: `36.0 PSI`
- Rear differential acceleration: `82%`

If the front still skates while the rear is controllable, then test the
secondary front-contact patch adjustment:

- Front camber: `-4.0 deg`
- Front toe: `+0.6 deg`
