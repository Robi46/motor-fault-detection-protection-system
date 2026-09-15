import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1] / "simulation"))

from run_scenarios import Sample, detect


def test_overcurrent_trips_contactor():
    result = detect("test", [Sample(0, 2.0, 30), Sample(100, 7.1, 30)])
    assert (result.detected_ms, result.cause, result.action) == (100, "OVERCURRENT", "CONTACTOR_OPEN")


def test_overheating_trips_contactor():
    result = detect("test", [Sample(0, 2.0, 74), Sample(100, 2.0, 75.0)])
    assert (result.detected_ms, result.cause, result.action) == (100, "OVERHEATING", "CONTACTOR_OPEN")


def test_sensor_malfunction_has_priority():
    result = detect("test", [Sample(0, 2.0, 30), Sample(100, 2.0, 30, sensor_healthy=False)])
    assert (result.detected_ms, result.cause, result.action) == (100, "SENSOR_MALFUNCTION", "CONTACTOR_OPEN")


def test_healthy_motor_remains_on():
    result = detect("test", [Sample(0, 2.0, 30), Sample(100, 2.5, 40)])
    assert result.action == "MOTOR_REMAINS_ENERGIZED"
