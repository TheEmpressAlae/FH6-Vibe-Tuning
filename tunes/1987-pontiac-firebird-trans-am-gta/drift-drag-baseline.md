# 1987 Pontiac Firebird Trans Am GTA - Drift-Drag Baseline

## Context

- Game: FH6
- Class: `S1 780`
- Drivetrain: RWD
- Purpose: drag-tire drift-drag baseline with forward bite before a sharp rear
  breakaway.
- Controls: Xbox controller, Standard steering, ABS off, traction control off,
  stability control off.
- Shifting: manual is available for drifting; current telemetry stayed in
  second gear.
- Status: v1.3 dry baseline. Rain began before a clean v1.3 telemetry pull, so
  wet-road behavior is not part of the dry baseline.

Rear trigger stops were confirmed at full throw before diagnosing throttle,
launch, drift wheelspin, or power delivery.

## Tune

### 1. Tires

- Compound: `Drag Tire Compound`
- Front: `30.0 PSI`
- Rear: `16.0 PSI`

### 2. Gearing

- Final drive: `4.60`
- 1st: `2.07`
- 2nd: `1.56`
- 3rd: `1.19`
- 4th: `0.98`
- 5th: `0.88`
- 6th: `0.80`

Second gear is the current drift-drag gear.

### 3. Alignment

- Front camber: `-2.2 deg`
- Rear camber: `-0.7 deg`
- Front toe: `+0.2 deg` toe-out
- Rear toe: `-0.1 deg` toe-in
- Front caster: `7.0 deg`

### 4. Antiroll Bars

- Front: `52.0`
- Rear: `45.0`

### 5. Springs

- Front: `600.0 lb/in`
- Rear: `500.0 lb/in`
- Front ride height: `4.0 in`
- Rear ride height: `4.1 in`

### 6. Damping

- Front rebound: `10.8`
- Rear rebound: `8.8`
- Front bump: `6.4`
- Rear bump: `5.2`

### 7. Aero

- Front: `145 lb`
- Rear: `247 lb`

### 8. Brake

- Balance: `70% front`
- Pressure: `100%`

### 9. Differential

- Rear acceleration: `83%`
- Rear deceleration: `10%`

## Measured Slider Ranges

| Setting | Front minimum | Front maximum | Rear minimum | Rear maximum |
| --- | ---: | ---: | ---: | ---: |
| Springs | 323.4 | 1,617.2 | 323.4 | 1,617.2 lb/in |
| Ride height | 3.4 | 4.8 | 3.4 | 4.8 in |

## Adjustment Cues

- If the rear shows too quickly on dry pavement, lower rear acceleration to
  `82%`.
- If the car feels slightly too lazy once the road is dry and the driver is
  awake, raise rear acceleration to `84%`.
- Keep rear deceleration at `10%` unless lift-off entry starts feeling numb;
  v1.2 telemetry showed the added decel helped calm the early rear rotation.
- Do not change spring, damping, ride height, or gearing from wet-road feel
  unless the target changes to rain drifting.

## Telemetry Notes

- `telemetry/20260628-104452-1987-pontiac-firebird-trans-am-gta-s1-780-rwd-10s-fh6-telemetry.jsonl`:
  v1.1 launch pull into a traffic-avoidance drift. The car signature was
  Firebird: ordinal `1045`, RWD, `S1 780`. It stayed in second, reached
  `60 mph` in about `2.48 s`, and showed no brake, handbrake, bottoming, or
  airborne samples.
- `telemetry/20260628-105607-1987-pontiac-firebird-trans-am-gta-s1-780-rwd-10s-fh6-telemetry.jsonl`:
  clean v1.1 held-line pull. Average speed was `49.9 mph`, max speed was
  `77.5 mph`, and rear slip ratio averaged `4.80`, matching the too-eager rear
  feel.
- `telemetry/20260628-110127-1987-pontiac-firebird-trans-am-gta-s1-780-rwd-10s-fh6-telemetry.jsonl`:
  v1.2 mid-line drift pull. Average speed was `79.5 mph`, max speed was
  `92.3 mph`, rear slip ratio averaged `0.97`, and the driver reported the car
  felt better but slightly sluggish.

These Firebird captures were repaired after the old Stream Deck default wrote
`miata-drag`; filenames and JSONL `_label` rows now match the packet identity.

Next dry validation: repeat a simple mid-line second-gear drift pull with
v1.3. Use rain captures only for a separate wet-road setup.
