## Descripción
Este código realiza las siguientes tareas:

- Inicializa los sensores del Arduino Nano 33 BLE Sense.
- Lee los datos del acelerómetro y el giroscopio.
- Aplica un filtro de Kalman para calcular el ángulo con precisión.
- Monitorea el estado del equilibrio y el movimiento.
- Envía los datos calculados a través de Bluetooth a una aplicación móvil o PC.

## Filtro de Kalman
El filtro de Kalman se utiliza para fusionar las lecturas del acelerómetro y el giroscopio, proporcionando estimaciones más precisas del ángulo y reduciendo el ruido en las mediciones.

## Maquina de estados
<div align="Center">
  <p float="left">
    <img src="https://github.com/chesusar/app-puntillas/blob/serial/sensor/codigo/maquina%20de%20estados.png" width="437" height="347">
  </p>
</div>
