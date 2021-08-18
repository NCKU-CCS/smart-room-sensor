#include "EmonLib.h"
// Include Emon Library

EnergyMonitor emon1;
// Create an instance

void setup() {
    Serial.begin(9600);
    // Current: input pin, calibration.
    emon1.current(0, 60);
}

void loop() {
    // Calculate Irms only
    double Irms = emon1.calcIrms(1480);
    // Apparent power
    Serial.println(Irms);
    // delay(60000);
    delay(10000);
}