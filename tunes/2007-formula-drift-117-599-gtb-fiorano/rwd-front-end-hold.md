# 2007 Formula Drift #117 599 GTB Fiorano - RWD Front-End Hold

## Context

- Game: FH6
- Drivetrain: RWD
- Purpose: off-road drift challenge tune with the front end tuned to hold the
  car together while the rear stays lively.
- Controls: Xbox controller, Standard steering, ABS off, traction control off,
  stability control off.
- Shifting: manual, 2nd gear as compact-zone scoring gear.
- Status: field-improved after pressure and rear differential adjustment. No
  camber or toe changes applied.

## Tune

### 1. Tires

- Compound: `Offroad Race Tire Compound`
- Front: `20.5 PSI`
- Rear: `36.0 PSI`

Offroad race gives the front loose-surface bite now that AWD is no longer
pulling the nose through the slide. The revised pressures reduced rear
over-bloom while keeping the rear willing to rotate.

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

- Rear acceleration: `82%`
- Rear deceleration: `18%`

## Adjustment Cues

- If the rear lights instantly and rotates past recoverable angle, lower rear
  acceleration to `78%`.
- If it feels lazy or one-wheel-ish under throttle, raise rear acceleration to
  `86-88%`.
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

## Telemetry Review - 2026-06-27 Fresh Pull

Source: `telemetry/20260627-213253-miata-drag-10s-fh6-telemetry.jsonl`

### Summary

- Duration: `10.0 s`, `720` packets.
- Drivetrain: RWD telemetry (`DrivetrainType: 1`).
- Gear: `2` for the entire run.
- Speed: `43.1 mph` average, `55.0 mph` maximum.
- Throttle: `68.1%` average; `100%` throttle for `219` packets.
- Brake and handbrake: unused throughout the capture.
- Rear combined slip: `4.04` average, `7.83` maximum.
- Front combined slip: `1.40` average, `4.66` maximum.
- No moving samples exceeded `20` rear combined slip or `5` front combined
  slip.
- Rear tire temperature: approximately `178-278 F` during the capture.

### Comparison To Sloppy Baseline

- Rear slip average dropped from `22.1` to `4.04`.
- Rear slip maximum dropped from `40.2` to `7.83`.
- Front slip average dropped from `2.46` to `1.40`.
- Absolute body-slip angle stayed under `39 deg`; the previous run reached
  nearly `88 deg`.
- Rear tire temperature was much cooler, dropping from roughly `275-315 F` to
  `178-278 F`.

### Diagnosis

The pressure and rear differential change worked. The car is no longer
over-blooming the rear tires or cooking them through the run. The higher speed
range means the rear is now converting more throttle into drive, but the slide
state is much more controlled. Leave camber and toe unchanged for the next
test.

### Next Small Test

Hold this setup. If the car now feels too hooked and climbs speed too easily,
test only one of these:

- Rear pressure: `38.0 PSI`
- Rear differential acceleration: `86%`

Do not apply both at once.

## Telemetry Review - 2026-06-27 Launch Pull

Source: `telemetry/20260627-213940-miata-drag-10s-fh6-telemetry.jsonl`

### Summary

- Duration: `10.0 s`, `720` packets.
- Drivetrain: RWD telemetry (`DrivetrainType: 1`).
- Gear: `2` for the entire run.
- Speed: `39.4 mph` average, `53.4 mph` maximum.
- Time to speed: `5 mph` in `0.625 s`, `20 mph` in `1.734 s`, `30 mph` in
  `2.469 s`, `40 mph` in `3.281 s`, and `50 mph` in `4.734 s`.
- Throttle: `71.1%` average; `100%` throttle for `194` packets.
- Brake and handbrake: unused throughout the capture.
- Rear combined slip: `6.83` average, `32.5` maximum.
- Front combined slip: `1.26` average, `5.96` maximum.
- Rear tire temperature: approximately `132-285 F` during the capture.

### Launch Shape

The rear bloomed hard at launch, then hooked into usable drive:

- `0-1 s`: rear slip median `27.9`, speed `0.0-10.0 mph`.
- `1-2 s`: rear slip median `14.0`, speed `10.2-23.3 mph`.
- `2-3 s`: rear slip median `5.9`, speed `23.5-36.4 mph`.
- `3-6 s`: rear slip stayed mostly around `2.8-4.7` while speed climbed into
  the low `50 mph` range.

### Diagnosis

The launch read supports holding the current tune. It creates smoke immediately
without staying in runaway wheelspin, then hooks enough to build speed and
maintain rhythm. That is the desired compromise for learning this RWD setup.

### Next Small Test

No tune change from this pull. Keep gathering mid-smoke and recovery samples
before changing pressure, differential, camber, or toe again.
