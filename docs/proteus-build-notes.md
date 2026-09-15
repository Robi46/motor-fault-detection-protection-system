# Proteus Build Notes

The reference circuit is intended for an Arduino Uno in Proteus. Use a 12 V DC source, a DC motor, a normally-open relay contact in series with the motor, and a transistor-driven relay coil with a flyback diode. Feed the current sensor output to A0, an LM35 to A1, and a normally-closed sensor-health loop to D2. The relay driver is connected to D8. Connect the Arduino ground to the sensor and relay-driver ground.

The current-sensor model uses a 0–5 V output mapped linearly to 0–10 A. The LM35 model uses 10 mV per °C. For scenario injection, change the current-sensor potentiometer, heat the LM35 input using a voltage source equivalent, or open the sensor-health loop. The expected response is a LOW signal at D8, an open K1 contact, a lit fault LED, and a timestamped serial event.

## Suggested Proteus parts

| Reference | Part | Purpose |
|---|---|---|
| U1 | Arduino Uno R3 | Sampling and decision logic |
| M1 | DC MOTOR | Conveyor load model |
| K1 | Relay SPST-NO | Automatic safety cutoff |
| Q1 | 2N2222 | Relay coil low-side driver |
| D1 | 1N4007 | Flyback suppression |
| U2 | LM35 | Temperature input |
| R/S | Potentiometer or current-sensor model | Current input |
| LED1/LED2 | LED | RUN and FAULT indication |

## Proteus firmware setup

Compile `src/motor_protection.ino` with the Arduino IDE or an equivalent AVR toolchain, then load the generated HEX file into U1. Set the virtual terminal to 9600 baud, 8 data bits, no parity, and one stop bit. The firmware samples every 100 ms and latches the first detected fault until reset.
