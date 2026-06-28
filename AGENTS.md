Forza Horizon 6 project instructions

- This project is for Forza Horizon 6 only. If the user omits the game title,
  infer FH6. Do not answer with FH5/FH4 assumptions unless the user explicitly
  asks for a comparison to another game.
- Before providing a tune, check this file and `TUNING.md` for local tuning
  conventions and prior measured values.
- Always present tuning values in the in-game menu order documented in
  `TUNING.md`: Tires, Gearing, Alignment, Antiroll Bars, Springs, Damping,
  Aero, Brake, Differential.
- Ask the user for the vehicle's front and rear ride-height slider minimums
  and maximums before giving numeric ride-height values. If the rest of the
  tune can be useful immediately, provide it with ride height marked `Pending
  min/max` rather than inventing values.
- The user's default play context is Xbox controller, Standard steering,
  automatic transmission, ABS off, traction control off, and stability control
  off.
- Before diagnosing throttle, gearing, launch, drift wheelspin, or power
  delivery problems, confirm the Xbox controller's rear trigger-stop switches
  are set to full trigger throw. The controller has three-way switches: top is
  full throw, middle is 50% throw, and bottom is click. This physically limits
  how deeply the trigger can be depressed, changing throttle modulation travel
  rather than indicating a tune issue.
- When a Git commit is requested during tuning or telemetry work, prefer
  spawning a separate Codex thread/agent to perform the scoped stage/commit so
  the main thread can continue analysis in parallel. The commit agent must be
  told the exact files or paths it owns and must not stage unrelated work.
- Manual shifting is available for drift builds only.
- The user prefers throatier, meaner sounding cars.
