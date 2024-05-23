<div align="Center">
  <h2 align="Center">Receptor Bluetooth con ESP32</h2>
  <p float="left">
  </p>
</div>

Este proyecto utiliza un ESP32 como receptor Bluetooth para recibir datos de un dispositivo IoT basado en Arduino Nano 33 BLE Sense. El código principal se encuentra en `receptor.ino`.

## Descripción

El código realiza las siguientes tareas:

- Inicializa el módulo Bluetooth del ESP32.
- Publicita el ESP32 como un dispositivo Bluetooth accesible.
- Escanea y se conecta al dispositivo IoT específico.
- Suscribe las características relevantes del servicio Bluetooth.
- Lee y muestra los datos recibidos del dispositivo IoT, tales como ángulos y tiempos.

## Características BLE

El código se conecta a un servicio Bluetooth específico y se suscribe a las siguientes características:

- **UUID_PROCESAR:** Característica para iniciar o detener el procesamiento de datos.
- **UUID_MAX_ANGULO:** Característica que transmite el ángulo máximo medido.
- **UUID_MIN_ANGULO:** Característica que transmite el ángulo mínimo medido.
- **UUID_ANGULO:** Característica que transmite el ángulo actual.
- **UUID_ESTADO:** Característica que transmite el estado actual del dispositivo.
- **UUID_TIEMPO_SUBIDA:** Característica que transmite el tiempo de subida.
- **UUID_TIEMPO_ALTO:** Característica que transmite el tiempo mantenido en la posición elevada.
- **UUID_PROMEDIO:** Característica que transmite el ángulo promedio.
