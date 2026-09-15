#!/usr/bin/env python3
"""Reproducible behavioral model for the Arduino motor protection logic."""
from dataclasses import dataclass
from typing import Optional

OVERCURRENT_A = 7.0
OVERTEMP_C = 75.0

@dataclass
class Sample:
    t_ms: int
    current_a: float
    temp_c: float
    sensor_healthy: bool = True

@dataclass
class Result:
    name: str
    detected_ms: Optional[int]
    cause: Optional[str]
    action: str
    samples: list[Sample]


def detect(name: str, samples: list[Sample]) -> Result:
    for sample in samples:
        if not sample.sensor_healthy:
            return Result(name, sample.t_ms, "SENSOR_MALFUNCTION", "CONTACTOR_OPEN", samples)
        if sample.current_a >= OVERCURRENT_A:
            return Result(name, sample.t_ms, "OVERCURRENT", "CONTACTOR_OPEN", samples)
        if sample.temp_c >= OVERTEMP_C:
            return Result(name, sample.t_ms, "OVERHEATING", "CONTACTOR_OPEN", samples)
    return Result(name, None, None, "MOTOR_REMAINS_ENERGIZED", samples)


def scenarios() -> list[Result]:
    return [
        detect("Overcurrent", [
            Sample(0, 2.1, 31.0), Sample(100, 2.3, 31.2), Sample(200, 8.4, 31.5),
        ]),
        detect("Overheating", [
            Sample(0, 3.0, 42.0), Sample(100, 3.1, 74.4), Sample(200, 3.1, 76.2),
        ]),
        detect("Sensor malfunction", [
            Sample(0, 2.7, 35.0), Sample(100, 2.8, 35.1, sensor_healthy=False),
        ]),
    ]


def main() -> None:
    print("Motor Fault-Detection & Protection System - scenario run")
    print("Thresholds: current >= %.1f A | temperature >= %.1f C" % (OVERCURRENT_A, OVERTEMP_C))
    print("-" * 72)
    for result in scenarios():
        print(f"SCENARIO: {result.name}")
        for sample in result.samples:
            health = "OK" if sample.sensor_healthy else "OPEN/INVALID"
            print(f"  t={sample.t_ms:>4} ms | I={sample.current_a:>4.1f} A | T={sample.temp_c:>4.1f} C | sensor={health}")
        print(f"  RESULT: t={result.detected_ms} ms | cause={result.cause} | action={result.action}")
        print()

if __name__ == "__main__":
    main()
