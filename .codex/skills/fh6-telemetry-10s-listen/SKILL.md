---
name: fh6-telemetry-10s-listen
description: Run the proven short Forza Horizon 6 telemetry listener workflow for troubleshooting, drag or cornering pulls, safe isolated captures, and crash isolation when FH6 Data Out is already enabled and the FH6 UDP Telemetry Router is forwarding 5310 to 5311. Use when the user asks for a 10-second listener window, quick telemetry capture, short pull, safe listener test, or to "fire it up" for FH6 telemetry.
---

# FH6 Telemetry 10s Listen

## Purpose

Use the existing project listener for a narrow, known-good 10-second capture window. This workflow proved that short reads from the router target port can complete while FH6 and the router remain alive.

## Assumed State

- Work from `C:\Users\EmpressAlae\Documents\ffh6`.
- FH6 may already be running; the router may already be running.
- In-game Data Out should be `On`, IP `127.0.0.1`, port `5310`.
- FH6 Telemetry Router should listen on `5310` and forward to target `5311`.
- Do not start the game, router, hub monitor, or extra listeners unless the user explicitly asks. This skill is only the short listener window.

## Capture

Tell the user the 10-second window is starting, then run this from the repo root. Pick a short label such as `drag-pass`, `cornering`, `beat-baseline`, or `crash-isolation`.

```powershell
$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$label = 'drag-pass'
$out = "telemetry\$stamp-$label-10s-fh6-telemetry.jsonl"
.\tools\fh6_telemetry.ps1 listen --port 5311 --duration 10 --jsonl $out --label "$label-10s" --summary-every 1
```

If the user is lining up for a pull, start the listener only when they say they are ready; the window is intentionally short.

## Immediate Check

After the listener exits, summarize the capture and confirm FH6/router health.

```powershell
.\tools\fh6_telemetry.ps1 summary $out
Get-Process -Name forzahorizon6,FH6_UDPort_Forwarder -ErrorAction SilentlyContinue |
    Select-Object ProcessName,Id,CPU,WorkingSet64,StartTime,Path |
    Format-List
```

## Report

Keep the response short and operational:

- Capture path.
- Packet count and effective sample rate.
- Detected car ordinal, class, PI, and drivetrain.
- Whether FH6 and `FH6_UDPort_Forwarder` are still alive.
- For a pull, call out if the launch happened late or outside the 10-second window.
- If useful, derive threshold timing from `_monotonic_s` in the JSONL, using the first near-stationary high-throttle sample as the launch reference.

Known clean examples from this project:

- `telemetry\20260627-110937-honda-beat-a700-10s-fh6-telemetry.jsonl`: 493 packets over 9.95s, FH6/router survived.
- `telemetry\20260627-111323-drag-pass-10s-fh6-telemetry.jsonl`: 722 packets over 10.00s, FH6/router survived.
