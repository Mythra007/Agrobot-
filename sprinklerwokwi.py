#include <ServoESP32.h>  // Include the ServoESP32 library for ESP32

ServoESP32 valveServo;  // Create a Servo object for ESP32

int xCoord = 20;    // Simulated input
int yCoord = 30;    // Simulated input
int moisture = 512; // Simulated analog sensor value
int matrixValue;
int newMoisture;

int L = 100;
int B = 100;

unsigned long wateringStartTime;
bool valveOpen = false;
const unsigned long wateringDuration = 10000;

int gridNumber(int x, int y) {
  int x_no = (x * 10) / L;
  int y_no = (y * 10) / B;
  int grid_no = 10 * y_no + (x_no + 1);
  return grid_no;
}

int valveAngle(int moisturePercent) {
  moisturePercent = constrain(moisturePercent, 0, 100);
  return map(moisturePercent, 0, 100, 120, 0); // Map moisture to valve angle
}

void setup() {
  Serial.begin(9600);
  valveServo.setPeriodHertz(50); // Set the frequency to 50Hz for ESP32 servos
  valveServo.attach(13);         // Attach the servo to pin 13 (GPIO 13 in ESP32)

  matrixValue = gridNumber(xCoord, yCoord);
  Serial.print("Matrix Number: ");
  Serial.println(matrixValue);

  newMoisture = map(moisture, 0, 1023, 0, 100);  // Map the moisture level to percentage
  int angle = valveAngle(newMoisture);             // Calculate the angle for the valve
  Serial.print("Moisture (%): ");
  Serial.print(newMoisture);
  Serial.print(" | Valve Angle: ");
  Serial.println(angle);

  valveServo.write(angle); // Set the valve position
  wateringStartTime = millis();  
  valveOpen = true;
}

void loop() {
  if (valveOpen && (millis() - wateringStartTime >= wateringDuration)) {
    Serial.println("Time exceeded. Closing valve...");
    valveServo.write(0);  // Close the valve by setting it to 0 degrees
    valveOpen = false;
  }

  delay(1000); // Delay for 1 second before the next loop
}