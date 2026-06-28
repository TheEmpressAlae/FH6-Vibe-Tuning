#!/usr/bin/env python3
"""Decode Forza Horizon 6 Data Out UDP packets.

The FH6 Data Out packet is a fixed 324-byte little-endian structure. This
tool listens on a UDP port, decodes packets, and can save JSONL/CSV captures
for later tuning analysis.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import socket
import struct
import sys
import time
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


MPH_PER_MPS = 2.2369362920544
KPH_PER_MPS = 3.6
HP_PER_WATT = 1.0 / 745.6998715822702
LBFT_PER_NM = 0.7375621492772654


@dataclass(frozen=True)
class Field:
    name: str
    code: str
    doc_type: str
    unit: str = ""
    note: str = ""

    @property
    def size(self) -> int:
        return struct.calcsize("<" + self.code)


FIELDS: tuple[Field, ...] = (
    Field("IsRaceOn", "i", "S32", note="1 when driving, 0 when stopped"),
    Field("TimestampMS", "I", "U32", "ms", "May overflow to 0 eventually"),
    Field("EngineMaxRpm", "f", "F32", "rpm"),
    Field("EngineIdleRpm", "f", "F32", "rpm"),
    Field("CurrentEngineRpm", "f", "F32", "rpm"),
    Field("AccelerationX", "f", "F32", "m/s^2", "Local space; X = right"),
    Field("AccelerationY", "f", "F32", "m/s^2", "Local space; Y = up"),
    Field("AccelerationZ", "f", "F32", "m/s^2", "Local space; Z = forward"),
    Field("VelocityX", "f", "F32", "m/s", "Local space; X = right"),
    Field("VelocityY", "f", "F32", "m/s", "Local space; Y = up"),
    Field("VelocityZ", "f", "F32", "m/s", "Local space; Z = forward"),
    Field("AngularVelocityX", "f", "F32", "rad/s", "Pitch rate"),
    Field("AngularVelocityY", "f", "F32", "rad/s", "Yaw rate"),
    Field("AngularVelocityZ", "f", "F32", "rad/s", "Roll rate"),
    Field("Yaw", "f", "F32", "rad"),
    Field("Pitch", "f", "F32", "rad"),
    Field("Roll", "f", "F32", "rad"),
    Field("NormalizedSuspensionTravelFrontLeft", "f", "F32", "0-1"),
    Field("NormalizedSuspensionTravelFrontRight", "f", "F32", "0-1"),
    Field("NormalizedSuspensionTravelRearLeft", "f", "F32", "0-1"),
    Field("NormalizedSuspensionTravelRearRight", "f", "F32", "0-1"),
    Field("TireSlipRatioFrontLeft", "f", "F32"),
    Field("TireSlipRatioFrontRight", "f", "F32"),
    Field("TireSlipRatioRearLeft", "f", "F32"),
    Field("TireSlipRatioRearRight", "f", "F32"),
    Field("WheelRotationSpeedFrontLeft", "f", "F32", "rad/s"),
    Field("WheelRotationSpeedFrontRight", "f", "F32", "rad/s"),
    Field("WheelRotationSpeedRearLeft", "f", "F32", "rad/s"),
    Field("WheelRotationSpeedRearRight", "f", "F32", "rad/s"),
    Field("WheelOnRumbleStripFrontLeft", "i", "S32", "bool"),
    Field("WheelOnRumbleStripFrontRight", "i", "S32", "bool"),
    Field("WheelOnRumbleStripRearLeft", "i", "S32", "bool"),
    Field("WheelOnRumbleStripRearRight", "i", "S32", "bool"),
    Field("WheelInPuddleFrontLeft", "i", "S32", "bool"),
    Field("WheelInPuddleFrontRight", "i", "S32", "bool"),
    Field("WheelInPuddleRearLeft", "i", "S32", "bool"),
    Field("WheelInPuddleRearRight", "i", "S32", "bool"),
    Field("SurfaceRumbleFrontLeft", "f", "F32"),
    Field("SurfaceRumbleFrontRight", "f", "F32"),
    Field("SurfaceRumbleRearLeft", "f", "F32"),
    Field("SurfaceRumbleRearRight", "f", "F32"),
    Field("TireSlipAngleFrontLeft", "f", "F32"),
    Field("TireSlipAngleFrontRight", "f", "F32"),
    Field("TireSlipAngleRearLeft", "f", "F32"),
    Field("TireSlipAngleRearRight", "f", "F32"),
    Field("TireCombinedSlipFrontLeft", "f", "F32"),
    Field("TireCombinedSlipFrontRight", "f", "F32"),
    Field("TireCombinedSlipRearLeft", "f", "F32"),
    Field("TireCombinedSlipRearRight", "f", "F32"),
    Field("SuspensionTravelMetersFrontLeft", "f", "F32", "m"),
    Field("SuspensionTravelMetersFrontRight", "f", "F32", "m"),
    Field("SuspensionTravelMetersRearLeft", "f", "F32", "m"),
    Field("SuspensionTravelMetersRearRight", "f", "F32", "m"),
    Field("CarOrdinal", "i", "S32"),
    Field("CarClass", "i", "S32", note="0 D through 7 X"),
    Field("CarPerformanceIndex", "i", "S32", "PI"),
    Field("DrivetrainType", "i", "S32", note="0 FWD, 1 RWD, 2 AWD"),
    Field("NumCylinders", "i", "S32"),
    Field("CarGroup", "I", "U32", note="FH6-specific"),
    Field("SmashableVelDiff", "f", "F32", "m/s", "FH6-specific"),
    Field("SmashableMass", "f", "F32", "kg", "FH6-specific"),
    Field("PositionX", "f", "F32", "m"),
    Field("PositionY", "f", "F32", "m"),
    Field("PositionZ", "f", "F32", "m"),
    Field("Speed", "f", "F32", "m/s"),
    Field("Power", "f", "F32", "W"),
    Field("Torque", "f", "F32", "N*m"),
    Field("TireTempFrontLeft", "f", "F32"),
    Field("TireTempFrontRight", "f", "F32"),
    Field("TireTempRearLeft", "f", "F32"),
    Field("TireTempRearRight", "f", "F32"),
    Field("Boost", "f", "F32", "psi", "Above atmospheric"),
    Field("Fuel", "f", "F32", "0-1"),
    Field("DistanceTraveled", "f", "F32", "m"),
    Field("BestLap", "f", "F32", "s"),
    Field("LastLap", "f", "F32", "s"),
    Field("CurrentLap", "f", "F32", "s"),
    Field("CurrentRaceTime", "f", "F32", "s"),
    Field("LapNumber", "H", "U16"),
    Field("RacePosition", "B", "U8"),
    Field("Accel", "B", "U8", "0-255"),
    Field("Brake", "B", "U8", "0-255"),
    Field("Clutch", "B", "U8", "0-255"),
    Field("HandBrake", "B", "U8", "0-255"),
    Field("Gear", "B", "U8"),
    Field("Steer", "b", "S8", "-127..127"),
    Field("NormalizedDrivingLine", "b", "S8", "-127..127"),
    Field("NormalizedAIBrakeDifference", "b", "S8", "-127..127"),
    # The documented named fields add up to 323 bytes; the official article
    # states a 324-byte packet. Preserve the final byte as alignment padding.
    Field("_PacketPadding", "B", "U8", note="Alignment padding"),
)
PACKET_STRUCT = struct.Struct("<" + "".join(field.code for field in FIELDS))
PACKET_SIZE = PACKET_STRUCT.size

CORNERS = ("FrontLeft", "FrontRight", "RearLeft", "RearRight")
CORNER_LABELS = {
    "FrontLeft": "FL",
    "FrontRight": "FR",
    "RearLeft": "RL",
    "RearRight": "RR",
}


class PacketSizeError(ValueError):
    pass


def parse_packet(data: bytes) -> dict[str, Any]:
    """Parse one FH6 Data Out packet."""
    if len(data) == PACKET_SIZE:
        values = PACKET_STRUCT.unpack(data)
        packet = dict(zip((field.name for field in FIELDS), values))
    else:
        raise PacketSizeError(
            f"unsupported packet size {len(data)} bytes; expected {PACKET_SIZE}"
        )

    packet["_packet_size"] = len(data)
    add_derived_fields(packet)
    return packet


def add_derived_fields(packet: dict[str, Any]) -> None:
    speed_mps = as_float(packet.get("Speed"))
    power_w = as_float(packet.get("Power"))
    torque_nm = as_float(packet.get("Torque"))
    accel = as_float(packet.get("Accel"))
    brake = as_float(packet.get("Brake"))
    clutch = as_float(packet.get("Clutch"))
    handbrake = as_float(packet.get("HandBrake"))
    steer = as_float(packet.get("Steer"))
    current_rpm = as_float(packet.get("CurrentEngineRpm"))
    max_rpm = as_float(packet.get("EngineMaxRpm"))

    packet["SpeedMph"] = speed_mps * MPH_PER_MPS
    packet["SpeedKph"] = speed_mps * KPH_PER_MPS
    packet["PowerHp"] = power_w * HP_PER_WATT
    packet["TorqueLbFt"] = torque_nm * LBFT_PER_NM
    packet["AccelPct"] = accel / 255.0 * 100.0
    packet["BrakePct"] = brake / 255.0 * 100.0
    packet["ClutchPct"] = clutch / 255.0 * 100.0
    packet["HandBrakePct"] = handbrake / 255.0 * 100.0
    packet["SteerPct"] = steer / 127.0 * 100.0 if steer >= 0 else steer / 128.0 * 100.0
    packet["EngineRpmPct"] = current_rpm / max_rpm * 100.0 if max_rpm > 0 else 0.0

    velocity = vector_magnitude(
        packet.get("VelocityX"), packet.get("VelocityY"), packet.get("VelocityZ")
    )
    packet["VelocityMagnitudeMps"] = velocity
    packet["VelocityMagnitudeMph"] = velocity * MPH_PER_MPS

    front_slip = average(
        [
            abs(as_float(packet.get("TireCombinedSlipFrontLeft"))),
            abs(as_float(packet.get("TireCombinedSlipFrontRight"))),
        ]
    )
    rear_slip = average(
        [
            abs(as_float(packet.get("TireCombinedSlipRearLeft"))),
            abs(as_float(packet.get("TireCombinedSlipRearRight"))),
        ]
    )
    slip_total = max(front_slip + rear_slip, 0.01)
    packet["FrontCombinedSlip"] = front_slip
    packet["RearCombinedSlip"] = rear_slip
    packet["SlipBalance"] = (front_slip - rear_slip) / slip_total

    velocity_x = as_float(packet.get("VelocityX"))
    velocity_z = as_float(packet.get("VelocityZ"))
    packet["BetaDeg"] = math.degrees(math.atan2(velocity_x, max(abs(velocity_z), 0.5)))

    steer_pct = abs(as_float(packet.get("SteerPct")) / 100.0)
    yaw_rate = abs(as_float(packet.get("AngularVelocityY")))
    packet["YawResponse"] = yaw_rate / max(speed_mps * steer_pct, 0.5)

    fl = as_float(packet.get("NormalizedSuspensionTravelFrontLeft"))
    fr = as_float(packet.get("NormalizedSuspensionTravelFrontRight"))
    rl = as_float(packet.get("NormalizedSuspensionTravelRearLeft"))
    rr = as_float(packet.get("NormalizedSuspensionTravelRearRight"))
    front_travel = average([fl, fr])
    rear_travel = average([rl, rr])
    packet["FrontTravel"] = front_travel
    packet["RearTravel"] = rear_travel
    packet["TravelBias"] = front_travel - rear_travel
    packet["DiagonalTravel"] = (fl + rr) - (fr + rl)
    packet["LeftRightTravel"] = (fl + rl) - (fr + rr)
    packet["AnyBottoming"] = int(max(fl, fr, rl, rr) >= 0.95)
    packet["AnyFullExtension"] = int(min(fl, fr, rl, rr) <= 0.05)
    packet["AirborneProxy"] = int(max(fl, fr, rl, rr) <= 0.05)


def vector_magnitude(*values: Any) -> float:
    return math.sqrt(sum(as_float(value) ** 2 for value in values))


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if value is None:
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def as_int(value: Any, default: int = 0) -> int:
    try:
        if value is None or value == "":
            return default
        return int(float(value))
    except (TypeError, ValueError):
        return default


def clean_for_json(value: Any) -> Any:
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    if isinstance(value, dict):
        return {key: clean_for_json(item) for key, item in value.items()}
    if isinstance(value, list):
        return [clean_for_json(item) for item in value]
    if isinstance(value, tuple):
        return [clean_for_json(item) for item in value]
    return value


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


def default_capture_path(output_dir: Path, label: str | None) -> Path:
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    suffix = ("-" + safe_slug(label)) if label else ""
    return output_dir / f"{stamp}{suffix}-fh6-telemetry.jsonl"


def safe_slug(value: str) -> str:
    slug = "".join(char.lower() if char.isalnum() else "-" for char in value)
    slug = "-".join(part for part in slug.split("-") if part)
    return slug[:48] or "capture"


def ordered_output_fields() -> list[str]:
    meta = [
        "_received_utc",
        "_monotonic_s",
        "_source_ip",
        "_source_port",
        "_label",
        "_packet_size",
    ]
    raw = [field.name for field in FIELDS]
    derived = [
        "SpeedMph",
        "SpeedKph",
        "PowerHp",
        "TorqueLbFt",
        "AccelPct",
        "BrakePct",
        "ClutchPct",
        "HandBrakePct",
        "SteerPct",
        "EngineRpmPct",
        "VelocityMagnitudeMps",
        "VelocityMagnitudeMph",
        "FrontCombinedSlip",
        "RearCombinedSlip",
        "SlipBalance",
        "BetaDeg",
        "YawResponse",
        "FrontTravel",
        "RearTravel",
        "TravelBias",
        "DiagonalTravel",
        "LeftRightTravel",
        "AnyBottoming",
        "AnyFullExtension",
        "AirborneProxy",
    ]
    return meta + raw + derived


class CsvSink:
    def __init__(self, path: Path):
        self.path = path
        self.file = path.open("w", newline="", encoding="utf-8")
        self.writer = csv.DictWriter(
            self.file, fieldnames=ordered_output_fields(), extrasaction="ignore"
        )
        self.writer.writeheader()

    def write(self, row: dict[str, Any]) -> None:
        self.writer.writerow(row)

    def close(self) -> None:
        self.file.close()


class JsonlSink:
    def __init__(self, path: Path):
        self.path = path
        self.file = path.open("w", encoding="utf-8")

    def write(self, row: dict[str, Any]) -> None:
        self.file.write(
            json.dumps(clean_for_json(row), separators=(",", ":"), allow_nan=False) + "\n"
        )

    def close(self) -> None:
        self.file.close()


def command_listen(args: argparse.Namespace) -> int:
    output_dir = Path(args.output_dir)
    sinks: list[Any] = []
    jsonl_path: Path | None = None
    csv_path: Path | None = None

    if not args.no_save:
        output_dir.mkdir(parents=True, exist_ok=True)
        jsonl_path = Path(args.jsonl) if args.jsonl else default_capture_path(output_dir, args.label)
        jsonl_path.parent.mkdir(parents=True, exist_ok=True)
        sinks.append(JsonlSink(jsonl_path))

    if args.csv:
        csv_path = Path(args.csv)
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        sinks.append(CsvSink(csv_path))

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((args.host, args.port))
    sock.settimeout(args.socket_timeout)

    print(f"Listening on {args.host}:{args.port} for FH6 {PACKET_SIZE}-byte Data Out packets.")
    if jsonl_path:
        print(f"JSONL capture: {jsonl_path}")
    if csv_path:
        print(f"CSV capture: {csv_path}")
    if args.save_hz > 0:
        print(f"Saving at up to {args.save_hz:g} Hz.")
    else:
        print("Saving every parsed packet.")
    print("Press Ctrl+C to stop.")

    started = time.monotonic()
    last_summary = started
    last_saved = 0.0
    packet_count = 0
    saved_count = 0
    bad_sizes: Counter[int] = Counter()
    last_packet: dict[str, Any] | None = None

    try:
        while True:
            now = time.monotonic()
            if args.duration and now - started >= args.duration:
                break

            try:
                data, source = sock.recvfrom(2048)
            except socket.timeout:
                if args.summary_every > 0 and last_packet and now - last_summary >= args.summary_every:
                    print_live_summary(packet_count, saved_count, last_packet, bad_sizes)
                    last_summary = now
                continue

            try:
                row = parse_packet(data)
            except PacketSizeError:
                bad_sizes[len(data)] += 1
                continue

            packet_count += 1
            now = time.monotonic()
            row["_received_utc"] = utc_now_iso()
            row["_monotonic_s"] = now - started
            row["_source_ip"] = source[0]
            row["_source_port"] = source[1]
            row["_label"] = args.label or ""
            last_packet = row

            should_save = args.save_hz <= 0 or now - last_saved >= 1.0 / args.save_hz
            if should_save:
                for sink in sinks:
                    sink.write(row)
                saved_count += 1
                last_saved = now

            if args.summary_every > 0 and now - last_summary >= args.summary_every:
                print_live_summary(packet_count, saved_count, row, bad_sizes)
                last_summary = now
    except KeyboardInterrupt:
        print()
    finally:
        sock.close()
        for sink in sinks:
            sink.close()

    print_live_summary(packet_count, saved_count, last_packet, bad_sizes, final=True)
    return 0


def print_live_summary(
    packet_count: int,
    saved_count: int,
    packet: dict[str, Any] | None,
    bad_sizes: Counter[int],
    final: bool = False,
) -> None:
    prefix = "Final" if final else "Live"
    if not packet:
        print(f"{prefix}: packets=0 saved=0 bad_sizes={dict(bad_sizes)}")
        return

    slip = " ".join(
        f"{CORNER_LABELS[corner]}={as_float(packet.get('TireCombinedSlip' + corner)):+.2f}"
        for corner in CORNERS
    )
    suspension = " ".join(
        f"{CORNER_LABELS[corner]}={as_float(packet.get('NormalizedSuspensionTravel' + corner)):.2f}"
        for corner in CORNERS
    )
    print(
        f"{prefix}: packets={packet_count} saved={saved_count} "
        f"speed={as_float(packet.get('SpeedMph')):.1f} mph "
        f"gear={as_int(packet.get('Gear'))} "
        f"rpm={as_float(packet.get('CurrentEngineRpm')):.0f} "
        f"thr={as_float(packet.get('AccelPct')):.0f}% "
        f"brk={as_float(packet.get('BrakePct')):.0f}% "
        f"steer={as_float(packet.get('SteerPct')):+.0f}% "
        f"slip[{slip}] susp[{suspension}]"
        + (f" bad_sizes={dict(bad_sizes)}" if bad_sizes else "")
    )


def command_schema(args: argparse.Namespace) -> int:
    rows = schema_rows(include_padding=args.include_padding)
    if args.markdown:
        print("| Offset | Type | Size | Field | Unit | Note |")
        print("| ---: | --- | ---: | --- | --- | --- |")
        for row in rows:
            print(
                f"| {row['offset']} | {row['type']} | {row['size']} | "
                f"{row['name']} | {row['unit']} | {row['note']} |"
            )
    else:
        print(f"FH6 Data Out packet size: {PACKET_SIZE} bytes")
        print(f"Named field bytes before padding: {PACKET_SIZE - 1} bytes")
        print()
        for row in rows:
            unit = f" {row['unit']}" if row["unit"] else ""
            note = f" - {row['note']}" if row["note"] else ""
            print(
                f"{row['offset']:>3} {row['type']:<3} "
                f"{row['size']:>2} {row['name']}{unit}{note}"
            )
    return 0


def schema_rows(include_padding: bool = True) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    offset = 0
    fields = FIELDS if include_padding else FIELDS[:-1]
    for field in fields:
        rows.append(
            {
                "offset": offset,
                "type": field.doc_type,
                "size": field.size,
                "name": field.name,
                "unit": field.unit,
                "note": field.note,
            }
        )
        offset += field.size
    return rows


def command_summary(args: argparse.Namespace) -> int:
    path = Path(args.capture)
    rows = list(read_capture(path))
    if not rows:
        print(f"No rows found in {path}")
        return 1

    active_rows = [row for row in rows if as_int(row.get("IsRaceOn")) == 1]
    summary_rows = active_rows or rows

    print(f"Capture: {path}")
    print(f"Packets: {len(rows)} total, {len(active_rows)} active")
    print_capture_identity(summary_rows)
    print_time_window(summary_rows)
    print_basic_stats(summary_rows)
    print_balance_diagnostics(summary_rows)
    print_suspension_stats(summary_rows)
    print_slip_stats(summary_rows)
    print_landing_stats(summary_rows)
    print_smashable_stats(summary_rows)
    return 0


def read_capture(path: Path) -> Iterable[dict[str, Any]]:
    if path.suffix.lower() == ".csv":
        with path.open("r", newline="", encoding="utf-8") as handle:
            yield from csv.DictReader(handle)
        return

    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                yield json.loads(line)


def print_capture_identity(rows: list[dict[str, Any]]) -> None:
    def most_common(field: str) -> str:
        values = [str(row.get(field, "")) for row in rows if row.get(field, "") != ""]
        if not values:
            return "unknown"
        value, count = Counter(values).most_common(1)[0]
        return f"{value} ({count} packets)"

    print(
        "Car: "
        f"ordinal={most_common('CarOrdinal')}, "
        f"class={most_common('CarClass')}, "
        f"PI={most_common('CarPerformanceIndex')}, "
        f"drivetrain={most_common('DrivetrainType')}"
    )


def print_time_window(rows: list[dict[str, Any]]) -> None:
    monotonic = [as_float(row.get("_monotonic_s")) for row in rows if row.get("_monotonic_s") != ""]
    timestamps = [as_float(row.get("TimestampMS")) for row in rows if row.get("TimestampMS") != ""]
    duration = 0.0
    if monotonic:
        duration = max(monotonic) - min(monotonic)
    elif timestamps:
        duration = (max(timestamps) - min(timestamps)) / 1000.0
    hz = len(rows) / duration if duration > 0 else 0.0
    print(f"Window: {duration:.2f} s, effective sample rate {hz:.1f} Hz")


def print_basic_stats(rows: list[dict[str, Any]]) -> None:
    print("Basics:")
    for label, field, suffix in (
        ("Speed", "SpeedMph", "mph"),
        ("RPM", "CurrentEngineRpm", "rpm"),
        ("Throttle", "AccelPct", "%"),
        ("Brake", "BrakePct", "%"),
        ("Steer", "SteerPct", "%"),
        ("Yaw rate", "AngularVelocityY", "rad/s"),
        ("Pitch", "Pitch", "rad"),
        ("Roll", "Roll", "rad"),
    ):
        values = values_for(rows, field)
        if values:
            print_stat_line(label, values, suffix=suffix)


def print_balance_diagnostics(rows: list[dict[str, Any]]) -> None:
    cornering = [
        row
        for row in rows
        if as_float(row.get("SpeedMph")) > 15.0 and abs(as_float(row.get("SteerPct"))) > 25.0
    ]
    throttle_cornering = [row for row in cornering if as_float(row.get("AccelPct")) > 40.0]
    braking_cornering = [row for row in cornering if as_float(row.get("BrakePct")) > 10.0]
    drift_window = [
        row
        for row in rows
        if as_float(row.get("SpeedMph")) > 10.0
        and abs(as_float(row.get("BetaDeg"))) > 8.0
        and as_float(row.get("RearCombinedSlip")) > as_float(row.get("FrontCombinedSlip"))
    ]

    print("Balance diagnostics:")
    if cornering:
        understeer = percentage(
            as_float(row.get("SlipBalance")) > 0.15 and as_float(row.get("YawResponse")) < 0.08
            for row in cornering
        )
        oversteer = percentage(
            as_float(row.get("SlipBalance")) < -0.15 and abs(as_float(row.get("BetaDeg"))) > 8.0
            for row in cornering
        )
        print(f"  Cornering samples: {len(cornering)}")
        print(f"  Understeer proxy: {understeer:.1f}% of cornering samples")
        print(f"  Oversteer proxy: {oversteer:.1f}% of cornering samples")
        print_stat_line("  Slip balance", values_for(cornering, "SlipBalance"))
        print_stat_line("  Body slip beta", values_for(cornering, "BetaDeg"), suffix="deg")
        print_stat_line("  Yaw response", values_for(cornering, "YawResponse"))
    else:
        print("  No useful cornering samples captured.")

    if braking_cornering:
        entry_understeer = percentage(
            as_float(row.get("SlipBalance")) > 0.15 and as_float(row.get("AccelPct")) < 20.0
            for row in braking_cornering
        )
        print(
            f"  Entry understeer proxy: {entry_understeer:.1f}% "
            f"of {len(braking_cornering)} braking-corner samples"
        )

    if throttle_cornering:
        exit_understeer = percentage(
            as_float(row.get("SlipBalance")) > 0.15 and as_float(row.get("YawResponse")) < 0.08
            for row in throttle_cornering
        )
        power_oversteer = percentage(
            as_float(row.get("SlipBalance")) < -0.15 and as_float(row.get("RearCombinedSlip")) > 0.6
            for row in throttle_cornering
        )
        print(
            f"  Exit understeer proxy: {exit_understeer:.1f}% "
            f"of {len(throttle_cornering)} throttle-corner samples"
        )
        print(
            f"  Power oversteer proxy: {power_oversteer:.1f}% "
            f"of {len(throttle_cornering)} throttle-corner samples"
        )

    if drift_window:
        print(
            f"  Drift/slide window: {len(drift_window)} samples, "
            f"avg beta {average(values_for(drift_window, 'BetaDeg')):.1f} deg"
        )


def print_suspension_stats(rows: list[dict[str, Any]]) -> None:
    print("Suspension normalized travel (0 = full stretch, 1 = full compression):")
    for corner in CORNERS:
        field = "NormalizedSuspensionTravel" + corner
        values = values_for(rows, field)
        if not values:
            continue
        compressed = percentage(abs(value) >= 0.95 for value in values)
        extended = percentage(abs(value) <= 0.05 for value in values)
        print(
            f"  {CORNER_LABELS[corner]}: "
            f"min={min(values):.3f} avg={average(values):.3f} max={max(values):.3f} "
            f">=0.95 {compressed:.1f}% <=0.05 {extended:.1f}%"
        )
    print_stat_line("  Front minus rear travel", values_for(rows, "TravelBias"))
    print_stat_line("  Diagonal twist", values_for(rows, "DiagonalTravel"))
    print_stat_line("  Left minus right travel", values_for(rows, "LeftRightTravel"))


def print_slip_stats(rows: list[dict[str, Any]]) -> None:
    for group, label in (
        ("TireCombinedSlip", "Combined tire slip"),
        ("TireSlipAngle", "Slip angle"),
        ("TireSlipRatio", "Slip ratio"),
    ):
        print(f"{label} (absolute values):")
        for corner in CORNERS:
            values = [abs(value) for value in values_for(rows, group + corner)]
            if not values:
                continue
            over_one = percentage(value >= 1.0 for value in values)
            print(
                f"  {CORNER_LABELS[corner]}: "
                f"avg={average(values):.3f} max={max(values):.3f} >=1.0 {over_one:.1f}%"
            )


def print_landing_stats(rows: list[dict[str, Any]]) -> None:
    bottoming = [row for row in rows if as_int(row.get("AnyBottoming"))]
    airborne = [row for row in rows if as_int(row.get("AirborneProxy"))]
    front_heavy = [
        row
        for row in rows
        if as_float(row.get("TravelBias")) > 0.20 and as_float(row.get("FrontTravel")) > 0.60
    ]
    roll_biased = [row for row in rows if abs(as_float(row.get("LeftRightTravel"))) > 0.25]

    print("Landing and travel diagnostics:")
    print(f"  Bottoming samples: {len(bottoming)} ({len(bottoming) / len(rows) * 100.0:.1f}%)")
    print(f"  Airborne proxy samples: {len(airborne)} ({len(airborne) / len(rows) * 100.0:.1f}%)")
    print(
        f"  Nose-heavy compression samples: {len(front_heavy)} "
        f"({len(front_heavy) / len(rows) * 100.0:.1f}%)"
    )
    print(
        f"  Roll-biased compression samples: {len(roll_biased)} "
        f"({len(roll_biased) / len(rows) * 100.0:.1f}%)"
    )
    if bottoming:
        print_stat_line("  Bottoming speed", values_for(bottoming, "SpeedMph"), suffix="mph")


def print_smashable_stats(rows: list[dict[str, Any]]) -> None:
    impacts = [
        row
        for row in rows
        if abs(as_float(row.get("SmashableVelDiff"))) > 0.01
        or abs(as_float(row.get("SmashableMass"))) > 0.01
    ]
    print(f"Smashable hits: {len(impacts)} packets with nonzero FH6 smashable data")
    if impacts:
        print_stat_line("  Velocity loss", values_for(impacts, "SmashableVelDiff"), suffix="m/s")
        print_stat_line("  Mass", values_for(impacts, "SmashableMass"), suffix="kg")
        print_stat_line("  Speed during hits", values_for(impacts, "SpeedMph"), suffix="mph")


def values_for(rows: Iterable[dict[str, Any]], field: str) -> list[float]:
    values: list[float] = []
    for row in rows:
        value = row.get(field)
        if value is None or value == "":
            continue
        number = as_float(value, default=float("nan"))
        if math.isfinite(number):
            values.append(number)
    return values


def print_stat_line(label: str, values: list[float], suffix: str = "") -> None:
    suffix = f" {suffix}" if suffix else ""
    print(
        f"  {label}: min={min(values):.2f}{suffix} "
        f"avg={average(values):.2f}{suffix} max={max(values):.2f}{suffix}"
    )


def average(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def percentage(flags: Iterable[bool]) -> float:
    total = 0
    hits = 0
    for flag in flags:
        total += 1
        hits += 1 if flag else 0
    return hits / total * 100.0 if total else 0.0


def command_self_test(_: argparse.Namespace) -> int:
    values: list[Any] = []
    for index, field in enumerate(FIELDS):
        if field.code == "f":
            values.append(float(index) + 0.25)
        elif field.code in {"b", "B"}:
            values.append(max(-100, min(100, index)))
        else:
            values.append(index)
    full_data = PACKET_STRUCT.pack(*values)

    full_packet = parse_packet(full_data)
    assert len(full_data) == PACKET_SIZE
    assert "SpeedMph" in full_packet
    assert full_packet["_packet_size"] == PACKET_SIZE
    try:
        parse_packet(full_data[:-1])
    except PacketSizeError:
        pass
    else:
        raise AssertionError("truncated 323-byte packet was accepted")
    print(f"Self-test passed: official packet size={PACKET_SIZE} bytes.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Listen for, decode, and summarize Forza Horizon 6 Data Out UDP packets."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    listen = subparsers.add_parser("listen", help="Listen on a UDP port and record packets")
    listen.add_argument("--host", default="127.0.0.1", help="UDP bind host")
    listen.add_argument("--port", type=int, default=5311, help="UDP bind port")
    listen.add_argument("--duration", type=float, default=0.0, help="Seconds to listen; 0 means until Ctrl+C")
    listen.add_argument("--label", default="", help="Capture label stored on each row")
    listen.add_argument("--output-dir", default="telemetry", help="Directory for default captures")
    listen.add_argument("--jsonl", help="Explicit JSONL capture path")
    listen.add_argument("--csv", help="Optional CSV capture path")
    listen.add_argument("--no-save", action="store_true", help="Only print live summaries")
    listen.add_argument("--save-hz", type=float, default=0.0, help="Maximum save rate; 0 saves every packet")
    listen.add_argument("--summary-every", type=float, default=1.0, help="Console summary interval in seconds")
    listen.add_argument("--socket-timeout", type=float, default=0.5, help="UDP receive timeout in seconds")
    listen.set_defaults(func=command_listen)

    schema = subparsers.add_parser("schema", help="Print the local packet schema")
    schema.add_argument("--markdown", action="store_true", help="Print as a Markdown table")
    schema.add_argument("--no-padding", dest="include_padding", action="store_false", help="Hide the final padding byte")
    schema.set_defaults(func=command_schema, include_padding=True)

    summary = subparsers.add_parser("summary", help="Summarize a JSONL or CSV capture")
    summary.add_argument("capture", help="Capture path")
    summary.set_defaults(func=command_summary)

    self_test = subparsers.add_parser("self-test", help="Run parser sanity checks")
    self_test.set_defaults(func=command_self_test)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
