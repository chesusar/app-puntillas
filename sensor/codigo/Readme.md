<div align="Center">
  <h1 align="Center">Codigo del dispositivo IoT</h1>
  <p float="left">
  </p>
</div>

## Descripción
Este código realiza las siguientes tareas:

- Inicializa los sensores del Arduino Nano 33 BLE Sense.
- Lee los datos del acelerómetro y el giroscopio.
- Aplica un filtro de Kalman para calcular el ángulo con precisión.
- Monitorea el estado del equilibrio y el movimiento.
- Envía los datos calculados a través de Bluetooth a una aplicación móvil o PC.

## Filtro de Kalman
El filtro de Kalman se utiliza para fusionar las lecturas del acelerómetro y el giroscopio, proporcionando estimaciones más precisas del ángulo y reduciendo el ruido en las mediciones.

<center>
  <h1>Dispositivo IoT de Monitoreo de Equilibrio y Movimiento</h1>
  
  <video src="https://github.com/chesusar/app-puntillas/assets/133507131/c614b8c2-d482-485f-80f9-662d0921a47c" width="226" height="416"/> 
</center>


## Maquina de estados
<div align="Center">
  <p float="left">
    <img src="https://github.com/chesusar/app-puntillas/blob/main/sensor/codigo/maquina%20de%20estados.png" width="437" height="347">
  </p>
</div>
