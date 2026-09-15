/*
 * Motor Fault-Detection & Protection System
 * Target: Arduino Uno (Proteus simulation)
 *
 * Inputs:
 *   A0 - current sensor, 0.0-5.0 V mapped to 0-10 A
 *   A1 - LM35 temperature sensor, 10 mV/°C
 *   D2 - sensor-health input (HIGH = sensor loop healthy)
 *
 * Outputs:
 *   D8 - relay/contactor drive (HIGH = motor energized)
 *   D9 - red fault LED
 *   D10 - green run LED
 *   Serial - timestamped event log
 */

const byte CURRENT_PIN = A0;
const byte TEMP_PIN = A1;
const byte SENSOR_HEALTH_PIN = 2;
const byte RELAY_PIN = 8;
const byte FAULT_LED_PIN = 9;
const byte RUN_LED_PIN = 10;

const float ADC_REF_V = 5.0;
const float CURRENT_SENSOR_MAX_A = 10.0;
const float OVERCURRENT_A = 7.0;
const float OVERTEMP_C = 75.0;
const unsigned long SAMPLE_PERIOD_MS = 100;

bool tripped = false;
unsigned long lastSample = 0;

float readCurrentAmps() {
  int raw = analogRead(CURRENT_PIN);
  return (raw * ADC_REF_V / 1023.0) * (CURRENT_SENSOR_MAX_A / ADC_REF_V);
}

float readTemperatureC() {
  int raw = analogRead(TEMP_PIN);
  return (raw * ADC_REF_V / 1023.0) * 100.0; // LM35: 10 mV/C
}

void tripMotor(const char* cause, float currentA, float tempC) {
  if (tripped) return;
  tripped = true;
  digitalWrite(RELAY_PIN, LOW);
  digitalWrite(RUN_LED_PIN, LOW);
  digitalWrite(FAULT_LED_PIN, HIGH);
  Serial.print("FAULT,t=");
  Serial.print(millis());
  Serial.print("ms,cause=");
  Serial.print(cause);
  Serial.print(",current=");
  Serial.print(currentA, 2);
  Serial.print("A,temp=");
  Serial.print(tempC, 1);
  Serial.println("C,action=CONTACTOR_OPEN");
}

void setup() {
  pinMode(SENSOR_HEALTH_PIN, INPUT_PULLUP);
  pinMode(RELAY_PIN, OUTPUT);
  pinMode(FAULT_LED_PIN, OUTPUT);
  pinMode(RUN_LED_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, HIGH);
  digitalWrite(FAULT_LED_PIN, LOW);
  digitalWrite(RUN_LED_PIN, HIGH);
  Serial.begin(9600);
  Serial.println("BOOT,motor_protection=READY");
}

void loop() {
  if (millis() - lastSample < SAMPLE_PERIOD_MS) return;
  lastSample = millis();

  float currentA = readCurrentAmps();
  float tempC = readTemperatureC();
  bool sensorHealthy = digitalRead(SENSOR_HEALTH_PIN) == HIGH;

  if (!sensorHealthy) {
    tripMotor("SENSOR_MALFUNCTION", currentA, tempC);
  } else if (currentA >= OVERCURRENT_A) {
    tripMotor("OVERCURRENT", currentA, tempC);
  } else if (tempC >= OVERTEMP_C) {
    tripMotor("OVERHEATING", currentA, tempC);
  }
}
