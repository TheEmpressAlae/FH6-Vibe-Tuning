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
- The user's default play context is Xbox controller, simulation steering,
  automatic transmission for race, manual for drift, ABS off, traction control
  off, and stability control off.
- When a Git commit is requested during tuning or telemetry work, prefer
  spawning a separate Codex thread/agent to perform the scoped stage/commit so
  the main thread can continue analysis in parallel. The commit agent must be
  told the exact files or paths it owns and must not stage unrelated work.
- The user prefers throatier, meaner sounding cars.
- Only ask the user about the throttle switches if something seems errant in
  the telemetry pulls the user provides for each car.
- When making tuning adjustments, only return the changed tabs in the correct
  menu order. There is no need to mention unchanged tabs if there is no reason
  to drill into them.
- For telemetry/log review, do not process raw JSONL or long logs in the main
  chat. Use bounded local parser commands and, when multi-agent tools are
  available, spawn a read-only telemetry review agent to reduce pulls into
  compact evidence. The main agent owns final tuning synthesis only.
