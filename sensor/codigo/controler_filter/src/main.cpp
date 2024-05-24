#include <Arduino.h>
#include <Arduino_LSM9DS1.h>
#include <ArduinoBLE.h>
#include "vector3.h"
#include "kalman.h"

#define SAMPLE_MS 50

// Umbrales transición de estados
const float ANGLE_THRESHOLD = 2;
const float DERIV_ANGLE_THRESHOLD = 20;

// Estados
const int ST_ABAJO = 1;
const int ST_SUBIDA = 2;
const int ST_ARRIBA = 3;
const int ST_BAJADA = 4;
int state = ST_ABAJO;
const String STATE_STRING[5] = {"EMPTY", "ABAJO", "SUBIDA", "ARRIBA", "BAJADA"};

kalman filtroY(SAMPLE_MS / 1000.0);

// Bluetooth
BLEService movService("6282a2a1-5f99-430e-abda-ba09b255bdd4");

BLECharCharacteristic procesoChar("99ee8226-8c9e-4972-b4f5-ea7af1caa0b5", BLEWrite);
BLEDescriptor procesoDes("0x2901", "Empezar proceso");
BLECharCharacteristic resetChar("7b14e65a-8610-4cd5-8653-5a3e0020204e", BLEWrite);
BLEDescriptor resetDes("0x2901", "Reset");

BLEIntCharacteristic maxChar("17cc3d4f-69c7-4e00-a954-0346ecbb22c7", BLERead | BLENotify);
BLEDescriptor maxDes("0x2901", "Angulo maximo");
BLEIntCharacteristic minChar("6a8adb71-4b3b-421f-b5e1-e74bad969122", BLERead | BLENotify);
BLEDescriptor minDes("0x2901", "Angulo minimo");
BLEIntCharacteristic medioChar("fdee3592-43f5-40ac-b408-2a15a0b4413c", BLERead | BLENotify);
BLEDescriptor medioDes("0x2901", "Angulo medio");
BLECharCharacteristic subidaChar("64247fd3-2d0e-461f-ac13-8651d2ba991e", BLERead | BLENotify);
BLEDescriptor subidaDes("0x2901", "Tiempo de subida");
BLECharCharacteristic altoChar("ddc902e8-9d9f-4db6-ba57-76609f6d2adb", BLERead | BLENotify);
BLEDescriptor altoDes("0x2901", "Tiempo en alto");

BLEIntCharacteristic anguloChar("38b48b19-373f-4425-a790-42df14c08300", BLERead | BLENotify);
BLEIntCharacteristic estadoChar("c4346fa0-d0ee-4c24-817f-0fab75a7fd23", BLERead | BLENotify);

void process();
float processAngle();
Vector3 getLastAcceleration();
Vector3 getLastAngularVelocity();

void iniciarBLE();

void setup()
{
  Serial.begin(115200);
  if (!IMU.begin())
  {
    Serial.println("Failed to initialize IMU!");
  }

  iniciarBLE();
}

void loop()
{
  uint32_t startMillis = millis();

  static BLEDevice central = BLE.central();
  int resetear = 0;
  static uint8_t procesando = 0;
  static int debug_conectado = 0;

  if (central)
  {
    if (debug_conectado == 0)
    {
      debug_conectado = 1;
      Serial.println("Conexion entrante");
    }
    if (central.connected())
    {
      if (procesoChar.written())
      {
        procesando = procesoChar.value();
        Serial.print("Proceso recibido ");
        Serial.println(procesando);
      }
      if (resetChar.written())
      {
        resetear = resetChar.value();
        resetChar.writeValue(0);
        Serial.println("Reset recibido");
        if (resetear == 1)
        {
          state = ST_ABAJO;
        }
      }
    }
  }
  else
  {
    if (debug_conectado == 1)
    {
      debug_conectado = 0;
      Serial.println("Conexion cerrada");
    }
    central = BLE.central();
  }

  if (procesando == 1)
  {
    process();
  }

  uint32_t elapsedTime = millis() - startMillis;
  uint32_t delayTime = SAMPLE_MS - elapsedTime;
  delayTime = delayTime > 0 ? delayTime : 0;
  delay(delayTime);
}

void process()
{
  // Tiempos
  static int tiempoSubida = 0;
  static int tiempoArriba = 0;

  // Angulos
  static float angle = 0.0;
  static float angleRaw = 0.0;
  static float angleOffset = 0.0;
  float angleAnterior = angle;
  float angleDeriv;
  static int anguloMaximo = 0;
  static int anguloMinimo = 999;
  static int anguloPromedio = 0;
  static int anguloPromedioContador = 0;

  angleRaw = processAngle();
  angle = angleRaw - angleOffset;
  angleDeriv = (angle - angleAnterior) / (SAMPLE_MS / 1000.0);

  anguloChar.writeValue((int)angle);

  switch (state)
  {
  case ST_ABAJO:
    tiempoArriba = 0;
    tiempoSubida = 0;
    anguloMaximo = 0;
    anguloMinimo = 999;
    anguloPromedio = 0;
    anguloPromedioContador = 0;

    if (angle >= ANGLE_THRESHOLD)
    {
      state = ST_SUBIDA;
      estadoChar.writeValue((int)state);
    }
    break;

  case ST_SUBIDA:
    tiempoSubida += SAMPLE_MS;
    anguloPromedio += angle;
    anguloPromedioContador += 1;

    if (angle > anguloMaximo)
    {
      anguloMaximo = angle;
    }

    if (angleDeriv < -DERIV_ANGLE_THRESHOLD)
    {
      state = ST_BAJADA;
      estadoChar.writeValue((int)state);
    }
    else if (angleDeriv < DERIV_ANGLE_THRESHOLD)
    {
      state = ST_ARRIBA;
      estadoChar.writeValue((int)state);
    }
    break;

  case ST_ARRIBA:
    tiempoArriba += SAMPLE_MS;
    anguloPromedio += angle;
    anguloPromedioContador += 1;
    if (angle > anguloMaximo)
    {
      anguloMaximo = angle;
    }
    if (angle < anguloMinimo)
    {
      anguloMinimo = angle;
    }

    if (angleDeriv > DERIV_ANGLE_THRESHOLD)
    {
      state = ST_SUBIDA;
      estadoChar.writeValue((int)state);
    }
    else if (angleDeriv < -DERIV_ANGLE_THRESHOLD)
    {
      state = ST_BAJADA;
      estadoChar.writeValue((int)state);
    }
    if (angle <= ANGLE_THRESHOLD)
    {
      state = ST_ABAJO;
      estadoChar.writeValue((int)state);
      minChar.writeValue((int)anguloMinimo);
      maxChar.writeValue((int)anguloMaximo);
      subidaChar.writeValue((int)tiempoSubida / 100);
      altoChar.writeValue((int)tiempoArriba / 100);
      medioChar.writeValue((int)anguloPromedio / anguloPromedioContador);
    }
    break;

  case ST_BAJADA:
    anguloPromedio += angle;
    anguloPromedioContador += 1;
    if (angleDeriv > DERIV_ANGLE_THRESHOLD)
    {
      state = ST_SUBIDA;
      estadoChar.writeValue((int)state);
    }
    else if (angleDeriv > -DERIV_ANGLE_THRESHOLD)
    {
      state = ST_ARRIBA;
      estadoChar.writeValue((int)state);
    }
    if (angle <= ANGLE_THRESHOLD)
    {
      state = ST_ABAJO;
      estadoChar.writeValue((int)state);
      minChar.writeValue((int)anguloMinimo);
      maxChar.writeValue((int)anguloMaximo);
      subidaChar.writeValue((int)tiempoSubida / 100);
      altoChar.writeValue((int)tiempoArriba / 100);
      medioChar.writeValue((int)anguloPromedio / anguloPromedioContador);
    }
    break;

  default:
    break;
  }

  // Serial.print(angle);
  // Serial.print("\t");
  // Serial.print(angleDeriv);
  // Serial.print("\t");
  // Serial.print(STATE_STRING[state]);
  // Serial.print("\t");
  // Serial.print(tiempoSubida);
  // Serial.print("\t");
  // Serial.println(tiempoArriba);
}

float processAngle()
{
  static float angleAccel = 0.0;

  // Acceleration
  Vector3 accel = getLastAcceleration();
  // Invertir vector g
  accel.x = -accel.x;
  accel.y = -accel.y;
  accel.z = -accel.z;
  if (accel.x != 0.0) // Evitar propagación de Nan
  {
    angleAccel = accel.getAngleY() - 90.0; // Ángulo 0 cuando en reposo
  }

  // Gyroscope
  Vector3 velocity = getLastAngularVelocity();

  float angleKalman = filtroY.process(-velocity.y, angleAccel);

  return angleKalman;
}

Vector3 getLastAcceleration()
{
  static float aX, aY, aZ;
  Vector3 v(-aX, -aZ, aY);
  if (IMU.accelerationAvailable())
  {
    IMU.readAcceleration(aX, aY, aZ);
    v.x = -aX;
    v.y = -aZ;
    v.z = aY;
  }
  return v;
}

Vector3 getLastAngularVelocity()
{
  static float aX, aY, aZ;
  Vector3 v(aX, aZ, -aY);
  if (IMU.gyroscopeAvailable())
  {
    IMU.readGyroscope(aX, aY, aZ);
    v.x = aX;
    v.y = aZ;
    v.z = -aY;
  }
  return v;
}

void iniciarBLE()
{
  if (!BLE.begin())
  {
    Serial.println("starting Bluetooth® Low Energy failed!");
  }
  BLE.setLocalName("DispositivoDoCaminaçao");

  BLE.setAdvertisedService(movService);

  subidaChar.addDescriptor(subidaDes);
  movService.addCharacteristic(subidaChar);

  altoChar.addDescriptor(altoDes);
  movService.addCharacteristic(altoChar);

  medioChar.addDescriptor(medioDes);
  movService.addCharacteristic(medioChar);

  minChar.addDescriptor(minDes);
  movService.addCharacteristic(minChar);

  maxChar.addDescriptor(maxDes);
  movService.addCharacteristic(maxChar);

  resetChar.addDescriptor(resetDes);
  movService.addCharacteristic(resetChar);

  procesoChar.addDescriptor(procesoDes);
  movService.addCharacteristic(procesoChar);

  movService.addCharacteristic(anguloChar);
  movService.addCharacteristic(estadoChar);

  BLE.addService(movService);

  BLE.advertise();
}