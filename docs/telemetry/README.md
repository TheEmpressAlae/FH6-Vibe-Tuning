# FH6 Telemetry

This project can now consume Forza Horizon 6 Data Out telemetry locally.

## Cached References

- Router source clone: `tools/FH6-UDP-Telemetry-Router`
- Router upstream: <https://github.com/Kurinshiku34/FH6-UDP-Telemetry-Router>
- Router release checked: <https://github.com/Kurinshiku34/FH6-UDP-Telemetry-Router/releases/tag/v1.0.2>
- Nexus page that pointed at the router: <https://www.nexusmods.com/forzahorizon6/mods/438>
- Official packet source: <https://support.forza.net/hc/en-us/articles/51744149102611-Forza-Horizon-6-Data-Out-Documentation>

The Nexus page is Cloudflare-protected from scripts, so the GitHub repo and
official Forza support article are the durable local sources.

## Wiring

Recommended ports:

- FH6 Data Out IP: `127.0.0.1`
- FH6 Data Out Port: `5310`
- Router Forza Main Port: `5310`
- Router target port for this project: `5311`
- Optional additional router target ports: SimHub, dashboards, motion rigs, etc.

The router README uses `5300` as its example main port, but the official FH6
Data Out article says to avoid ports `5200` through `5300` because the game can
bind its outgoing socket in that range. Prefer `5310+` unless a later test proves
we need a different range.

The local router clone is currently at `v1.0.2`, which fixes the router's
`config.json` lookup when launched through Steam. Router settings are stored in
`config.json` beside the router executable, not in this project folder.

The router clone is intentionally ignored by this repo because it is a nested
upstream repository. Recreate it after a fresh checkout with:

```powershell
.\tools\clone_fh6_router.ps1
```

The runnable router release is also cached locally but ignored by git:

- ZIP: `tools\FH6_Telemetry_Router_v1.0.2.zip`
- EXE: `tools\FH6-Telemetry-Router-release\FH6 Telemetry Router\FH6_Telemetry_Router.exe`
- ZIP SHA256: `BD57AB92BECA65381D16AEE1FBD2B5DE0D5AE6A6C1D99C4D12DCD3C1E8D1ABA1`
- EXE SHA256: `523D33175529860D8FB1BE4450C2974348C399089B453AA8D1CD08A3F415CDDD`

Recreate or launch the local router with:

```powershell
.\tools\download_fh6_router_release.ps1
.\tools\configure_fh6_router.ps1
.\tools\start_fh6_router.ps1
```

For Steam Launch Options, do not copy from the router help window. It can point
at the wrong local copy and the wrapped help text is easy to misread. Generate
the project-local one-line command instead:

```powershell
.\tools\get_fh6_steam_launch_option.ps1
```

Paste that output into Steam as a single line. `configure_fh6_router.ps1` sets
`AutoWatch` to `true`, so Steam can launch the router first and the router will
start forwarding when the FH6 process appears.

## Capture

Start the router, make sure it is routing or has `AutoWatch` enabled, then run:

```powershell
.\tools\fh6_telemetry.ps1 listen --port 5311 --label escort-tabletop-v2
```

By default this writes a JSONL file under `telemetry/` and prints a live summary
once per second. Use `--csv telemetry\run.csv` if a spreadsheet view is useful.

Useful variants:

```powershell
.\tools\fh6_telemetry.ps1 listen --port 5311 --duration 60 --label peugeot-v4
.\tools\fh6_telemetry.ps1 listen --port 5311 --save-hz 20 --label short-test
.\tools\fh6_telemetry.ps1 listen --port 5311 --no-save
```

Summarize a capture:

```powershell
.\tools\fh6_telemetry.ps1 summary telemetry\20260627-120000-escort-tabletop-v2-fh6-telemetry.jsonl
```

Print the schema:

```powershell
.\tools\fh6_telemetry.ps1 schema
.\tools\fh6_telemetry.ps1 schema --markdown
```

The `.ps1` launcher uses a normal Python install when available and falls back
to Codex's bundled Python runtime on this machine.

## What The Tool Watches

The first-pass analysis focuses on tuning-relevant signals:

- speed, gear, RPM, throttle, brake, handbrake, and steering input
- normalized suspension travel per corner, where `0` is full stretch and `1` is
  full compression
- tire slip ratio, slip angle, and combined slip per corner
- local acceleration and angular velocity for pitch, yaw, and roll behavior
- FH6 smashable-object fields for skill-chain routes

The packet does not include the human-readable car name or installed tuning
values. Capture labels still matter; use labels like `escort-v2-tabletop` or
`peugeot-v4-skill-chain` so later analysis lines up with `TUNING.md`.
