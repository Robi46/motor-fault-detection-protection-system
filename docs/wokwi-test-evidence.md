# Wokwi Verification Evidence

This project uses Wokwi as the free, browser-based interactive verification environment. It replaces the unavailable Proteus installation for portfolio demonstration while preserving the Arduino firmware, relay cutoff behavior, analog sensor inputs, and serial diagnostic output.

## Open the project

After the project is created in Wokwi, add its public URL here:

```text
WOKWI_PROJECT_URL: pending browser save
```

The checked-in `wokwi/diagram.json`, `wokwi/sketch.ino`, and `wokwi/wokwi.toml` files are sufficient to recreate the project in a new Wokwi workspace.

## Scenario procedure

| Scenario | Wokwi action | Expected serial event | Expected hardware response |
|---|---|---|---|
| Normal operation | Leave current and temperature knobs below threshold; leave health switch closed. | No `FAULT` event. | RUN LED on, FAULT LED off, contactor energized, load on. |
| Overcurrent | Increase the `current` potentiometer until A0 maps to at least 7.0 A. | `cause=OVERCURRENT` and `action=CONTACTOR_OPEN`. | Contactor opens, load turns off, FAULT LED turns on. |
| Overheating | Reset the simulation, then increase the `temperature` potentiometer until A1 maps to at least 75.0 °C. | `cause=OVERHEATING` and `action=CONTACTOR_OPEN`. | Contactor opens, load turns off, FAULT LED turns on. |
| Sensor malfunction | Reset the simulation, then open the blue sensor-health switch. | `cause=SENSOR_MALFUNCTION` and `action=CONTACTOR_OPEN`. | Contactor opens, load turns off, FAULT LED turns on. |

The Arduino latch intentionally requires a simulation reset before testing the next scenario. Capture the Serial Monitor after each reset and fault injection, then add the screenshots under `assets/wokwi/` if image evidence is desired.

## Scope note

Wokwi's potentiometer model is used as an analog input control rather than a physical current-transformer or LM35 electrical model. The project therefore verifies the firmware decision path and protection response, not motor electromagnetic behavior or certified protection performance.
