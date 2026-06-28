# Tuning Reference

## FH6 Class Caps

- A class is capped at `700 PI`. Build A-class tunes to `A 700`, not `A 800`.

## Tune Inventory

Canonical tune notes currently live in this file. Detailed values remain under
each vehicle section in FH6 menu order.

| Vehicle / event | Recorded tune or result | Status |
| --- | --- | --- |
| 2007 Formula Drift #117 599 GTB Fiorano | Separate tune entries in `tunes/2007-formula-drift-117-599-gtb-fiorano/` | RWD front-end revision pending field test |
| Deep Forest Seasonal Speed Zone | BMW M1 shared-tune completion result | Complete |
| 1985 Toyota Sprinter Trueno GT Apex | B 600 Deep Forest lightweight baseline; S1 AWD drift package | B 600 unsuccessful; S1 drift awaiting field test |
| 1982 Porsche 911 Turbo 3.3 | B 600 Deep Forest baseline | Field tested; unsuccessful |
| 1982 DeLorean DMC-12 | S1 street baseline; planned A-class revision | S1 baseline recorded; A-class pending |
| 1984 Peugeot 205 Turbo 16 | Stable skill-chain baseline and powered-landing guide | Field-validated live baseline |
| 1977 Ford #5 Escort RS1800 MkII | S1 skill-chain baseline and tabletop nose-heavy revision | v1 applied; v2 next test |

## 2007 Formula Drift #117 599 GTB Fiorano

Purpose: FH6 off-road challenge-score drift baseline for Xbox controller,
Standard steering, no ABS, traction control, or stability control. This is a
drift build, so manual shifting is allowed and recommended.

Build context: the AWD snow version helped while learning the car, but full
trigger throw and RWD practice made rear-drive more fun and usable. Current
test direction is RWD with a front-end confidence tune: more front dirt bite,
less nose wash, and a rear diff that is still lively without being binary.
Keep the throaty V12 character unless a later class target requires a swap.

### Tune Entry Files

- [RWD front-end hold](tunes/2007-formula-drift-117-599-gtb-fiorano/rwd-front-end-hold.md)
  is the current next field test.
- [AWD snow 2nd-gear](tunes/2007-formula-drift-117-599-gtb-fiorano/awd-snow-2nd-gear.md)
  is the field-improved learning baseline.
- [AWD rally 4.10 reference](tunes/2007-formula-drift-117-599-gtb-fiorano/awd-rally-4-10-reference.md)
  is the archived too-grippy reference.

### Behemoth RWD Front-End Hold Revision

**Status:** Next field test after full trigger throw was restored and RWD drift
practice improved throttle confidence.

#### 1. Tires

- Compound: `Offroad Race Tire Compound`
- Front: `22.0 PSI`
- Rear: `40.0 PSI`

Offroad race is chosen over snow for the RWD revision because the front needs
loose-surface bite now that AWD is no longer pulling the nose through the
slide. The high rear pressure keeps the rear willing to bloom.

#### 2. Gearing

- Final drive: `5.00`
- 1st: `3.10`
- 2nd: `2.60`
- 3rd: `2.15`
- 4th: `1.72`
- 5th: `1.42`
- 6th: `1.18`

Keep second as the compact-zone scoring gear for this test. Do not revise
gearing again until the new tire and front-end setup has been driven.

#### 3. Alignment

- Front camber: `-4.5 deg`
- Rear camber: `-0.7 deg`
- Front toe: `+0.8 deg` (toe-out)
- Rear toe: `-0.2 deg` (toe-in)
- Front caster: `7.0 deg`

This backs away from maximum front camber and heavy toe-out to give the front
tires a broader dirt contact patch while keeping fast steering response.

#### 4. Antiroll Bars

- Front: `5.5`
- Rear: `10.5`

#### 5. Springs

- Front: `390.0 lb/in`
- Rear: `440.0 lb/in`
- Front ride height: `8.1 in`
- Rear ride height: `8.5 in`

Lowering and softening the nose helps it take a set; the higher rear keeps
rotation available without relying only on throttle violence.

#### 6. Damping

- Front rebound: `4.8`
- Rear rebound: `5.6`
- Front bump: `2.3`
- Rear bump: `2.8`

#### 7. Aero

- Front: `55 lb`
- Rear: `20 lb`

#### 8. Brake

- Balance: `68% front`
- Pressure: `90%`

#### 9. Differential

- Rear acceleration: `88%`
- Rear deceleration: `18%`

If the rear lights instantly and rotates past recoverable angle, lower rear
acceleration to `82%`. If it feels lazy or one-wheel-ish under throttle, raise
rear acceleration to `94-100%`. If entry rotation pushes the nose wide, lower
rear deceleration to `12-15%`; if lift-off entries feel nervous, raise it to
`20-22%`.

### Behemoth AWD Dirt Drift Baseline

**Status:** Hold for driver acclimation. First snow/5.00-final test produced a
marked improvement and advanced the drift challenge by one star. Later review
found the Xbox controller throttle stop was accidentally set to the middle
`50%` trigger-throw setting; full trigger throw is now restored and greatly
improved control.

#### 1. Tires

- Compound: `Snow Tire Compound`
- Front: `24.0 PSI`
- Rear: `42.0 PSI`

Snow is the next test because it loosens the car more than offroad race without
adding rally/offroad tire bite. Avoid semi-slick, Horizon semi-slick, slick,
and drag compounds for this dirt drift target.

#### 2. Gearing

- Final drive: `5.00`
- 1st: `3.10`
- 2nd: `2.60`
- 3rd: `2.15`
- 4th: `1.72`
- 5th: `1.42`
- 6th: `1.18`

Use second as the main scoring gear for tight dirt drift zones. Third is now
an exit or recovery gear, not the target. If second still carries too much road
speed before the tires bloom, raise final drive to `5.25`. If second is
instantly pinned with no throttle control, lower final drive to `4.75`.

#### 3. Alignment

- Front camber: `-5.0 deg`
- Rear camber: `-1.0 deg`
- Front toe: `+1.2 deg` (toe-out)
- Rear toe: `-0.1 deg` (toe-in)
- Front caster: `7.0 deg`

#### 4. Antiroll Bars

- Front: `7.5`
- Rear: `9.5`

#### 5. Springs

- Front: `440.0 lb/in`
- Rear: `420.0 lb/in`
- Front ride height: `8.5 in`
- Rear ride height: `8.2 in`

This keeps the car off the bump stops on loose surfaces while preserving a low
enough center of gravity for drift transitions.

#### 6. Damping

- Front rebound: `5.4`
- Rear rebound: `5.0`
- Front bump: `2.7`
- Rear bump: `2.5`

#### 7. Aero

- Front: `55 lb`
- Rear: `20 lb`

#### 8. Brake

- Balance: `70% front`
- Pressure: `90%`

#### 9. Differential

- Front acceleration: `12%`
- Front deceleration: `0%`
- Rear acceleration: `100%`
- Rear deceleration: `8%`
- Center balance: `90% rear`

Field note: the `3.75` final-drive version was too tall for the desired
low-speed dirt scoring rhythm and required second gear. Later revisions made
second gear the intentional scoring gear for compact dirt sections.

Field note: the rally-tire version still gained speed too quickly in third and
held the tires instead of staying in a low-speed scoring slide. A street tire
compound was mistakenly suggested, but this car does not offer one. The next
revision uses snow compound, high rear pressure, less front acceleration lock,
and a more rearward center split.

Field note: the `4.10` gearing still let third climb to approximately `60 mph`
on a compact dirt section. The next revision targets second gear as the
scoring gear and uses a `5.00` final drive so the rear tires bloom before the
car builds road speed.

Field note: after soaking this tune, the Xbox controller's rear throttle-stop
switch was found in the middle `50%` trigger-throw setting instead of the top
full-throw setting. This physically limited how deeply the trigger could be
depressed, reducing throttle modulation travel and contributing to earlier
tire-bloom and drivability symptoms. Re-test future refinements only with full
trigger throw enabled.

If the car still straightens under throttle, lower front acceleration to
`8-10%` or move center balance to `93% rear`. If the tail becomes too loose on
dirt, raise front acceleration to `16-20%` before lowering center balance back
toward `85% rear`.

### Measured Slider Ranges

| Setting | Front minimum | Front maximum | Rear minimum | Rear maximum |
| --- | ---: | ---: | ---: | ---: |
| Springs | 285.0 | 1,662.0 | 253.5 | 1,662.0 lb/in |
| Ride height | 7.7 | 9.6 | 6.7 | 8.7 in |
| Downforce | 18 | 55 | 20 | 88 lb |

### Tire Compound Options

Measured from screenshots with the AWD build.

| Compound | Relative note | Class shown | Handling | Accel | Braking | Offroad |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Stock Tire Compound (Drift) | Grip `+0.06` | S2 892 | 5.3 | 8.9 | 6.3 | 4.3 |
| Semi-Slick Race Tire Compound | Grip `+0.11` | R 907 | 5.5 | 10.0 | 6.6 | 4.2 |
| Horizon Semi-Slick Race Tire Compound | Grip `+0.11` | R 907 | 5.5 | 10.0 | 6.6 | 4.2 |
| Slick Race Tire Compound | Grip `+0.15` | R 920 | 5.6 | 10.0 | 7.5 | 4.1 |
| Rally Tire Compound | Installed reference | S2 879 | 5.7 | 9.5 | 5.7 | 5.4 |
| Offroad Race Tire Compound | Grip `-0.08` | S2 859 | 5.5 | 9.2 | 5.8 | 5.8 |
| Snow Tire Compound | Grip `-0.11` | S2 858 | 5.1 | 9.0 | 6.0 | 4.2 |
| Drag Tire Compound | Grip `-0.55` | S2 844 | 4.7 | 10.0 | 6.6 | 3.7 |

### AWD Rally Gearing Reference

- Captured at `S2 879` with the `4.10` final-drive gearing.
- Braking distance: `87.7 ft` from 60-0 mph and `223.7 ft` from 100-0 mph.
- Lateral Gs: `1.22` at 60 mph and `1.25` at 120 mph.
- Acceleration and speed: `1.924 s` 0-60, `3.303 s` 0-100, and `161.3 mph`
  top speed.
- Miscellaneous: `0.51` mechanical balance, `0.47` aero balance, and `0.772`
  aero efficiency.

### AWD Snow 2nd-Gear Reference

- Captured at `S2 858` with snow tires and the `5.00` final-drive gearing.
- Field result: first run was a marked improvement and advanced the challenge
  by one star. Hold this setup until the driver has more seat time with the
  car and tune. Later controller review found prior runs were affected by a
  `50%` trigger-throw setting; full trigger throw is now restored.
- Braking distance: `110.2 ft` from 60-0 mph and `278.9 ft` from 100-0 mph.
- Lateral Gs: `1.05` at 60 mph and `1.08` at 120 mph.
- Acceleration and speed: `2.301 s` 0-60, `3.897 s` 0-100, and `134.5 mph`
  top speed.
- Miscellaneous: `0.52` mechanical balance, `0.47` aero balance, and `0.772`
  aero efficiency.

## Deep Forest Seasonal Speed Zone Result

**Status:** Complete.

- Successful car: BMW M1, eligible `B 600` 1980s build.
- Tune source: shared tune whose description explicitly referenced the
  challenge; exact settings were not exposed for documentation.
- Result: three stars and seasonal challenge completion.
- The 1982 Porsche 911 Turbo 3.3 and 1985 Toyota Sprinter Trueno GT Apex
  experimental tunes did not reach the required `95.0 mph` average.

## 1985 Toyota Sprinter Trueno GT Apex

Purpose: lightweight `B 600` Deep Forest seasonal Speed Zone build for
automatic transmission, Xbox controller, Standard steering, and no ABS,
traction control, or stability control.

Build context: maximum practical weight reduction, stock engine architecture
with the available power upgrades, sport tires, adjustable front and rear
aero, and a six-speed transmission.

### Deep Forest Lightweight Baseline

**Status:** Field tested; unsuccessful for the `95.0 mph` seasonal target.

#### 1. Tires

- Front: `24.5 PSI`
- Rear: `24.0 PSI`

#### 2. Gearing

- Final drive: `4.10`
- 1st: `3.66`
- 2nd: `2.64`
- 3rd: `1.90`
- 4th: `1.37`
- 5th: `0.99`
- 6th: `0.71`

The first and sixth effective ratios remain close to the measured baseline,
preserving launch and top-speed headroom. Second through fifth are shorter
and more evenly spaced to keep the naturally aspirated engine high in its
power band from the `52 mph` hairpin through the 100 mph recovery range.

#### 3. Alignment

- Front camber: `-1.2 deg`
- Rear camber: `-0.8 deg`
- Front toe: `0.0 deg`
- Rear toe: `-0.1 deg` (toe-in)
- Front caster: `6.5 deg`

#### 4. Antiroll Bars

- Front: `10.2`
- Rear: `24.0`

This split produces the measured `0.56` mechanical balance. Treat the readout
as a starting point rather than an absolute target: if the rear snaps or the
front rolls too slowly into direction changes, raise the front bar to `12.0`
and accept the lower displayed balance.

#### 5. Springs

- Front: `205.0 lb/in`
- Rear: `242.0 lb/in`
- Front ride height: `7.4 in`
- Rear ride height: `7.6 in`

#### 6. Damping

- Front rebound: `6.8`
- Rear rebound: `7.2`
- Front bump: `2.7`
- Rear bump: `2.9`

#### 7. Aero

- Front: `95 lb`
- Rear: `180 lb`

Maximum aero reduced the displayed top speed from `135.9 mph` to `128.8 mph`
and worsened the 0-100 estimate from `14.603 s` to `15.043 s`, while adding
only `0.01 g` at 60 mph. The lower setting retains useful stability without
paying the full acceleration penalty.

#### 8. Brake

- Balance: `50% front`
- Pressure: `110%`

#### 9. Differential

- Rear acceleration: `55%`
- Rear deceleration: `10%`

### Measured Slider Ranges

| Setting | Front minimum | Front maximum | Rear minimum | Rear maximum |
| --- | ---: | ---: | ---: | ---: |
| Springs | 86.8 | 433.9 | 145.8 | 433.9 lb/in |
| Ride height | 6.6 | 8.4 | 6.6 | 8.4 in |
| Downforce | 78 | 130 | 158 | 263 lb |

### Measured Build Baseline

- Final drive: `3.63`
- Gears: `4.14 / 2.67 / 1.82 / 1.33 / 1.00 / 0.80`
- Full-aero performance: `6.440 s` 0-60, `15.043 s` 0-100,
  `128.8 mph` top speed.
- Minimum-aero performance: `6.420 s` 0-60, `14.603 s` 0-100,
  `135.9 mph` top speed.
- Starting mechanical balance: approximately `0.49-0.50`.
- Applied `v1` panel: `6.460 s` 0-60, `14.750 s` 0-100,
  `133.5 mph` top speed, `0.54` mechanical balance, and `0.797` aero
  efficiency.
- `v1.2` uses `10.2` front and `24.0` rear antiroll stiffness, producing a
  measured `0.56` mechanical balance.

### Validation Run

- Enter the first gate above `100 mph`.
- Carry at least `60 mph` through the tightest corner.
- Recover above `85 mph` before the following bend.
- Exit above `120 mph`.
- Pass condition: seasonal result of `95.0 mph` or higher.
- If the rear spins under power, reduce differential acceleration to `50%`.
- If the engine drops below its useful rev range after the hairpin, raise
  second gear to `2.70` before changing the final drive.

### S1 AWD Drift Package

**Status:** Initial baseline; awaiting field test.

Purpose: casual AWD drift package for the `S1 794` build, Xbox controller,
Standard steering, no assists, and manual shifting during drifting. The AWD
system is strongly rear biased; light front locking is retained to pull the
nose through a slide without making the car straighten under throttle.

#### 1. Tires

- Front: `28.0 PSI`
- Rear: `32.0 PSI`

#### 2. Gearing

- Final drive: `3.40`
- 1st: `4.15`
- 2nd: `3.01`
- 3rd: `2.31`
- 4th: `1.82`
- 5th: `1.47`
- 6th: `1.24`

Hold third for medium-speed drifting and fourth for faster sweepers. If third
hits the limiter through the entire slide, lower the final drive toward
`3.25`. If the engine cannot climb through third while the tires are spinning,
raise it toward `3.55`.

#### 3. Alignment

- Front camber: `-4.0 deg`
- Rear camber: `-1.0 deg`
- Front toe: `+0.5 deg` (toe-out)
- Rear toe: `-0.1 deg` (toe-in)
- Front caster: `7.0 deg`

#### 4. Antiroll Bars

- Front: `8.0`
- Rear: `12.0`

#### 5. Springs

- Front: `400.0 lb/in` (or nearest selectable value)
- Rear: `400.0 lb/in` (or nearest selectable value)
- Front ride height: `5.5 in`
- Rear ride height: `5.7 in`

The slight rear rake helps turn-in while leaving compression room above the
`5.3 in` minimum.

#### 6. Damping

- Front rebound: `6.0`
- Rear rebound: `5.5`
- Front bump: `3.0`
- Rear bump: `2.8`

#### 7. Aero

- Front: `130 lb`
- Rear: `158 lb`

#### 8. Brake

- Balance: `70% front`
- Pressure: `90%`

#### 9. Differential

- Front acceleration: `15%`
- Front deceleration: `0%`
- Rear acceleration: `100%`
- Rear deceleration: `10%`
- Center balance: `85% rear`

### Measured S1 Drift Slider Ranges

| Setting | Front minimum | Front maximum | Rear minimum | Rear maximum |
| --- | ---: | ---: | ---: | ---: |
| Springs | 203.1 | 1015.4 | 203.1 | 1015.4 lb/in |
| Ride height | 5.3 | 7.5 | 5.3 | 7.5 in |
| Downforce | 78 | 130 | 158 | 263 lb |

### First Drift Test

- Hold third gear and initiate with a throttle lift or brief handbrake input.
- Feed the throttle back in and let the front axle pull the nose toward the
  exit; avoid full steering lock unless the car is close to spinning.
- If it straightens under power, reduce front acceleration to `10%`, then move
  center balance to `90% rear` if needed.
- If the nose will not recover from angle, raise front acceleration to `20%`.
- If transitions snap too quickly, lower the rear antiroll bar to `10.0`.
- If the rear feels planted and will not rotate, raise rear pressure to
  `34.0 PSI` before changing suspension values.

## 1982 Porsche 911 Turbo 3.3

Purpose: `B 600` Deep Forest seasonal Speed Zone tune for automatic
transmission, Xbox controller, Standard steering, and no ABS, traction
control, or stability control.

### Deep Forest B-Class Baseline

**Status:** Field tested; unsuccessful for the `95.0 mph` seasonal target.

The seasonal challenge requires a `95.0 mph` average in a `B 600` car from
the 1980s. The 1982 Porsche is eligible. The reviewed run averaged
`86.52 mph`; speed fell to approximately `52 mph` in the hairpin before the
car recovered to approximately `135 mph` at the exit. This revision favors
rough-surface turn-in, controlled rear rotation, and boost recovery without
sacrificing the required exit speed.

#### 1. Tires

- Front: `24.5 PSI`
- Rear: `24.0 PSI`

These pressures assume the current stock, street, or rally-class compound.

#### 2. Gearing

- Final drive: `3.53`
- 1st: `3.80`
- 2nd: `2.85`
- 3rd: `2.25`
- 4th: `1.85`
- 5th: `1.60`
- 6th: `1.48`
- 7th: `1.39`
- 8th: `1.32`
- 9th: `1.27`
- 10th: `1.22`

The 10-speed transmission at its `6.10` final-drive endpoint estimated
`130.0 mph`, but its `4.756 s` 0-60 and `12.182 s` 0-100 times were slower
than the six-speed baseline (`4.521 s` and `11.804 s`). The endpoint is too
short and spends acceleration on unnecessary shifts.

The nearest selectable final drive, `3.53`, and the `1.22` tenth gear produce
a `4.31` effective top ratio and an estimated `128.9 mph` ceiling. The revised
spacing restored the six-speed's `4.521 s` 0-60 estimate, while the 10-speed
0-100 estimate remained `12.182 s`. Second gear is placed for the `52-55 mph`
hairpin exit; third through fifth keep the engine in boost while recovering
toward 100 mph. Sixth through tenth close progressively so each high-speed
shift drops fewer revs.

#### 3. Alignment

- Front camber: `-1.3 deg`
- Rear camber: `-0.9 deg`
- Front toe: `0.0 deg`
- Rear toe: `-0.1 deg` (toe-in)
- Front caster: `6.5 deg`

#### 4. Antiroll Bars

- Front: `24.0`
- Rear: `20.0`

Target a mechanical-balance reading between `0.58` and `0.62`. Preserve the
four-point front-to-rear split if both values need to move to reach it.

#### 5. Springs

- Front: `360.0 lb/in`
- Rear: `535.0 lb/in`
- Front ride height: `8.1 in`
- Rear ride height: `7.9 in`

The spring rates sit near one-third of each measured adjustment range. The
ride heights retain dirt-road travel while keeping the chassis low enough to
respond during the hairpin transition.

#### 6. Damping

- Front rebound: `8.0`
- Rear rebound: `8.8`
- Front bump: `3.2`
- Rear bump: `3.5`

#### 7. Aero

- Front: `Unchanged`
- Rear: `Unchanged`

#### 8. Brake

- Balance: `48% front`
- Pressure: `110%`

#### 9. Differential

- Rear acceleration: `52%`
- Rear deceleration: `12%`

### Measured Slider Ranges

| Setting | Front minimum | Front maximum | Rear minimum | Rear maximum |
| --- | ---: | ---: | ---: | ---: |
| Springs | 153.3 | 766.6 | 412.4 | 766.6 lb/in |
| Ride height | 7.6 | 9.0 | 7.3 | 8.7 in |

### Validation Run

Use the same direction as the reviewed run and begin far enough back to enter
the first gate above `100 mph`.

- Hairpin target: hold second near the `52-55 mph` apex, then shift to third
  under boost and recover above `60 mph` immediately after the apex.
- Exit target: at least `125 mph` without reaching the limiter.
- Pass condition: seasonal result of `95.0 mph` or higher.
- If second gear reaches the limiter before the apex, reduce second to `2.80`.
  If the engine falls out of boost, raise second to `2.90`.
- Judge the 10-speed by the timed zone's `52-85 mph` recovery and final
  average, not the standing-start 0-100 estimate. Keep it only if the run
  improves on `86.52 mph`; restore the six-speed if rolling recovery does not
  improve.
- If the rear rotates before steering input, raise rear differential
  deceleration from `12%` to `15%` before changing the suspension.

## 1982 DeLorean DMC-12

Purpose: AWD street-racing baseline for automatic transmission, Xbox
controller, Standard steering, and no ABS, traction control, or stability
control.

### S1 Street Baseline

**Status:** Configured baseline, pending road validation.

#### 1. Tires

- Front: `28.0 PSI`
- Rear: `28.5 PSI`

#### 2. Gearing

- Final drive: `2.93`
- 1st: `4.15`
- 2nd: `3.01`
- 3rd: `2.31`
- 4th: `1.82`
- 5th: `1.53`
- 6th: `1.38`

The tuning panel estimates `160.8 mph`, `2.529 s` from 0-60 mph, and
`6.950 s` from 0-100 mph. Fifth is expected to be the effective top-speed
gear; sixth acts as overdrive.

#### 3. Alignment

- Front camber: `-1.4 deg`
- Rear camber: `-1.0 deg`
- Front toe: `0.0 deg`
- Rear toe: `-0.1 deg` (toe-in)
- Front caster: `6.5 deg`

#### 4. Antiroll Bars

- Front: `28.0`
- Rear: `38.0`

#### 5. Springs

- Front: `650.0 lb/in`
- Rear: `760.0 lb/in`
- Front ride height: `5.7 in`
- Rear ride height: `5.9 in`

#### 6. Damping

- Front rebound: `11.0`
- Rear rebound: `12.2`
- Front bump: `4.5`
- Rear bump: `5.0`

#### 7. Aero

- Front: `69 lb`
- Rear: `320 lb`

#### 8. Brake

- Balance: `52% front`
- Pressure: `110%`

#### 9. Differential

- Front acceleration: `40%`
- Front deceleration: `10%`
- Rear acceleration: `60%`
- Rear deceleration: `15%`
- Center balance: `65% rear`

### Measured Slider Ranges

These are endpoint measurements only, not installed tune values.

| Setting | Minimum | Maximum |
| --- | ---: | ---: |
| Final drive | 2.20 | 6.10 |
| Springs, front/rear | 285.0 | 1,425.2 lb/in |
| Ride height, front/rear | 5.1 | 7.1 in |
| Front downforce | 58 | 69 lb |
| Rear downforce | 262 | 437 lb |

### Planned A-Class Revision

- Target `A 700` exactly.
- Preserve adjustable suspension, antiroll bars, transmission, and
  differential where the PI budget permits.
- Remove power upgrades first, then retune after the final parts and slider
  ranges are known.

## 1984 Peugeot 205 Turbo 16

Purpose: stable, playful skill-chain build using the car's 9x skill multiplier.
Automatic transmission and Xbox controller.

## Vehicle Eligibility Guardrail

- A 9x skill multiplier is a vehicle-specific Car Mastery perk. Upgrades and
  tuning cannot add it to a car whose mastery tree does not contain it.
- Do not substitute the 2024 Ram 1500 TRX for this build. Its June 11-18, 2026
  prominence comes from the `Guts. Glory. Ram.` weekly challenge, not a
  verified 9x mastery perk.
- The 1984 Peugeot 205 Turbo 16 is independently documented as a 9x-capable
  car, so it remains the vehicle for this skill-chain tune.
- Other community-verified 9x choices include the 1974 Lancia Stratos, 1998
  Subaru Impreza 22B-STi, Welcome Pack Mitsubishi Lancer Evolution, and 1977
  Ford Escort RS1800 #5.

Sources checked 2026-06-17:

- <https://forums.forza.net/t/general-fh6-tips/829138>
- <https://forums.forza.net/t/fh6-festival-playlist-events-and-rewards-june-11-18-series-01-week-4/834308>

## Required Output Order

Always present tuning values in the same left-to-right order as the in-game
menu. Do not omit a tab; mark it `Unchanged` or `Pending review` when no new
values are available.

1. Tires
2. Gearing
3. Alignment
4. Antiroll Bars
5. Springs
6. Damping
7. Aero
8. Brake
9. Differential

## Screenshot Reading Convention

- The black menu tab identifies the active tuning screen.
- The lime underline confirms the same active tab.
- The outlined row is the currently selected slider.
- Screenshots taken with sliders at an endpoint measure static minimum or
  maximum values only; they do not represent the installed tune.
- When documenting a range, label the screenshot as `Minimum` or `Maximum`.
- A single image may document multiple sliders when their endpoint values are
  visible and unambiguous.

### Static Slider Ranges

| Setting | Front / minimum | Rear / maximum | Increment / unit |
| --- | ---: | ---: | --- |
| Tire pressure | 15.0 | 55.0 | 0.5 PSI |
| Final drive | 2.20 | 6.10 | Ratio |
| Individual gear ratio | 0.48 | 6.00 | 0.01 ratio |
| Camber, front/rear | -5.0 | 5.0 | 0.1 deg |
| Toe, front/rear | -5.0 | 5.0 | 0.1 deg |
| Front caster | 1.0 | 7.0 | 0.1 deg |
| Antiroll stiffness, front/rear | 1.0 | 65.0 | 0.1 |
| Springs, front | 246.0 | 1,230.0 | lb/in |
| Springs, rear | 246.0 | 1,230.0 | lb/in |
| Ride height, front | 6.2 | 9.1 | in |
| Ride height, rear | 7.0 | 9.8 | in |
| Rebound stiffness, front | 1.0 | 20.0 | 0.1 |
| Rebound stiffness, rear | 1.0 | 20.0 | 0.1 |
| Bump stiffness, front | 1.0 | 20.0 | 0.1 |
| Bump stiffness, rear | 1.0 | 20.0 | 0.1 |
| Downforce, front | 102 | 170 | lb |
| Downforce, rear | 212 | 379 | lb |
| Brake balance | 0 | 100 | 1% |
| Brake pressure | 0 | 200 | 1% |
| Differential settings | 0 | 100 | 1% |

The two numeric columns are the slider minimum and maximum. Front/rear
settings share a range unless the row is specifically a ride-height or
downforce row.

Alignment, caster, antiroll, damping, brake, differential, and gearing ranges
are standard FH6 tuning ranges. Spring, ride-height, and downforce ranges are
specific to this car and its installed parts.

### Measurement Context

- Final drive was `4.39` when the performance panel was captured.
- The performance panel showed 154.6 mph top speed and 0.56 mechanical
  balance at that moment.
- Screenshots with sliders at opposite extremes exist only to expose their
  limits. They are not the installed tune.
- The damping screenshot values are also review positions, not installed
  settings.
- Web cross-check: the FH6 ForzaFire builder exposes the standard tuning
  ranges, and its published Peugeot dirt tune uses `22.0` front and `18.0`
  rear antiroll stiffness:
  <https://www.forzafire.com/best-all-around-cars/1984-peugeot-205-turbo-16-14022>

### Build Priority

1. Protect the skill chain through stable landings and predictable rotation.
2. Keep enough suspension travel for playful traversal over small obstacles.
3. Favor a loud, mean engine note over leaderboard optimization.

### Stable Skill-Chain Baseline

**Status:** Field-validated live baseline (`v4`, 2026-06-17)

#### 1. Tires

- Front: `19.0 PSI`
- Rear: `17.5 PSI`

#### 2. Gearing

- Final drive: `4.39`
- Individual gears: `Unchanged`

#### 3. Alignment

- Front camber: `-1.3 deg`
- Rear camber: `-0.8 deg`
- Front toe: `0.0 deg`
- Rear toe: `-0.1 deg` (toe-in)
- Front caster: `5.5 deg`

#### 4. Antiroll Bars

- Front: `22.0`
- Rear: `18.0`

#### 5. Springs

- Front: `360 lb/in`
- Rear: `390 lb/in`
- Front ride height: `8.4 in`
- Rear ride height: `9.0 in`

#### 6. Damping

- Front rebound: `8.0`
- Rear rebound: `8.6`
- Front bump: `3.2`
- Rear bump: `3.4`

#### 7. Aero

- Front: `160 lb`
- Rear: `379 lb`

#### 8. Brake

- Balance: `55% front`
- Pressure: `110%`

#### 9. Differential

- Front acceleration: `40%`
- Front deceleration: `10%`
- Rear acceleration: `55%`
- Rear deceleration: `20%`
- Center balance: `65% rear`

If the car bounces twice after landing, add `0.5` to both rebound values. If
it bottoms out, add `0.3` to both bump values.

### Live Revision Rule

Change one setting group per test run. Record the observed problem before
changing a value, then promote the revision only when it improves stability
without making the car less fun. Skill-chain loss takes priority over speed or
score improvements.

### Powered-Landing Pull Guide

Use this guide when an AWD car lands with one front tire before the other.

**Symptom:** The front tires grip on landing, but the car digs toward the side
that compresses last while power is applied.

**Diagnosis:** Front differential acceleration lock is too high. The second
front tire reaches the ground with a different speed and load, then the locked
front axle converts that mismatch into steering pull.

**Direct adjustment:**

- Set front differential acceleration near `40%`.
- Use `35-45%` as the practical correction range.
- Change in `5%` steps only when refining an already stable result.
- Leave front deceleration, alignment, springs, and damping unchanged for this
  symptom.

**Validation test:** Intentionally land under steady power with approximately
`3-6%` left or right roll. Test both directions.

**Pass condition:** Both front tires grip without digging in, pulling the
steering, or changing the intended heading.

**If it still pulls:** Move center balance `5%` farther rearward before changing
suspension. If front drive becomes weak or a front tire spins freely, add `5%`
front acceleration lock back.

## 1977 Ford #5 Escort RS1800 MkII

Purpose: aggressive FH6 open-world skill-chain build for Xbox controller,
Standard steering, automatic transmission, ABS off, traction control off, and
stability control off.

### Car Mastery Skill Modifiers

Verified from user readout on 2026-06-25:

- `+15%` Drift skills
- `+10%` Wreckage skills
- `+15%` Sideswipe skills
- `+15%` Airborne Pass skills
- `+15%` Crash Landing skills
- `+20%` Link skills
- `+20%` Combo skills
- `2.5x` skill multiplier build speed
- `9x` skill multiplier cap

### Measured Slider Ranges

Screenshots were endpoint measurements only, not installed tune values.

| Setting | Front minimum | Front maximum | Rear minimum | Rear maximum |
| --- | ---: | ---: | ---: | ---: |
| Springs | 130.3 | 651.5 | 156.4 | 651.5 lb/in |
| Ride height | 10.0 | 12.5 | 10.2 | 12.7 in |

### S1 Skill-Chain Baseline

**Status:** Applied baseline (`v1`, 2026-06-25). Replaces the short gearing
test that showed `95.8 mph` top speed, `0.51` mechanical balance, and `0.824`
aero efficiency.

#### 1. Tires

- Front: `20.0 PSI`
- Rear: `19.0 PSI`

#### 2. Gearing

- Final drive: `3.45`
- 1st: `3.60`
- 2nd: `2.55`
- 3rd: `1.95`
- 4th: `1.55`
- 5th: `1.25`
- 6th: `1.05`

#### 3. Alignment

- Front camber: `-1.2 deg`
- Rear camber: `-0.8 deg`
- Front toe: `0.0 deg`
- Rear toe: `-0.1 deg` (toe-in)
- Front caster: `5.4 deg`

#### 4. Antiroll Bars

- Front: `18.0`
- Rear: `20.0`

#### 5. Springs

- Front: `310.0 lb/in`
- Rear: `330.0 lb/in`
- Front ride height: `11.8 in`
- Rear ride height: `12.1 in`

#### 6. Damping

- Front rebound: `6.4`
- Rear rebound: `6.8`
- Front bump: `2.6`
- Rear bump: `2.8`

#### 7. Aero

- Front: `Unchanged`
- Rear: `Unchanged`

The captured performance panel showed `0.00` aero balance, so this baseline
assumes no adjustable aero is installed.

#### 8. Brake

- Balance: `52% front`
- Pressure: `105%`

#### 9. Differential

- Front acceleration: `35%`
- Front deceleration: `5%`
- Rear acceleration: `65%`
- Rear deceleration: `15%`
- Center balance: `70% rear`

If the Escort feels too loose while banking skill chains, lower rear
acceleration to `60%` before changing suspension. If it still pulls or yaws
hard on powered landings, move center balance to `75% rear`.

### Post-Tune Performance Panel

Captured after applying the v1 baseline on 2026-06-25. The corrected gearing
screen confirms `1st` at `3.60`, matching the written baseline.

| Metric | Value |
| --- | ---: |
| PI | S1 756 |
| 60-0 braking | 83.8 ft |
| 100-0 braking | 212.3 ft |
| 60 mph lateral G | 1.15 |
| 120 mph lateral G | 1.14 |
| 0-60 mph | 2.152 s |
| 0-100 mph | 6.017 s |
| Top speed | 130.3 mph |
| Mechanical balance | 0.45 |
| Aero balance | 0.00 |
| Aero efficiency | 0.824 |

First read: the gearing fix worked, moving top speed from `95.8 mph` to
`130.3 mph` without losing the quick launch. Mechanical balance at `0.45` is
below the normal target window, so watch for front-end push during paved
transitions before changing springs or differentials.

### EventLab Skill Grind Point

Current test context: EventLab runway grind lane with repeated destructible
prop rows and enough straight-line space to maintain a long chain.

Why this fits the Escort mastery tree:

- Repeated prop hits feed the `+10%` Wreckage bonus.
- Light lane changes and near-contact hits can feed Sideswipe, Link, and Combo.
- The long straight lets the `2.5x` multiplier build speed reach the `9x` cap
  quickly without needing a high-risk freeroam route.
- Keep speed in the controllable range first; score loss from breaking the
  chain matters more than peak speed.

Driving rhythm for v1:

1. Launch cleanly, then settle into second or third before the first prop row.
2. Weave gently across the destructible lanes instead of sawing the wheel.
3. Use small throttle lifts to keep the rear planted if the car starts skating.
4. Bank the chain before pushing for another pass if the car starts bouncing or
   the camera shakes after repeated hits.

If the Escort drifts wide and misses rows, raise front tire pressure to
`20.5 PSI` or soften front antiroll to `17.0`, one change at a time. If prop
hits kick the rear loose, lower rear antiroll to `18.5` before touching the
differential.

### House Track Tabletop Test

Current preferred grind context: user's house EventLab track with much shorter
loading time than the runway grind. The track uses small tabletop jumps,
destructible props, and repeated short runs.

Observed issue on v1: the Escort is nose-heavy even on small tabletops. This is
likely rear kick plus front landing load, not a need for more speed.

### Tabletop Nose-Heavy Revision

**Status:** Next test (`v2`, 2026-06-25). Keep the v1 gearing and skill-chain
pace, but calm the rear and give the front more support for tabletop landings.

#### 1. Tires

- Front: `20.0 PSI`
- Rear: `19.0 PSI`

#### 2. Gearing

- Final drive: `3.45`
- 1st: `3.60`
- 2nd: `2.55`
- 3rd: `1.95`
- 4th: `1.55`
- 5th: `1.25`
- 6th: `1.05`

#### 3. Alignment

- Front camber: `-1.2 deg`
- Rear camber: `-0.8 deg`
- Front toe: `0.0 deg`
- Rear toe: `-0.1 deg` (toe-in)
- Front caster: `5.4 deg`

#### 4. Antiroll Bars

- Front: `18.0`
- Rear: `18.5`

#### 5. Springs

- Front: `315.0 lb/in`
- Rear: `315.0 lb/in`
- Front ride height: `12.2 in`
- Rear ride height: `12.0 in`

#### 6. Damping

- Front rebound: `6.2`
- Rear rebound: `6.1`
- Front bump: `3.0`
- Rear bump: `2.3`

#### 7. Aero

- Front: `Unchanged`
- Rear: `Unchanged`

#### 8. Brake

- Balance: `52% front`
- Pressure: `105%`

#### 9. Differential

- Front acceleration: `35%`
- Front deceleration: `5%`
- Rear acceleration: `65%`
- Rear deceleration: `15%`
- Center balance: `70% rear`

Validation target: hold light throttle over the tabletop and land close to
level without the nose stabbing down. If the nose still dives, move center
balance to `75% rear` before adding more spring. If the car starts floating or
bouncing after landing, add `0.3` front bump.
