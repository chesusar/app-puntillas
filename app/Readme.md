<div align="Center">
  <h1 align="Center">Na Punta Dos Pes APP</h1>
  <p float="left">
    <img src="https://i.imgur.com/DUAvY2D.png" width="226" height="416">  
    <img src="https://i.imgur.com/QgZnqLW.png" width="226" height="416">
  </p>
</div>

## Descripción

Esta aplicación en Python se utiliza para interactuar con un dispositivo IoT que envía datos a través de Bluetooth Low Energy (BLE). El código principal se encuentra en `app.py`. La aplicación realiza las siguientes tareas:

- Se conecta al dispositivo IoT a través del receptor BLE.
- Suscribe las características relevantes del servicio BLE.
- Muestra los datos recibidos en una interfaz gráfica de usuario (GUI).
- Almacena los datos recibidos en el servidor de adafruit-io mediante peticiones MQTT.
- Permite iniciar y detener la transmisión de datos desde el dispositivo IoT.

## Datos recibidos y almacenados
- **Tiempo hasta el ángulo máximo:** Mide el tiempo que se tarda en alcanzar el ángulo máximo al ponerse de puntillas desde el inicio del movimiento.
- **Tiempo de permanencia en puntillas:** Registra el tiempo durante el cual una persona puede mantenerse de puntillas.
- **Ángulo máximo alcanzado:** Mide el ángulo máximo logrado al estar de puntillas.
- **Ángulo mínimo en puntillas:** Determina el ángulo mínimo mientras se mantiene la posición de puntillas.
- **Promedio del ángulo en puntillas:** Calcula el promedio del ángulo durante la permanencia en puntillas.
