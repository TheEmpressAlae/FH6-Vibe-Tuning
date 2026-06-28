# FH6 telemetry baseline

Date: 2026-06-27

## Current stable baseline

- Steam Launch Options for FH6 are empty.
- FH6 is stable with Data Out enabled across multiple play sessions.
- No telemetry hub, router, splitter, or listener is bound on known UDP ports during the stable sessions.
- Vortex-deployed convenience mods are present:
  - Completely Silent Start Menu
  - Fast Startup v1.3.1
  - fh-less-anims
  - NO TRAFFIC
  - No Transmission Whine
- The convenience mod set is not the first suspect because the game has been stable with those deployed and Data Out enabled.
- Data Out itself is not the first suspect. The remaining suspect class is the receiving/forwarding stack: hub, router, splitter, listener, or downstream telemetry tool behavior.

## Tool expectations

FH6 Data Out sends telemetry to one IP and one UDP port. If more than one tool needs packets, run exactly one splitter/forwarder as the Data Out target and let it fan packets out to the tools.

Observed tool ports:

- ONYX Drive HUD: listen on UDP `5607`.
- ForzaTuner: listen on UDP `8000`.
- ForzaDash: listen on UDP `1234`.
- Current FH6 Data Out port: UDP `5310`.
- Current local router/splitter fanout target for project capture: UDP `5311`.

Port `44405` appeared in an earlier draft of this note as a splitter-side example/default. It is not the current FH6 baseline, not present in local router configs, and should not replace `5310` unless deliberately testing a splitter that cannot listen on `5310`.

The current local router config uses:

- Game/Data Out source target: UDP `5310`.
- Forwarded local target: UDP `5311`.

Do not run the old router and the Nexus splitter at the same time. They solve the same "single Data Out target, many consumers" problem, and stacking them adds failure surface.

## Preferred architecture

Single consumer:

```text
FH6 Data Out -> tool port
```

Examples:

```text
FH6 Data Out -> 127.0.0.1:8000 -> ForzaTuner
FH6 Data Out -> 127.0.0.1:1234 -> ForzaDash
FH6 Data Out -> 127.0.0.1:5607 -> ONYX Drive HUD
```

Multiple consumers:

```text
FH6 Data Out -> 127.0.0.1:5310 -> Forza Telemetry Splitter
Splitter -> 127.0.0.1:8000 -> ForzaTuner
Splitter -> 127.0.0.1:1234 -> ForzaDash
Splitter -> 127.0.0.1:5607 -> ONYX Drive HUD
```

Add the project capture/listener only after the commercial tools are stable:

```text
Splitter -> 127.0.0.1:5311 -> local capture script
```

## Test rounds

Keep each round long enough to include real driving, map loads, skill chains, and garage/menu transitions.

1. Baseline already passed: Launch Options empty, Data Out enabled, mods deployed, no router/splitter/listener.
2. Receiverless Data Out repeat: keep Data Out pointed at `127.0.0.1:5310`, but run no splitter/listener. This is already effectively passing; repeat only if a port/config change needs confirmation.
3. Splitter only: start Forza Telemetry Splitter listening on `5310`, with no downstream tools enabled. Expected result: packets arrive and are discarded or logged without game impact.
4. One tool direct through splitter: add exactly one downstream target. Start with ForzaTuner on `8000` because it is the tuning workflow tool.
5. Second tool: add ForzaDash on `1234`.
6. Third tool: add ONYX on `5607`.
7. Optional project capture: add local listener on `5311` for short named captures only.

If FH6 exits during a round, the last added component is the suspect. Reset to the previous stable round and repeat once before changing other variables.

## Preflight check

Before a telemetry test, verify:

```powershell
Get-Process | Where-Object { $_.ProcessName -match 'forzahorizon6|Forza|Telemetry|UDPort|Forwarder|Router|Splitter|ONYX|ForzaDash|ForzaTuner' }
Get-NetUDPEndpoint | Where-Object { $_.LocalPort -in 5607,8000,1234,5310,5311 }
```

Known clean state: no UDP endpoints bound on `5607`, `8000`, `1234`, `5310`, or `5311` before starting the next telemetry component.
