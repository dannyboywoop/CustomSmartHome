
#include <ArduinoBLE.h>

BLEService motorService("cdcd7cfc-cb56-11ea-87d0-0242ac130003"); // create service

// create rotate characteristic and allow remote device to read and write
BLEIntCharacteristic rotateCharacteristic("fd5db22e-cb57-11ea-87d0-0242ac130003", BLERead | BLEWrite);

void setup() {
  Serial.begin(9600);

  pinMode(LED_BUILTIN, OUTPUT);
  setupMotor();

  // begin initialization
  if (!BLE.begin()) {
    Serial.println("starting BLE failed!");

    while (1);
  }

  // set the local name peripheral advertises
  BLE.setLocalName("BlindMotor");
  // set the UUID for the service this peripheral advertises
  BLE.setAdvertisedService(motorService);

  // add the characteristic to the service
  motorService.addCharacteristic(rotateCharacteristic);

  // add service
  BLE.addService(motorService);

  // assign event handlers for connected, disconnected to peripheral
  BLE.setEventHandler(BLEConnected, blePeripheralConnectHandler);
  BLE.setEventHandler(BLEDisconnected, blePeripheralDisconnectHandler);

  // assign event handlers for characteristic
  rotateCharacteristic.setEventHandler(BLEWritten, rotateCharacteristicWritten);
  // set an initial value for the characteristic
  rotateCharacteristic.writeValue(0);

  // start advertising
  BLE.advertise();

  Serial.println(("Bluetooth device active, waiting for connections..."));
}

void loop() {
  // poll for BLE events
  BLE.poll();
}

void blePeripheralConnectHandler(BLEDevice central) {
  // central connected event handler
  Serial.print("Connected event, central: ");
  Serial.println(central.address());
  digitalWrite(LED_BUILTIN, HIGH);
}

void blePeripheralDisconnectHandler(BLEDevice central) {
  // central disconnected event handler
  Serial.print("Disconnected event, central: ");
  Serial.println(central.address());
  digitalWrite(LED_BUILTIN, LOW);
}

int endianSwap(int val){
  unsigned char* bytes = (unsigned char*)&val;
  return int(bytes[0] << 24 | bytes[1] << 16 | bytes[2] << 8 | bytes[3]);
}

void rotateCharacteristicWritten(BLEDevice central, BLECharacteristic characteristic) {
  // central wrote new value to characteristic, rotate motor
  Serial.print("Rotating motor by angle: ");
  int val = endianSwap(rotateCharacteristic.value());
  Serial.println(val);
  rotateByAngle(val, 100);
}
