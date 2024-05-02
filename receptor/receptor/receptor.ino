const String UUID_SERVICE = "6282a2a1-5f99-430e-abda-ba09b255bdd4";
const String UUID_PROCESAR = "99ee8226-8c9e-4972-b4f5-ea7af1caa0b5";
const String UUID_MAX_ANGULO = "17cc3d4f-69c7-4e00-a954-0346ecbb22c7";
const String UUID_MIN_ANGULO = "6a8adb71-4b3b-421f-b5e1-e74bad969122";
const String UUID_ANGULO = "38b48b19-373f-4425-a790-42df14c08300";
const String UUID_ESTADO = "c4346fa0-d0ee-4c24-817f-0fab75a7fd23";
const String UUID_TIEMPO_SUBIDA = "64247fd3-2d0e-461f-ac13-8651d2ba991e";
const String UUID_TIEMPO_ALTO = "ddc902e8-9d9f-4db6-ba57-76609f6d2adb";

void setup() {
  Serial.begin(115200);
}

void loop() {
  static String serialDato = "";

  if (Serial.available() > 0){
    char read = Serial.read();
    serialDato.concat(read);
  }
  if (serialDato.endsWith("\n")){
    Serial.print(serialDato);
    serialDato = "";
  }

  // serialDato = UUID_ANGULO + " " + (String)dato;
  // Serial.println(serialDato);

  delay(100);
}
