from test_scenarios import (
    test_overcurrent_trips_contactor,
    test_overheating_trips_contactor,
    test_sensor_malfunction_has_priority,
    test_healthy_motor_remains_on,
)

TESTS = [
    test_overcurrent_trips_contactor,
    test_overheating_trips_contactor,
    test_sensor_malfunction_has_priority,
    test_healthy_motor_remains_on,
]

for test in TESTS:
    test()
    print(f"PASS {test.__name__}")
print(f"{len(TESTS)} tests passed")
