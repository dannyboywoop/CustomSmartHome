#include <math.h>

const int PWM_MAX = 255;
const int ADC_MAX = 1023;
const float knownResistance = 10000;
const float thermistor_R0 = 10000;
const float thermistor_T0 = 298.15;
const float B_value = 3950;
const float tempOffset = -3;
int fanPin = 9;
int tempPin = A0;
volatile int tempADC = 0;
volatile int fanPWM = 0;

void setup() {
  pinMode(fanPin, OUTPUT);
  pinMode(tempPin, INPUT);
}

float calculateResistance(int tempADC){
  float coefficient = (float(ADC_MAX)/float(tempADC) - 1);
  return coefficient * knownResistance;
}

float kelvinToDegreesC(float tempKelvin){
  return tempKelvin - 273.15;
}

float calculateTemp(int tempADC){
  float resistance = calculateResistance(tempADC);
  float log_denominator = thermistor_R0 * exp(-B_value/thermistor_T0);
  float T_kelvin = B_value / log(resistance/log_denominator);
  T_kelvin += tempOffset;
  return kelvinToDegreesC(T_kelvin);
}

void loop() {
  tempADC = analogRead(tempPin);
  float temp = calculateTemp(tempADC);
  if (temp < 30){
    fanPWM = 0;
  }else if(tempADC < 32.5){
    fanPWM = PWM_MAX/2;
  }else if(tempADC < 37.5){
    fanPWM = PWM_MAX/2;
  }else{
    fanPWM = PWM_MAX;
  }
  analogWrite(fanPin, fanPWM);
  delay(15000);
}
