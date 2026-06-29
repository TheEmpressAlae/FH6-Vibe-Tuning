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

KNOWN_CAR_SLUGS = {
    1045: "1987-pontiac-firebird-trans-am-gta",
    3249: "2007-formula-drift-117-599-gtb-fiorano",
    3852: "1991-honda-beat",
    4197: "1994-mazda-mx-5-miata-forza-edition",
}

CLASS_SLUGS = {
    0: "d",
    1: "c",
    2: "b",
    3: "a",
    4: "s1",
    5: "s2",
    6: "r",
    7: "x",
}

DRIVETRAIN_SLUGS = {
    0: "fwd",
    1: "rwd",
    2: "awd",
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


def full_safe_slug(value: str) -> str:
    slug = "".join(char.lower() if char.isalnum() else "-" for char in value)
    slug = "-".join(part for part in slug.split("-") if part)
    return slug or "capture"


def capture_identity_slug(
    car_ordinal: Any,
    car_class: Any,
    pi: Any,
    drivetrain: Any,
) -> str:
    ordinal = as_int(car_ordinal, default=-1)
    class_id = as_int(car_class, default=-1)
    drivetrain_id = as_int(drivetrain, default=-1)

    car_slug = KNOWN_CAR_SLUGS.get(ordinal, f"car-{ordinal}" if ordinal >= 0 else "car-unknown")
    class_slug = CLASS_SLUGS.get(class_id, f"class{class_id}" if class_id >= 0 else "class-unknown")
    pi_slug = str(as_int(pi, default=0)) if str(pi) != "" else "pi-unknown"
    drive_slug = DRIVETRAIN_SLUGS.get(
        drivetrain_id, f"drive{drivetrain_id}" if drivetrain_id >= 0 else "drive-unknown"
    )

    return full_safe_slug(f"{car_slug}-{class_slug}-{pi_slug}-{drive_slug}")


def effective_capture_label(row_label: str, identity_slug: str) -> str:
    label = (row_label or "").strip()
    if not label:
        return identity_slug

    normalized = full_safe_slug(label)
    if normalized.startswith("capture-") or normalized == "capture":
        return identity_slug
    if normalized.startswith("miata-drag") and "miata" not in identity_slug:
        return identity_slug

    return label


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


def command_analyze(args: argparse.Namespace) -> int:
    analyses = [analyze_capture(Path(capture)) for capture in args.captures]
    baseline = None
    if args.baseline:
        baseline_path = Path(args.baseline).resolve()
        baseline = next(
            (
                analysis
                for analysis in analyses
                if Path(analysis["path"]).resolve() == baseline_path
            ),
            None,
        )
        if baseline is None:
            baseline = analyze_capture(Path(args.baseline))

    result: dict[str, Any] = {
        "generated_utc": utc_now_iso(),
        "baseline": baseline["path"] if baseline else "",
        "captures": analyses if args.full else [analysis_brief(analysis) for analysis in analyses],
    }
    if baseline:
        result["deltas"] = [analysis_delta(analysis, baseline) for analysis in analyses]

    output = json.dumps(clean_for_json(result), separators=(",", ":"), allow_nan=False)
    if args.json:
        json_path = Path(args.json)
        json_path.parent.mkdir(parents=True, exist_ok=True)
        json_path.write_text(output + "\n", encoding="utf-8")
    else:
        print(output)
    return 0


def command_breakaway(args: argparse.Namespace) -> int:
    path = Path(args.capture)
    rows = list(read_capture(path))
    for row in rows:
        add_derived_fields(row)

    active_rows = [row for row in rows if as_int(row.get("IsRaceOn")) == 1]
    analysis_rows = active_rows or rows
    if not analysis_rows:
        print(f"No rows found in {path}")
        return 1

    kick = find_breakaway_index(
        analysis_rows,
        min_speed_mph=args.min_speed_mph,
        min_throttle_pct=args.min_throttle_pct,
        min_beta_deg=args.min_beta_deg,
        min_rear_slip=args.min_rear_slip,
        rear_slip_margin=args.rear_slip_margin,
        sustain_samples=args.sustain_samples,
    )
    if kick is None:
        print(f"No sustained breakaway window found in {path}")
        return 2

    kick_index, kick_reason = kick
    kick_row = analysis_rows[kick_index]
    kick_time = row_time_seconds(kick_row)
    windows = breakaway_windows(
        analysis_rows,
        kick_time,
        before_seconds=args.before_seconds,
        after_seconds=args.after_seconds,
    )
    result = {
        "generated_utc": utc_now_iso(),
        "path": str(path),
        "row_count": len(rows),
        "active_count": len(active_rows),
        "kick": breakaway_marker(kick_index, kick_reason, kick_row),
        "windows": {
            name: breakaway_window_summary(window_rows)
            for name, window_rows in windows.items()
        },
    }

    output = json.dumps(clean_for_json(result), separators=(",", ":"), allow_nan=False)
    if args.json:
        json_path = Path(args.json)
        json_path.parent.mkdir(parents=True, exist_ok=True)
        json_path.write_text(output + "\n", encoding="utf-8")
    else:
        print(output)
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


def analyze_capture(path: Path) -> dict[str, Any]:
    rows = list(read_capture(path))
    for row in rows:
        add_derived_fields(row)

    active_rows = [row for row in rows if as_int(row.get("IsRaceOn")) == 1]
    analysis_rows = active_rows or rows
    if not analysis_rows:
        return {
            "path": str(path),
            "row_count": 0,
            "active_count": 0,
            "error": "no rows found",
        }

    moving = [row for row in analysis_rows if as_float(row.get("SpeedMph")) > 10.0]
    cornering = [
        row
        for row in analysis_rows
        if as_float(row.get("SpeedMph")) > 15.0
        and abs(as_float(row.get("SteerPct"))) > 25.0
    ]
    throttle_cornering = [
        row for row in cornering if as_float(row.get("AccelPct")) > 40.0
    ]
    drift_window = [
        row
        for row in analysis_rows
        if as_float(row.get("SpeedMph")) > 10.0
        and abs(as_float(row.get("BetaDeg"))) > 8.0
        and as_float(row.get("RearCombinedSlip")) > as_float(row.get("FrontCombinedSlip"))
    ]

    duration = capture_duration_seconds(analysis_rows)
    gear_counts = Counter(str(as_int(row.get("Gear"))) for row in analysis_rows)
    events = {
        "full_throttle_pct": rate(
            as_float(row.get("AccelPct")) >= 98.0 for row in analysis_rows
        ),
        "near_zero_throttle_pct": rate(
            as_float(row.get("AccelPct")) <= 5.0 for row in analysis_rows
        ),
        "brake_used_pct": rate(
            as_float(row.get("BrakePct")) > 5.0 for row in analysis_rows
        ),
        "handbrake_used_pct": rate(
            as_float(row.get("HandBrakePct")) > 5.0 for row in analysis_rows
        ),
        "steering_lock_moving_pct": rate(
            abs(as_float(row.get("SteerPct"))) >= 90.0 for row in moving
        ),
        "rear_slip_ge_10_pct": rate(
            as_float(row.get("RearCombinedSlip")) >= 10.0 for row in analysis_rows
        ),
        "front_slip_ge_5_pct": rate(
            as_float(row.get("FrontCombinedSlip")) >= 5.0 for row in analysis_rows
        ),
        "bottoming_pct": rate(
            as_int(row.get("AnyBottoming")) == 1 for row in analysis_rows
        ),
        "airborne_proxy_pct": rate(
            as_int(row.get("AirborneProxy")) == 1 for row in analysis_rows
        ),
    }

    row_label = most_common_value(analysis_rows, "_label")
    car_ordinal = most_common_value(analysis_rows, "CarOrdinal")
    car_class = most_common_value(analysis_rows, "CarClass")
    pi = most_common_value(analysis_rows, "CarPerformanceIndex")
    drivetrain = most_common_value(analysis_rows, "DrivetrainType")
    identity_slug = capture_identity_slug(car_ordinal, car_class, pi, drivetrain)
    label = effective_capture_label(row_label, identity_slug)

    analysis = {
        "path": str(path),
        "identity": {
            "label": label,
            "row_label": row_label,
            "identity_slug": identity_slug,
            "car_ordinal": car_ordinal,
            "car_class": car_class,
            "pi": pi,
            "drivetrain": drivetrain,
        },
        "row_count": len(rows),
        "active_count": len(active_rows),
        "analysis_count": len(analysis_rows),
        "duration_s": duration,
        "sample_rate_hz": len(analysis_rows) / duration if duration > 0 else 0.0,
        "windows": {
            "moving": len(moving),
            "cornering": len(cornering),
            "throttle_cornering": len(throttle_cornering),
            "drift": len(drift_window),
        },
        "gear_counts": dict(
            sorted(gear_counts.items(), key=lambda item: as_int(item[0]))
        ),
        "speed_mph": stat_summary(analysis_rows, "SpeedMph"),
        "rpm": stat_summary(analysis_rows, "CurrentEngineRpm"),
        "throttle_pct": stat_summary(analysis_rows, "AccelPct"),
        "brake_pct": stat_summary(analysis_rows, "BrakePct"),
        "steer_pct_abs": stat_summary(analysis_rows, "SteerPct", absolute=True),
        "beta_deg": stat_summary(analysis_rows, "BetaDeg"),
        "beta_deg_abs": stat_summary(analysis_rows, "BetaDeg", absolute=True),
        "yaw_response": stat_summary(cornering, "YawResponse"),
        "front_combined_slip": stat_summary(analysis_rows, "FrontCombinedSlip"),
        "rear_combined_slip": stat_summary(analysis_rows, "RearCombinedSlip"),
        "slip_balance": stat_summary(analysis_rows, "SlipBalance"),
        "front_combined_slip_drift": stat_summary(drift_window, "FrontCombinedSlip"),
        "rear_combined_slip_drift": stat_summary(drift_window, "RearCombinedSlip"),
        "front_slip_angle_abs": stat_summary_corners(
            analysis_rows, "TireSlipAngle", ("FrontLeft", "FrontRight")
        ),
        "rear_slip_angle_abs": stat_summary_corners(
            analysis_rows, "TireSlipAngle", ("RearLeft", "RearRight")
        ),
        "front_slip_ratio_abs": stat_summary_corners(
            analysis_rows, "TireSlipRatio", ("FrontLeft", "FrontRight")
        ),
        "rear_slip_ratio_abs": stat_summary_corners(
            analysis_rows, "TireSlipRatio", ("RearLeft", "RearRight")
        ),
        "front_tire_temp": stat_summary_corners(
            analysis_rows, "TireTemp", ("FrontLeft", "FrontRight")
        ),
        "rear_tire_temp": stat_summary_corners(
            analysis_rows, "TireTemp", ("RearLeft", "RearRight")
        ),
        "front_travel": stat_summary(analysis_rows, "FrontTravel"),
        "rear_travel": stat_summary(analysis_rows, "RearTravel"),
        "travel_bias": stat_summary(analysis_rows, "TravelBias"),
        "diagonal_travel_abs": stat_summary(
            analysis_rows, "DiagonalTravel", absolute=True
        ),
        "events": events,
        "launch": launch_metrics(analysis_rows),
    }
    analysis["flags"] = analysis_flags(analysis)
    return analysis


def analysis_delta(analysis: dict[str, Any], baseline: dict[str, Any]) -> dict[str, Any]:
    return {
        "path": analysis.get("path", ""),
        "vs": baseline.get("path", ""),
        "speed_avg_mph": delta_metric(analysis, baseline, "speed_mph", "avg"),
        "speed_max_mph": delta_metric(analysis, baseline, "speed_mph", "max"),
        "rear_slip_avg": delta_metric(analysis, baseline, "rear_combined_slip", "avg"),
        "rear_slip_p95": delta_metric(analysis, baseline, "rear_combined_slip", "p95"),
        "front_slip_avg": delta_metric(analysis, baseline, "front_combined_slip", "avg"),
        "front_slip_p95": delta_metric(analysis, baseline, "front_combined_slip", "p95"),
        "abs_beta_avg_deg": delta_metric(analysis, baseline, "beta_deg_abs", "avg"),
        "steering_lock_moving_pct": delta_event(
            analysis, baseline, "steering_lock_moving_pct"
        ),
        "bottoming_pct": delta_event(analysis, baseline, "bottoming_pct"),
        "full_throttle_pct": delta_event(analysis, baseline, "full_throttle_pct"),
    }


def analysis_brief(analysis: dict[str, Any]) -> dict[str, Any]:
    return {
        "path": analysis.get("path", ""),
        "label": analysis.get("identity", {}).get("label", ""),
        "row_label": analysis.get("identity", {}).get("row_label", ""),
        "identity_slug": analysis.get("identity", {}).get("identity_slug", ""),
        "car": {
            "ordinal": analysis.get("identity", {}).get("car_ordinal", ""),
            "class": analysis.get("identity", {}).get("car_class", ""),
            "pi": analysis.get("identity", {}).get("pi", ""),
            "drivetrain": analysis.get("identity", {}).get("drivetrain", ""),
        },
        "samples": {
            "rows": analysis.get("analysis_count", 0),
            "seconds": analysis.get("duration_s", 0.0),
            "hz": analysis.get("sample_rate_hz", 0.0),
            "windows": analysis.get("windows", {}),
        },
        "gear_counts": analysis.get("gear_counts", {}),
        "speed_mph": analysis.get("speed_mph", {}),
        "throttle": {
            "avg_pct": analysis.get("throttle_pct", {}).get("avg", 0.0),
            "full_pct": analysis.get("events", {}).get("full_throttle_pct", 0.0),
            "zero_pct": analysis.get("events", {}).get("near_zero_throttle_pct", 0.0),
        },
        "steering": {
            "abs_avg_pct": analysis.get("steer_pct_abs", {}).get("avg", 0.0),
            "lock_moving_pct": analysis.get("events", {}).get("steering_lock_moving_pct", 0.0),
        },
        "body_slip_abs_deg": analysis.get("beta_deg_abs", {}),
        "combined_slip": {
            "front": analysis.get("front_combined_slip", {}),
            "rear": analysis.get("rear_combined_slip", {}),
            "front_drift": analysis.get("front_combined_slip_drift", {}),
            "rear_drift": analysis.get("rear_combined_slip_drift", {}),
        },
        "slip_ratio_abs": {
            "front": analysis.get("front_slip_ratio_abs", {}),
            "rear": analysis.get("rear_slip_ratio_abs", {}),
        },
        "tire_temp": {
            "front": analysis.get("front_tire_temp", {}),
            "rear": analysis.get("rear_tire_temp", {}),
        },
        "travel": {
            "front": analysis.get("front_travel", {}),
            "rear": analysis.get("rear_travel", {}),
            "bias": analysis.get("travel_bias", {}),
            "bottoming_pct": analysis.get("events", {}).get("bottoming_pct", 0.0),
            "airborne_proxy_pct": analysis.get("events", {}).get("airborne_proxy_pct", 0.0),
        },
        "brakes": {
            "brake_used_pct": analysis.get("events", {}).get("brake_used_pct", 0.0),
            "handbrake_used_pct": analysis.get("events", {}).get("handbrake_used_pct", 0.0),
        },
        "launch": analysis.get("launch", {}),
        "flags": analysis.get("flags", []),
    }


def most_common_value(rows: list[dict[str, Any]], field: str) -> str:
    values = [str(row.get(field, "")) for row in rows if str(row.get(field, "")) != ""]
    if not values:
        return ""
    return Counter(values).most_common(1)[0][0]


def capture_duration_seconds(rows: list[dict[str, Any]]) -> float:
    monotonic = [
        as_float(row.get("_monotonic_s"))
        for row in rows
        if row.get("_monotonic_s") not in (None, "")
    ]
    if monotonic:
        return max(monotonic) - min(monotonic)

    timestamps = [
        as_float(row.get("TimestampMS"))
        for row in rows
        if row.get("TimestampMS") not in (None, "")
    ]
    if timestamps:
        return (max(timestamps) - min(timestamps)) / 1000.0
    return 0.0


def stat_summary(
    rows: Iterable[dict[str, Any]], field: str, absolute: bool = False
) -> dict[str, float]:
    values = values_for(rows, field)
    if absolute:
        values = [abs(value) for value in values]
    if not values:
        return empty_stats()
    values = sorted(values)
    return {
        "avg": average(values),
        "p95": percentile(values, 95.0),
        "max": values[-1],
    }


def stat_summary_corners(
    rows: Iterable[dict[str, Any]], prefix: str, corners: tuple[str, ...]
) -> dict[str, float]:
    values: list[float] = []
    for row in rows:
        for corner in corners:
            value = row.get(prefix + corner)
            if value is None or value == "":
                continue
            number = as_float(value, default=float("nan"))
            if math.isfinite(number):
                values.append(abs(number))
    if not values:
        return empty_stats()
    values = sorted(values)
    return {
        "avg": average(values),
        "p95": percentile(values, 95.0),
        "max": values[-1],
    }


def empty_stats() -> dict[str, float]:
    return {"avg": 0.0, "p95": 0.0, "max": 0.0}


def percentile(sorted_values: list[float], percentile_value: float) -> float:
    if not sorted_values:
        return 0.0
    if len(sorted_values) == 1:
        return sorted_values[0]
    index = (len(sorted_values) - 1) * percentile_value / 100.0
    lower = math.floor(index)
    upper = math.ceil(index)
    if lower == upper:
        return sorted_values[int(index)]
    weight = index - lower
    return sorted_values[lower] * (1.0 - weight) + sorted_values[upper] * weight


def rate(flags: Iterable[bool]) -> float:
    return percentage(flags)


def launch_metrics(rows: list[dict[str, Any]]) -> dict[str, Any]:
    timed_rows = [(row_time_seconds(row), row) for row in rows]
    timed_rows = [(seconds, row) for seconds, row in timed_rows if seconds is not None]
    if not timed_rows:
        return {"detected": False, "time_to_mph": {}}

    start_index = None
    for index, (_, row) in enumerate(timed_rows):
        if as_float(row.get("SpeedMph")) <= 3.0 and as_float(row.get("AccelPct")) >= 50.0:
            start_index = index
            break
    if start_index is None:
        return {"detected": False, "time_to_mph": {}}

    start_time, start_row = timed_rows[start_index]
    thresholds = (5, 20, 30, 40, 50, 60, 100)
    time_to_mph: dict[str, float | None] = {}
    for threshold in thresholds:
        hit = next(
            (
                seconds - start_time
                for seconds, row in timed_rows[start_index:]
                if as_float(row.get("SpeedMph")) >= threshold
            ),
            None,
        )
        time_to_mph[str(threshold)] = hit

    return {
        "detected": True,
        "start_time_s": start_time,
        "start_speed_mph": as_float(start_row.get("SpeedMph")),
        "start_throttle_pct": as_float(start_row.get("AccelPct")),
        "time_to_mph": time_to_mph,
    }


def row_time_seconds(row: dict[str, Any]) -> float | None:
    if row.get("_monotonic_s") not in (None, ""):
        return as_float(row.get("_monotonic_s"))
    if row.get("TimestampMS") not in (None, ""):
        return as_float(row.get("TimestampMS")) / 1000.0
    return None


def find_breakaway_index(
    rows: list[dict[str, Any]],
    min_speed_mph: float,
    min_throttle_pct: float,
    min_beta_deg: float,
    min_rear_slip: float,
    rear_slip_margin: float,
    sustain_samples: int,
) -> tuple[int, str] | None:
    checks = (
        (
            "power_oversteer",
            lambda row: (
                as_float(row.get("SpeedMph")) >= min_speed_mph
                and as_float(row.get("AccelPct")) >= min_throttle_pct
                and abs(as_float(row.get("BetaDeg"))) >= min_beta_deg
                and as_float(row.get("RearCombinedSlip")) >= min_rear_slip
                and as_float(row.get("RearCombinedSlip"))
                > as_float(row.get("FrontCombinedSlip")) + rear_slip_margin
            ),
        ),
        (
            "rear_slip_dominant",
            lambda row: (
                as_float(row.get("SpeedMph")) >= min_speed_mph
                and as_float(row.get("RearCombinedSlip")) >= min_rear_slip
                and as_float(row.get("RearCombinedSlip"))
                > as_float(row.get("FrontCombinedSlip")) + rear_slip_margin
            ),
        ),
        (
            "rear_slip_ratio",
            lambda row: (
                as_float(row.get("SpeedMph")) >= min_speed_mph
                and as_float(row.get("AccelPct")) >= min_throttle_pct
                and rear_slip_ratio_abs(row) >= 1.0
            ),
        ),
        (
            "body_angle",
            lambda row: (
                as_float(row.get("SpeedMph")) >= min_speed_mph
                and abs(as_float(row.get("BetaDeg"))) >= min_beta_deg
            ),
        ),
    )
    for name, check in checks:
        index = first_sustained_index(rows, check, sustain_samples)
        if index is not None:
            return index, name
    return None


def first_sustained_index(
    rows: list[dict[str, Any]], check: Any, sustain_samples: int
) -> int | None:
    run_start: int | None = None
    run_count = 0
    for index, row in enumerate(rows):
        if check(row):
            if run_start is None:
                run_start = index
            run_count += 1
            if run_count >= sustain_samples:
                return run_start
        else:
            run_start = None
            run_count = 0
    return None


def breakaway_windows(
    rows: list[dict[str, Any]],
    kick_time: float | None,
    before_seconds: float,
    after_seconds: float,
) -> dict[str, list[dict[str, Any]]]:
    if kick_time is None:
        return {
            "before_kick": [],
            "pre_kick": [],
            "kick": [],
            "after_kick": [],
        }

    return {
        "before_kick": [
            row for row in rows if (row_time_seconds(row) or 0.0) < kick_time
        ],
        "pre_kick": [
            row
            for row in rows
            if kick_time - before_seconds <= (row_time_seconds(row) or 0.0) < kick_time
        ],
        "kick": [
            row
            for row in rows
            if kick_time <= (row_time_seconds(row) or 0.0) < kick_time + after_seconds
        ],
        "after_kick": [
            row
            for row in rows
            if (row_time_seconds(row) or 0.0) >= kick_time + after_seconds
        ],
    }


def breakaway_marker(index: int, reason: str, row: dict[str, Any]) -> dict[str, Any]:
    return {
        "index": index,
        "reason": reason,
        "time_s": row_time_seconds(row),
        "speed_mph": as_float(row.get("SpeedMph")),
        "throttle_pct": as_float(row.get("AccelPct")),
        "brake_pct": as_float(row.get("BrakePct")),
        "handbrake_pct": as_float(row.get("HandBrakePct")),
        "steer_pct": as_float(row.get("SteerPct")),
        "beta_deg": as_float(row.get("BetaDeg")),
        "front_combined_slip": as_float(row.get("FrontCombinedSlip")),
        "rear_combined_slip": as_float(row.get("RearCombinedSlip")),
        "front_slip_ratio_abs": front_slip_ratio_abs(row),
        "rear_slip_ratio_abs": rear_slip_ratio_abs(row),
    }


def breakaway_window_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    if not rows:
        return {"count": 0}

    times = [time for row in rows if (time := row_time_seconds(row)) is not None]
    front_gt_rear = sum(
        1
        for row in rows
        if as_float(row.get("FrontCombinedSlip")) > as_float(row.get("RearCombinedSlip"))
    )
    rear_gt_front = sum(
        1
        for row in rows
        if as_float(row.get("RearCombinedSlip")) > as_float(row.get("FrontCombinedSlip"))
    )
    return {
        "count": len(rows),
        "start_s": min(times) if times else None,
        "end_s": max(times) if times else None,
        "speed_mph": stat_summary(rows, "SpeedMph"),
        "throttle_pct": stat_summary(rows, "AccelPct"),
        "steer_pct_abs": stat_summary(rows, "SteerPct", absolute=True),
        "beta_deg_abs": stat_summary(rows, "BetaDeg", absolute=True),
        "front_combined_slip": stat_summary(rows, "FrontCombinedSlip"),
        "rear_combined_slip": stat_summary(rows, "RearCombinedSlip"),
        "front_slip_ratio_abs": stat_summary_custom(rows, front_slip_ratio_abs),
        "rear_slip_ratio_abs": stat_summary_custom(rows, rear_slip_ratio_abs),
        "front_gt_rear_pct": front_gt_rear / len(rows) * 100.0,
        "rear_gt_front_pct": rear_gt_front / len(rows) * 100.0,
        "brake_max_pct": max(as_float(row.get("BrakePct")) for row in rows),
        "handbrake_max_pct": max(as_float(row.get("HandBrakePct")) for row in rows),
        "bottoming_pct": percentage(as_int(row.get("AnyBottoming")) == 1 for row in rows),
        "airborne_proxy_pct": percentage(
            as_int(row.get("AirborneProxy")) == 1 for row in rows
        ),
    }


def front_slip_ratio_abs(row: dict[str, Any]) -> float:
    return average(
        [
            abs(as_float(row.get("TireSlipRatioFrontLeft"))),
            abs(as_float(row.get("TireSlipRatioFrontRight"))),
        ]
    )


def rear_slip_ratio_abs(row: dict[str, Any]) -> float:
    return average(
        [
            abs(as_float(row.get("TireSlipRatioRearLeft"))),
            abs(as_float(row.get("TireSlipRatioRearRight"))),
        ]
    )


def stat_summary_custom(
    rows: Iterable[dict[str, Any]], getter: Any
) -> dict[str, float]:
    values = sorted(getter(row) for row in rows)
    if not values:
        return empty_stats()
    return {
        "avg": average(values),
        "p95": percentile(values, 95.0),
        "max": values[-1],
    }


def analysis_flags(analysis: dict[str, Any]) -> list[str]:
    flags: list[str] = []
    windows = analysis.get("windows", {})
    events = analysis.get("events", {})
    front_slip = analysis.get("front_combined_slip", {})
    rear_slip = analysis.get("rear_combined_slip", {})

    if windows.get("drift", 0) > 0:
        flags.append("drift-window")
    if events.get("steering_lock_moving_pct", 0.0) >= 50.0:
        flags.append("heavy-steering-lock")
    if rear_slip.get("avg", 0.0) >= front_slip.get("avg", 0.0) * 2.0 and rear_slip.get("avg", 0.0) > 1.0:
        flags.append("rear-slip-dominant")
    if events.get("front_slip_ge_5_pct", 0.0) >= 10.0:
        flags.append("front-saturation")
    if events.get("rear_slip_ge_10_pct", 0.0) >= 10.0:
        flags.append("rear-runaway-slip")
    if events.get("bottoming_pct", 0.0) > 2.0:
        flags.append("bottoming")
    if events.get("brake_used_pct", 0.0) <= 1.0 and events.get("handbrake_used_pct", 0.0) <= 1.0:
        flags.append("no-brake-handbrake")
    return flags


def delta_metric(
    analysis: dict[str, Any], baseline: dict[str, Any], metric: str, field: str
) -> float:
    return (
        analysis.get(metric, {}).get(field, 0.0)
        - baseline.get(metric, {}).get(field, 0.0)
    )


def delta_event(analysis: dict[str, Any], baseline: dict[str, Any], field: str) -> float:
    return (
        analysis.get("events", {}).get(field, 0.0)
        - baseline.get("events", {}).get(field, 0.0)
    )


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

    analyze = subparsers.add_parser("analyze", help="Emit compact JSON metrics for one or more captures")
    analyze.add_argument("captures", nargs="+", help="Capture paths")
    analyze.add_argument("--baseline", help="Capture to use for delta metrics")
    analyze.add_argument("--json", help="Optional output JSON path; stdout stays quiet when set")
    analyze.add_argument("--full", action="store_true", help="Include all local metrics instead of the brief comparison view")
    analyze.set_defaults(func=command_analyze)

    breakaway = subparsers.add_parser("breakaway", help="Split a drift pull around sustained rear breakaway")
    breakaway.add_argument("capture", help="Capture path")
    breakaway.add_argument("--json", help="Optional output JSON path; stdout stays quiet when set")
    breakaway.add_argument("--min-speed-mph", type=float, default=25.0)
    breakaway.add_argument("--min-throttle-pct", type=float, default=50.0)
    breakaway.add_argument("--min-beta-deg", type=float, default=8.0)
    breakaway.add_argument("--min-rear-slip", type=float, default=1.0)
    breakaway.add_argument("--rear-slip-margin", type=float, default=0.35)
    breakaway.add_argument("--sustain-samples", type=int, default=12)
    breakaway.add_argument("--before-seconds", type=float, default=1.0)
    breakaway.add_argument("--after-seconds", type=float, default=1.0)
    breakaway.set_defaults(func=command_breakaway)

    self_test = subparsers.add_parser("self-test", help="Run parser sanity checks")
    self_test.set_defaults(func=command_self_test)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
