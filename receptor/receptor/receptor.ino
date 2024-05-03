#include <ArduinoBLE.h>

const char* UUID_SERVICE = "6282a2a1-5f99-430e-abda-ba09b255bdd4";
const char* UUID_PROCESAR = "99ee8226-8c9e-4972-b4f5-ea7af1caa0b5";
const char* UUID_MAX_ANGULO = "17cc3d4f-69c7-4e00-a954-0346ecbb22c7";
const char* UUID_MIN_ANGULO = "6a8adb71-4b3b-421f-b5e1-e74bad969122";
const char* UUID_ANGULO = "38b48b19-373f-4425-a790-42df14c08300";
const char* UUID_ESTADO = "c4346fa0-d0ee-4c24-817f-0fab75a7fd23";
const char* UUID_TIEMPO_SUBIDA = "64247fd3-2d0e-461f-ac13-8651d2ba991e";
const char* UUID_TIEMPO_ALTO = "ddc902e8-9d9f-4db6-ba57-76609f6d2adb";
const char* UUID_PROMEDIO = "fdee3592-43f5-40ac-b408-2a15a0b4413c";

BLECharacteristic procesarChar;
BLECharacteristic maxAnguloChar;
BLECharacteristic minAnguloChar;
BLECharacteristic promAnguloChar;
BLECharacteristic anguloChar;
BLECharacteristic estadoChar;
BLECharacteristic tiempoSubidaChar;
BLECharacteristic tiempoAltoChar;

void setup() {
  Serial.begin(115200);
  BLE.begin();
  BLE.setLocalName("ESP Receptor");
  BLE.advertise();
}

void subscribe(BLECharacteristic c){
  if(!c.subscribe()){
    Serial.println("Cannot subscribe");
  }
}

void readChar(BLECharacteristic c){
  if(c.valueUpdated()){
    byte m;
    c.readValue(m);
    int m_int = m;
    String msg = String(c.uuid()) + " " + (String)m_int;
    Serial.println(msg);
  }
}

void loop() {
  static String serialDato = "";
  static BLEDevice peripheral;

  while(!peripheral){
    // Serial.println("Buscando");
    BLE.scanForAddress("18:14:25:D8:88:BD");
    peripheral = BLE.available();
    delay(1000);
  }

  // Serial.println("COnnectado ble");

  if (!peripheral.connected()){
    BLE.stopScan();
    peripheral.connect();
    peripheral.discoverAttributes();

    procesarChar = peripheral.characteristic(UUID_PROCESAR);
    // subscribe(procesarChar);

    maxAnguloChar = peripheral.characteristic(UUID_MAX_ANGULO);
    subscribe(maxAnguloChar);
    
    minAnguloChar = peripheral.characteristic(UUID_MIN_ANGULO);
    subscribe(minAnguloChar);
    
    anguloChar = peripheral.characteristic(UUID_ANGULO);
    subscribe(anguloChar);
    
    estadoChar = peripheral.characteristic(UUID_ESTADO);
    subscribe(estadoChar);
    
    tiempoSubidaChar = peripheral.characteristic(UUID_TIEMPO_SUBIDA);
    subscribe(tiempoSubidaChar);
    
    tiempoAltoChar = peripheral.characteristic(UUID_TIEMPO_ALTO);
    subscribe(tiempoAltoChar);

    promAnguloChar = peripheral.characteristic(UUID_PROMEDIO);
    subscribe(promAnguloChar);
  }

  if (peripheral.connected()){
    readChar(maxAnguloChar);
    readChar(minAnguloChar);
    readChar(anguloChar);
    readChar(estadoChar);
    readChar(tiempoSubidaChar);
    readChar(tiempoAltoChar);
    readChar(promAnguloChar);
  }

  if (Serial.available() > 0){
    char read = Serial.read();
    if (read == 1 || read == '1')
      procesarChar.writeValue(1);
    else
      procesarChar.writeValue(0);

    // serialDato.concat(read);
  }
  // if (serialDato.endsWith("\n")){
  //   // Serial.print(serialDato);
    
  //   serialDato.trim();
  //   int index = serialDato.indexOf(' ');
    
  //   serialDato = serialDato.substring(index+1);

  //   procesarChar.writeValue(serialDato.toInt());
    
  //   // Serial.print("Dato ");
  //   // Serial.println(serialDato);
  //   serialDato = "";
  // }

  // serialDato = UUID_ANGULO + " " + (String)dato;
  // Serial.println(serialDato);

  delay(50);
}
