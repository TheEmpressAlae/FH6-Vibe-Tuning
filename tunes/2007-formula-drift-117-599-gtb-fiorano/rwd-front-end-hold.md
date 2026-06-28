# 2007 Formula Drift #117 599 GTB Fiorano - RWD Front-End Hold

## Context

- Game: FH6
- Drivetrain: RWD
- Purpose: off-road drift challenge tune with the front end tuned to hold the
  car together while the rear stays lively.
- Controls: Xbox controller, Standard steering, ABS off, traction control off,
  stability control off.
- Shifting: manual, 2nd gear as compact-zone scoring gear.
- Status: current field baseline. Pressure, rear differential, and front
  contact-patch changes have all improved behavior during live drift practice.

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

- Front camber: `-4.0 deg`
- Rear camber: `-0.7 deg`
- Front toe: `+0.6 deg` toe-out
- Rear toe: `-0.2 deg` toe-in
- Front caster: `7.0 deg`

Backs away from maximum front camber and heavy toe-out to give the front tires
a broader dirt contact patch while keeping enough steering response for fast
direction changes.

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
- If a direction change still makes the front skate while the rear is
  recoverable, test front toe at `+0.5 deg`. Leave camber, pressure, and
  differential unchanged for that test.
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

## Telemetry Review - 2026-06-27 Clean Mid-Smoke Pull

Source: `telemetry/20260627-215405-miata-drag-10s-fh6-telemetry.jsonl`

### Summary

- Duration: `10.0 s`, `721` packets.
- Drivetrain: RWD telemetry (`DrivetrainType: 1`).
- Raw telemetry gear: `2` for the entire run. Per the gear mapping note, verify
  against in-game display before treating this as the literal displayed gear.
- Speed: `41.0 mph` average, `44.9 mph` maximum, `34.5 mph` minimum.
- Throttle: `45.9%` average; `100%` throttle for `46` packets; near-zero
  throttle for `162` packets.
- Brake and handbrake: unused throughout the capture.
- Rear combined slip: `4.50` average, `9.62` maximum.
- Front combined slip: `1.64` average, `5.62` maximum.
- No samples exceeded `10` rear combined slip or `8` front combined slip.
- Absolute body-slip angle stayed below `39 deg`.
- Rear tire temperature: approximately `184 F` at capture start in the raw
  sample and remained controlled in the generated summary.

### Comparison

- Compared with the fresh pull, speed was much tighter: roughly `34-45 mph`
  instead of `25-55 mph`.
- Rear slip stayed in the useful singing range rather than runaway smoke:
  `4.50` average and `9.62` maximum.
- The throttle-lift recovery pattern is visible in the telemetry: `162`
  near-zero-throttle packets without brake or handbrake use.
- The last-second overcook appears mild in the capture: at `9.469 s`, rear slip
  peaked at `9.62` with `100%` throttle, full steering, `34.7 mph`, and
  approximately `31 deg` body slip. It did not become a runaway spin inside the
  logged window.

### Diagnosis

This is the current best reference pull. The tune is producing controlled RWD
drift behavior, and the driver input pattern is improving: throttle drops are
recovering the car while the tires keep making usable slip. Understeer is not
the active problem in this capture.

### Next Small Test

Hold the tune. Do not change camber, toe, pressure, or differential from this
pull. The next useful data is another clean mid-smoke sample or a recovery
sample that intentionally captures the moment after a direction change starts
to overcook.

## Telemetry Review - 2026-06-27 Chaos Recovery Pull

Source: `telemetry/20260627-220105-miata-drag-10s-fh6-telemetry.jsonl`

### Driver Context

The run started with a lot of runway speed in 6th, then shifted down hard into
2nd and threw the car into a recovery drill. The capture includes both a
successful high-angle recovery and a later overcook.

### Summary

- Duration: `10.0 s`, `721` packets.
- Drivetrain: RWD telemetry (`DrivetrainType: 1`).
- Raw telemetry gear: starts in `6`, passes through `5`, `4`, `3`, and the
  known transient `11`, then sits in `2` from about `1.27 s` onward.
- Speed: `64.7 mph` average, `133.7 mph` maximum, `21.9 mph` minimum.
- Throttle: `41.2%` average; brake and handbrake unused throughout the
  capture.
- Body-slip beta: `-67.7 deg` minimum, `31.2 deg` maximum.
- Combined tire slip averages: front `1.89`, rear `6.28`.
- Combined tire slip peaks: front `8.0` near `6.11 s`, rear `14.3` near
  `6.73 s`.
- No bottoming or airborne proxy samples appeared in the capture.

### Recovery Shape

- Entry and shift, `0.0-1.25 s`: speed stayed `120-134 mph`; throttle was
  mostly lifted and the car had not yet built much angle.
- First recovery, `1.25-5.75 s`: speed fell from about `120 mph` to `36 mph`;
  beta reached `-67.7 deg`; throttle was near zero for `77.5%` of the phase;
  front slip averaged `2.05` with a `4.00` peak while rear slip averaged
  `6.79` with a `10.67` peak.
- Reversal and overcook, `5.75-7.75 s`: speed was only `22-36 mph`; throttle
  was full for `63.9%` of the phase; front slip peaked first at `8.0`, then
  rear slip peaked at `14.3` once full throttle and full opposite lock were
  applied.
- Final recovery and end, `7.75-10.0 s`: speed rebuilt to about `41 mph`; beta
  moved from `-34.5 deg` back through center and ended near `30 deg`.

### Diagnosis

The tune is strong enough to catch a very ugly high-speed send without brake
or handbrake help. The first recovery does not look like a rear differential
problem: the rear is smoking, but the front stays readable and the car bleeds
speed cleanly.

The first weak point appears during the low-speed direction change. The front
slip spike happens before the rear peak, which means the nose briefly asks for
more time/contact patch before the tail fully blooms. The later rear slip
spike is mostly full-throttle commitment at low speed, not a reason to calm
the rear yet.

### Field Result

The front contact-patch test was promoted after live Horizon Stadium practice.
The car behaved better while the driver explored the edge with throttle
feathering and cleaner lines, reaching about half way around the stadium while
leaving a continuous visible drift trail.

### Next Small Test

Hold this baseline. If the front still hesitates during direction changes,
try only front toe at `+0.5 deg`. If the rear starts becoming too calm or
straightening early, return front toe to `+0.6 deg` before changing the rear
differential.

## Telemetry Note - Gear Field Mapping

In the U-turn/recovery capture from
`telemetry/20260627-214740-miata-drag-10s-fh6-telemetry.jsonl`, the car was
visibly in 3rd gear on the runway while the raw telemetry reported `Gear = 2`.
For this car and capture set, read the Data Out `Gear` field as a raw
telemetry value, not the literal in-game gear label. Practical interpretation:

- Data Out `Gear = 2` matched the in-game runway 3rd gear state.
- Data Out `Gear = 3` should be treated as the next gear up from that state,
  not literal displayed 3rd.
- Data Out `Gear = 11` appeared briefly during the gear transition and should
  be treated as a transient/sentinel value until proven otherwise.

Do not tune around a capture solely because it reports `Gear = 3`; first verify
the in-game gear or driver context.
