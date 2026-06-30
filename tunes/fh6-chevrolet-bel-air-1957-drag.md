# FH6 Chevrolet Bel Air 1957 - Drag Tune

## Context

- Game: FH6
- Car identity: ordinal `1459`
- Class: `S1 787`
- Drivetrain: AWD
- Build: max engine direction, drag tires, 7-speed transmission, and maximum
  practical weight removal.
- Purpose: drag tune for the map kilo-drag challenge and the great air leap
  landing afterward. This is not a drift tune.
- Controls: Xbox controller, simulation steering, automatic transmission, ABS
  off, traction control off, stability control off.
- Status: complete. The Bel Air did her job.

## Completion Result

The build completed the map kilo-drag challenge and made the great air leap
afterward, landing approximately `1100 ft` downrange and planting cleanly.
Treat this direction as validated for the challenge target: straight-line
launch, high-speed pull, and landing stability all passed.

## Telemetry Anchor

- `telemetry/20260630-094126-car-1459-s1-787-awd-10s-fh6-telemetry.jsonl`:
  `720` active packets over `9.985 s`, full throttle throughout, no brake use,
  no bottoming, and no airborne proxy during the captured window. The car
  reached `60 mph` in `2.016 s`, `100 mph` in `3.500 s`, and `181.84 mph`
  inside the 10-second pull.
- Compared with the earlier Bel Air pull, this pass improved by about `0.59 s`
  to `60 mph`, about `0.55 s` to `100 mph`, and `3.48 mph` at max speed.
  Front slip dropped sharply while rear slip became dominant, meaning the car
  was finally launching from the rear instead of wasting the pull through the
  front axle.

## Hold

Do not retune this for drift behavior. If the challenge goal returns, preserve
the validated drag direction unless a matched follow-up pull shows a clear
launch, shift, or landing regression.
