# FlySky Noble USB input profile

Scope: FlySky Noble NB4/NB4+ as a USB simulator controller for FH6 through the local XOutput bridge.

## Sources checked

- FlySky NB4 downloads and current NB4 manual: https://www.flysky-cn.com/nb4-xiazai
- FlySky NB4+ current manual: https://www.flysky-cn.com/s/Noble_NB4_User_Manual-20250911-EN-3500mAh.pdf
- XOutput project: https://github.com/csutorasa/XOutput
- Microsoft RawGameController API reference: https://learn.microsoft.com/en-us/uwp/api/windows.gaming.input.rawgamecontroller

## Local state observed

As of 2026-06-29, the current Windows device probe did not expose a connected FlySky/Noble device. The legacy joystick probe only reported Microsoft/Xbox joystick devices.

The local XOutput folder does contain an existing profile:

- File: `tools/XOutput-3.32/settings.json`
- Profile: `Flysky Noble Native`
- Historical DirectInput device: `Flysky Noble+ EN`
- Historical DirectInput GUID: `9cd567c0-6d87-11f1-8003-444553540000`
- XOutput log showed emulation starting through ViGEm on 2026-06-21, then a poll failure for that GUID later the same session.

Because DirectInput GUIDs can change after reconnects, do not trust the stored GUID alone. Re-detect the device by product name first, then bind the offsets.

The Noble and the other USB controller path share the same cord in the current setup, so they are not expected to compete as two physical USB controllers at the same time. The remaining double-input risk is Windows/FH6 seeing both the raw FlySky DirectInput device and XOutput's virtual Xbox controller.

## Radio-side baseline

Use a dedicated model memory named something like `FH6 USB RAW`.

For NB4+, set `SYSTEM > USB Setup > USB Function`. The NB4+ manual says USB Function is the Type-C USB signal mode for simulator/computer/FlySky Assistant use; Trainer Mode is PPM. Original NB4 documentation says the USB simulator function is enabled by default and the USB port is used for charging, firmware/update software, and simulator connection.

Recommended transmitter settings for clean USB interpretation:

- `REV`: leave steering and throttle normal at first. Fix inversion in XOutput or the input interpreter after sampling.
- `EPA`: CH1 steering left/right `100/100`; CH2 throttle forward/brake `100/100`.
- `SUBTRIM`: CH1 and CH2 `0`.
- `ST DR/EXP`: rate `100`, EXP `0`.
- `TH DR/EXP`: Rate.F `100`, Rate.B `100`, Exp.F `0`, Exp.B `0`.
- `TH MID`: leave at the stock midpoint unless the neutral raw value is not close to `0.5`; tune only after transmitter stick calibration.
- `TH NEUTRAL`: Dead Zone `0%`. Leave Forward/Backward at defaults unless the trigger jumps away from neutral; any dead zone here hides real USB movement.
- `TH CURVE`: disabled or linear.
- `Channel Speed`: no delay / fastest response for CH1 and CH2.
- `ABS`, `SVC/gyro`, mixes, brake mixes, idle-up, throttle speed shaping, cruise, crawler/4WS helpers: disabled.
- Trims and assigned knobs: avoid changing them after calibration; they move the center point that the USB interpreter depends on.

After mechanical changes or if center/endpoints drift, run `SYSTEM > Stick Calibration`. FlySky's manual says to move the steering wheel and throttle trigger to their full ranges, release them to neutral, save, then verify outputs in `Servo View`.

## Current XOutput mapping

The existing `Flysky Noble Native` profile maps the Noble like this:

| XInput output | DirectInput offset | Observed profile range | Role |
| --- | ---: | ---: | --- |
| `LX` | `12` | `0.0826733806` to `0.9166704814` | Steering |
| `R2` | `8` | `0.5` to `0.0833295186` | Throttle, inverted side of trigger axis |
| `L2` | `8` | `0.5` to `0.9173266194` | Brake, positive side of trigger axis |

This matches the FH6 convention of Xbox `RT` as throttle and `LT` as brake, but verify physically: pull the trigger for throttle and confirm `R2` rises; push for brake and confirm `L2` rises.

Historical XOutput log offsets for `Flysky Noble+ EN`:

- `X Rotation`: offset `0`
- `Z Axis`: offset `4`
- `Y Axis`: offset `8`
- `X Axis`: offset `12`
- Buttons `0..11`: offsets `16..27`

The later Xbox/Bluetooth devices in the same log use different offsets, so keep FlySky-specific offsets tied to the detected `Flysky Noble+ EN` product name, not to the last seen generic joystick.

## Interpreter rules

Prefer one of these input paths:

- DirectInput raw device to XOutput to ViGEm virtual Xbox controller for FH6.
- Raw HID/RawGameController style reading for Codex-side diagnostics.

Normalize axes from measured values, not theoretical full scale:

```text
steering = clamp((raw - steer_center) / max(steer_center - steer_min, steer_max - steer_center), -1, 1)
throttle = clamp((trigger_center - raw) / (trigger_center - trigger_throttle_full), 0, 1)
brake    = clamp((raw - trigger_center) / (trigger_brake_full - trigger_center), 0, 1)
```

For the current XOutput profile, `trigger_center` is `0.5`, throttle-full is about `0.08333`, and brake-full is about `0.91733`.

Use small interpreter dead zones after radio calibration:

- Steering: `0.01` to `0.02`.
- Trigger neutral split: `0.02` around center.

Do not stack curves. Keep the transmitter linear and put any FH6 feel tuning in XOutput/game settings/interpreter code, where it is visible and repeatable.

## Troubleshooting checklist

- If the radio does not appear, confirm NB4+ is in `USB Function`, not `Trainer Mode`.
- Use a data-capable USB cable and the transmitter data port, not a charge-only path.
- If XOutput cannot see it, close FH6/XOutput, reconnect the transmitter, then reopen XOutput.
- If XOutput sees it but FH6 sees double input, check HidHide/HidGuardian so FH6 only sees the virtual Xbox controller and XOutput still sees the raw FlySky.
- If steering or trigger reaches only about `0.08..0.92`, that can still be normal; calibrate min/center/max around observed endpoints rather than forcing full `0..1`.
- If neutral wanders, rerun FlySky Stick Calibration and then update XOutput min/max/center.
- If the profile breaks after reconnect, create a fresh XOutput mapping for the newly detected `Flysky Noble+ EN` device and copy the axis choices/ranges above.
