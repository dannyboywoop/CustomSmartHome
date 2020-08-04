int fanPin = 9;
int tempPin = A0;
const int PWM_MAX = 255;
volatile int tempADC = 0;
volatile int fanPWM = 0;

void setup() {
  pinMode(fanPin, OUTPUT);
  pinMode(tempPin, INPUT);
}

void loop() {
  tempADC = analogRead(tempPin);
  if (tempADC < 600){
    fanPWM = 0;
  }else if(tempADC < 700){
    fanPWM = PWM_MAX/4;
  }else if(tempADC < 800){
    fanPWM = PWM_MAX/2;
  }else{
    fanPWM = PWM_MAX;
  }
  analogWrite(fanPin, fanPWM);
  delay(15000);
}
