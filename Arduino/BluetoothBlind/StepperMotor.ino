const float STEPS_PER_ROTATION = 509.4716;
const int MIN_DELAY = 2;
const int NUMBER_OF_STEPPER_PINS = 4;
const int STEPPER_PINS[NUMBER_OF_STEPPER_PINS] = {9, 10, 11, 12};
const int STATES_PER_STEP = 4;
const int STEPPER_PIN_STATES[4][4] = {
  {HIGH, LOW, LOW, LOW},
  {LOW, HIGH, LOW, LOW},
  {LOW, LOW, HIGH, LOW},
  {LOW, LOW, LOW, HIGH}
};
const int CLOCKWISE = 1;
const int ANTI_CLOCKWISE = -1;

void setupMotor() {
  for (int i=0; i<NUMBER_OF_STEPPER_PINS; i++){
    pinMode(STEPPER_PINS[i], OUTPUT);
  }
}

void setStepperState(int delayLength, const int states[]){
  for (int i=0; i<NUMBER_OF_STEPPER_PINS; i++){
    digitalWrite(STEPPER_PINS[i], states[i]);
    delay(delayLength);
  }
}

void setStepperState(int delayLength){
  int states[4] = {LOW, LOW, LOW, LOW};
  setStepperState(delayLength, states);
}

void performStep(int delayLength, int rotationDirection){
  // default to CLOCKWISE if invalid rotationDirection
  if (abs(rotationDirection) != 1){
    rotationDirection = CLOCKWISE;
  }

  // set i to 0 if CLOCKWISE, 3 if ANTI_CLOCKWISE
  int i = 1.5 - 1.5*rotationDirection;
  
  for (int count=0; count<STATES_PER_STEP; count++){
    setStepperState(delayLength, STEPPER_PIN_STATES[i]);
    i+=rotationDirection;
  }
}

int delayForSpeed(float percentageSpeed){
  float percentage = max(percentageSpeed, 0);
  int delayLength = MIN_DELAY * 100 / percentage;
  return max(MIN_DELAY, delayLength);
}

void rotateByAngle(float angle, float rotationSpeed){
  int rotationDirection = CLOCKWISE;
  if (angle < 0){
    angle = abs(angle);
    rotationDirection = ANTI_CLOCKWISE;
  }
  int steps_to_perform = 0.5 + STEPS_PER_ROTATION * angle / 360;
  int delayLength = delayForSpeed(rotationSpeed);

  for (int i=0; i<steps_to_perform; i++){
    performStep(delayLength, rotationDirection);
  }

  setStepperState(delayLength);
}
