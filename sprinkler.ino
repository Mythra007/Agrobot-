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
const unsigned long wateringDuration = 10000; 

int gridNumber(int x, int y) {
  int x_no = (x * 10) / L;
  int y_no = (y * 10) / B;
  int grid_no = 10 * y_no + (x_no + 1);
  return grid_no;
}

int valveAngle(int moisturePercent) {
  if (moisturePercent >= 0 && moisturePercent < 10) {
    return 120;
  } else if (moisturePercent >= 10 && moisturePercent < 20) {
    return 100;
  } else if (moisturePercent >= 20 && moisturePercent < 30) {
    return 80;
  } else if (moisturePercent >= 30 && moisturePercent < 40) {
    return 60;
  } else if (moisturePercent >= 40 && moisturePercent < 50) {
    return 40;
  } else if (moisturePercent >= 50 && moisturePercent < 60) {
    return 20;
  } else if (moisturePercent >= 60 && moisturePercent < 70) {
    return 5;
  } else {
    return 0; 
  }
}

void setup() {
  Serial.begin(9600);
  valveServo.attach(3);

  matrixValue = gridNumber(xCoord, yCoord);
  Serial.print("Matrix Number: ");
  Serial.println(matrixValue);

  newMoisture = map(moisture, 0, 1023, 0, 100);
  int angle = valveAngle(newMoisture);

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