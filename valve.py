#include <Servo.h>

Servo valveServo;

int xCoord = 20;    // Example input from IoT
int yCoord = 30;    // Example input from IoT
int moisture = 512; // Example input from sensor
int matrixValue;
int newMoisture;

int L = 100;  // Length of the plot
int B = 100;  // Breadth of the plot

unsigned long wateringStartTime;
bool valveOpen = false;
const unsigned long wateringDuration = 10000; //defined after calculating

int gridNumber(int x, int y) {
  int x_no = (x * 10) / L;
  int y_no = (y * 10) / B;
  int grid_no = 10 * y_no + (x_no + 1);
  return grid_no;
}

// Smooth linear version
int valveAngle(int moisturePercent) {
  moisturePercent = constrain(moisturePercent, 0, 100);
  return map(moisturePercent, 0, 100, 120, 0); // Linear mapping from 0–100% to 120°–0°
}

/*
// Optional: Non-linear version (for sharper control at higher moisture)
int valveAngle(int moisturePercent) {
  moisturePercent = constrain(moisturePercent, 0, 100);
  float angle = 120 * pow((1 - (moisturePercent / 100.0)), 1.5); // Non-linear decay
  return (int)angle;
}
*/

void setup() {
  Serial.begin(9600);
  valveServo.attach(3);

  matrixValue = gridNumber(xCoord, yCoord);
  Serial.print("Matrix Number: ");
  Serial.println(matrixValue);

  newMoisture = map(moisture, 0, 1023, 0, 100);
  int angle = valveAngle(newMoisture);
  Serial.print("Moisture (%): ");
  Serial.print(newMoisture);
  Serial.print(" | Valve Angle: ");
  Serial.println(angle);

  valveServo.write(angle);
  wateringStartTime = millis();  
  valveOpen = true;
}

void loop() {
  if (valveOpen && (millis() - wateringStartTime >= wateringDuration)) {
    Serial.println("Time exceeded. Closing valve...");
    valveServo.write(0);  
    valveOpen = false;
  }

  delay(1000);
}