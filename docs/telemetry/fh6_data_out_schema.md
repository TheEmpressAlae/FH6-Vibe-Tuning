# FH6 Data Out Schema Notes

Official source: <https://support.forza.net/hc/en-us/articles/51744149102611-Forza-Horizon-6-Data-Out-Documentation>

Important points from the official article:

- FH6 sends one fixed packet format. There is no Sled/Dash selector.
- Total packet size is `324` bytes.
- Packets are one-way UDP to the configured address.
- Packets are sent at the game frame rate while the player is actively driving.
- Packets are not sent during menus, pause, replays, rewinds, or after finishing
  a race.
- `127.0.0.1` localhost output is supported.
- Avoid ports `5200` through `5300` for the receiving app.
- FH6 adds `CarGroup`, `SmashableVelDiff`, and `SmashableMass` after
  `NumCylinders`.
- FH6 does not include the Forza Motorsport `TireWear` or `TrackOrdinal` fields.
- FH6 uses `S32 WheelInPuddle*` boolean fields. Older Forza Motorsport docs use
  `F32 WheelInPuddleDepth*`; do not apply that older schema to FH6 captures.

The documented fields add to `323` bytes. The local parser treats the last byte
as `_PacketPadding` so the decoded structure matches the official `324` byte
packet size. If a future patch changes the packet size, the listener will report
the unexpected byte count instead of silently decoding bad data.

Run this command for the authoritative local offset table generated from the
parser:

```powershell
.\tools\fh6_telemetry.ps1 schema --markdown
```
