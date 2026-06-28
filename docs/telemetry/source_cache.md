# FH6 Telemetry Source Cache

This is the local map of the external material behind the telemetry workflow so
future tuning work does not need to rediscover it.

## Local Copies

| Item | Local path | Upstream |
| --- | --- | --- |
| UDP router source clone | `tools/FH6-UDP-Telemetry-Router` | <https://github.com/Kurinshiku34/FH6-UDP-Telemetry-Router> |
| UDP router release zip | `tools/FH6_Telemetry_Router_v1.0.2.zip` | <https://github.com/Kurinshiku34/FH6-UDP-Telemetry-Router/releases/download/v1.0.2/FH6_Telemetry_Router_v1.0.2.zip> |
| UDP router executable | `tools/FH6-Telemetry-Router-release/FH6 Telemetry Router/FH6_Telemetry_Router.exe` | Extracted from `v1.0.2` release zip |
| FH6 Data Out notes | `docs/telemetry/fh6_data_out_schema.md` | <https://support.forza.net/hc/en-us/articles/51744149102611-Forza-Horizon-6-Data-Out-Documentation> |
| Telemetry workflow | `docs/telemetry/README.md` | Local synthesis from router source and official FH6 docs |
| Decoder/listener | `tools/fh6_telemetry.py` | Local implementation of official 324-byte packet |
| PowerShell launcher | `tools/fh6_telemetry.ps1` | Local wrapper for Windows/Codex Python runtime |

## Router

- Repository: <https://github.com/Kurinshiku34/FH6-UDP-Telemetry-Router>
- Current local clone: tag `v1.0.2`, commit `5df4e2f`
- Latest release checked during setup: <https://github.com/Kurinshiku34/FH6-UDP-Telemetry-Router/releases/tag/v1.0.2>
- Useful release asset: `FH6_Telemetry_Router_v1.0.2.zip`
- Nexus discovery page: <https://www.nexusmods.com/forzahorizon6/mods/438>
- Local zip SHA256:
  `BD57AB92BECA65381D16AEE1FBD2B5DE0D5AE6A6C1D99C4D12DCD3C1E8D1ABA1`
- Local exe SHA256:
  `523D33175529860D8FB1BE4450C2974348C399089B453AA8D1CD08A3F415CDDD`

The router source clone is a local cache and is ignored by git as a nested
repository. Run `.\tools\clone_fh6_router.ps1` to recreate it after a fresh
checkout.

The release zip and extracted executable are also ignored by git. Run
`.\tools\download_fh6_router_release.ps1` to recreate them.

Run `.\tools\configure_fh6_router.ps1` to write the local `5310 -> 5311`
router config before launching the executable. The generated config enables
`AutoWatch` so Steam launch automation can start forwarding after FH6 appears.

Run `.\tools\get_fh6_steam_launch_option.ps1` to print the safe one-line Steam
Launch Options command for the project-local router executable.

Router behavior from source:

- Listens on one configured Forza main UDP port.
- Forwards raw datagrams unchanged to each target port on `127.0.0.1`.
- Does not parse, filter, transform, or relay to remote hosts.
- Defaults to main port `5300`, but this project should prefer `5310+`.
- Defaults the auto-watch process name to `forzahorizon6`.
- Saves `ForzaPort`, `GameExeName`, `AutoWatch`, `TargetPorts`, and launched
  companion app paths in `config.json` beside the router executable.

## Official FH6 Packet

- Official article: <https://support.forza.net/hc/en-us/articles/51744149102611-Forza-Horizon-6-Data-Out-Documentation>
- Packet size: `324` bytes.
- Transport: one-way UDP to the configured IP/port.
- Emission rate: game frame rate while actively driving.
- In-game setup: `Settings > HUD and Gameplay`, `Data Out = On`,
  IP `127.0.0.1`, port matching the router main port.
- Official caveat: avoid receiver ports `5200` through `5300`.
- FH6-specific fields after `NumCylinders`: `CarGroup`,
  `SmashableVelDiff`, `SmashableMass`.
- FH6 omits Motorsport `TireWear` and `TrackOrdinal`.
- The visible field list totals `323` named bytes, so the local parser preserves
  one trailing `_PacketPadding` byte to match the official `324` byte packet.
