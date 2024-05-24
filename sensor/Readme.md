
<div align="Center">
  <h1 align="Center">Dispositivo IoT de Monitoreo de Equilibrio y Movimiento - Sensor</h1>
  <p float="left">
  </p>
</div>

## Descripción
Este proyecto utiliza un dispositivo IoT basado en el sensor IMU para monitorear y analizar el equilibrio y los movimientos relacionados con mantenerse de puntillas. El dispositivo emplea un Arduino Nano 33 BLE Sense para procesar los datos del acelerómetro y el giroscopio, aplicando un filtro de Kalman para mejorar la precisión de las mediciones.

## Estructura de Carpetas
- codigo
  - dispositivo_iot.ino

- componentes
  - comparacion_IMUs.pdf
  - comparacion_DCDC.pdf
  - decisiones.pdf

- medidas
  - Datos_arduino
  - Datos_finales
  - Manejo_datos
    - convertir_datos.py
    - representar_datos.m

- modelo_3D
   - carcasa.stl

## Código
### Ubicación
El código fuente del dispositivo IoT se encuentra en la carpeta `codigo`.

### Descripción
El código está desarrollado para el **Arduino Nano 33 BLE Sense** y se encarga de:
- Tomar mediciones del acelerómetro y el giroscopio.
- Aplicar un filtro de Kalman para calcular el ángulo con mayor precisión.
- Enviar los datos procesados vía Bluetooth al receptor bluetooh del PC.

### Filtro de Kalman
El filtro de Kalman se utiliza para combinar las lecturas del acelerómetro y el giroscopio, proporcionando estimaciones más precisas del ángulo, reduciendo el ruido y mejorando la estabilidad de las mediciones.

<center>
  <video src="https://github.com/chesusar/app-puntillas/assets/133507131/c614b8c2-d482-485f-80f9-662d0921a47c" width="226" height="416"/> 
</center>

## Componentes
### Ubicación
La información sobre los componentes se encuentra en la carpeta `componentes`.

### Descripción
- **Sensor inercial.xlsx:** Comparación de diferentes sensores IMU considerados para el proyecto.
- **Reguladores de tensión.xlsx:** Comparación de diferentes convertidores DC-DC utilizados.
- **Comparacion_componentes.pdf:** Documento explicando las decisiones tomadas en la selección de componentes.

## Medidas
### Ubicación
Los datos de las mediciones se encuentran en la carpeta `medidas`.

### Descripción
- **Datos_arduino:** Lecturas de acelerómetro y giroscopio realizadas con el dispositivo IoT en diferentes personas.
- **Datos_finales:** Datos procesados a partir de las lecturas originales, separados en archivos CSV y un archivo Excel con información resumida de cada persona.
- **Manejo_datos:** Scripts para manejar y representar los datos:
  - `convertir_datos.py:` Script en Python para convertir los datos de `Datos_arduino` en `Datos_finales`.
  - `representar_datos.m:` Script en Matlab para representar los datos en gráficos.

## Modelo 3D
### Ubicación
El diseño de la carcasa para el dispositivo se encuentra en la carpeta `modelo_3D`.

### Descripción
- **Tobillera.stl:** Modelo 3D de la carcasa diseñada para integrar la batería y el sensor en un solo dispositivo compacto.

