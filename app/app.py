import asyncio
from bleak import BleakClient, BleakGATTCharacteristic
from tkinter import *
import customtkinter
from PIL import Image, ImageTk
from device import NPDPDevice
import time
import threading
from Adafruit_IO import MQTTClient

# MQTT
ADAFRUIT_IO_KEY = ''
ADAFRUIT_IO_USERNAME= 'Rarribas'
client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
client.connect()

client.loop_background()

FLAG_ON = b"\x01"
FLAG_OFF = b"\x00"

UUID_SERVICE = "6282a2a1-5f99-430e-abda-ba09b255bdd4"
UUID_PROCESAR = "99ee8226-8c9e-4972-b4f5-ea7af1caa0b5"
UUID_MAX_ANGULO = "17cc3d4f-69c7-4e00-a954-0346ecbb22c7"
UUID_MIN_ANGULO = "6a8adb71-4b3b-421f-b5e1-e74bad969122"
UUID_ANGULO = "38b48b19-373f-4425-a790-42df14c08300"
UUID_ESTADO = "c4346fa0-d0ee-4c24-817f-0fab75a7fd23"
UUID_PROMEDIO = "fdee3592-43f5-40ac-b408-2a15a0b4413c"
UUID_TIEMPO_SUBIDA = "64247fd3-2d0e-461f-ac13-8651d2ba991e"
UUID_TIEMPO_ALTO = "ddc902e8-9d9f-4db6-ba57-76609f6d2adb"

device_address = "18:14:25:D8:88:BD"
device_connected = False

# UI Components
root = None
font_default = None

lbl_estado_sensor = None
bt_inicio = None

frame_bar = None
frame_bar_int = None
frame_bar_letra = None
frame_bar_barras = None
bar_angulo = None
bar_angulo_max = None
bar_angulo_min = None
bar_angulo_prom = None
image_max = None
icon_max = None
image_min = None
icon_min = None
icon_prom = None
lbl_angulo = None
lbl_angulo_max = None
lbl_angulo_min = None
lbl_angulo_prom = None

icon_usb = None

frame_tiempos = None
frame_tiempos_int = None
lbl_tiempo_subida = None
lbl_tiempo_subida_tiempo = None
lbl_tiempo_arriba = None
lbl_tiempo_arriba_tiempo = None

# Colores
COLOR_BACKGROUND_IDLE = "#212121"   # 12303B
COLOR_SECONDARY_IDLE = "#424242"    # 265C6D
COLOR_ACCENT_IDLE = "#1973ac"       # 007EA8
COLOR_ACCENT_2_IDLE = "#1f90d7"     # 35B5DF
COLOR_BACKGROUND_RUN = "#12303B"    # 543808
COLOR_SECONDARY_RUN = "#265C6D"     # C29547
COLOR_ACCENT_RUN = "#f9ae01"        # EEB044
COLOR_ACCENT_2_RUN = "#c98c01"      # F1C67D

# Estado
ST_IDLE = 0
ST_RUNNING = 1
state = ST_IDLE
bt_inicio_pressed = False
app_running = True
npdp = None
FPS = 60

thread_communication = None

# Estado sensor
ESTADOS_SENSOR = ["Desconectado", "Parado", "Subiendo", "Arriba", "Bajando"]
state_sensor = 0

datos = {
    "angulo" : 0.0,
    "angulo_prom" : 0.0,
    "angulo_min" : 0.0,
    "angulo_max" : 0.0,
    "state_sensor" : 0,
    "t_subida" : 0,
    "t_alto" : 0
}


def hsl_to_hex(h, s, l):
    # Normalizar los valores de H, S y L
    h = h % 360
    s = max(0, min(100, s))
    l = max(0, min(100, l))
    
    # Calcular los valores de R, G y B
    c = (1 - abs(2*l/100 - 1)) * s/100
    x = c * (1 - abs((h/60) % 2 - 1))
    m = l/100 - c/2
    
    if 0 <= h < 60:
        r, g, b = c, x, 0
    elif 60 <= h < 120:
        r, g, b = x, c, 0
    elif 120 <= h < 180:
        r, g, b = 0, c, x
    elif 180 <= h < 240:
        r, g, b = 0, x, c
    elif 240 <= h < 300:
        r, g, b = x, 0, c
    else:
        r, g, b = c, 0, x
    
    # Convertir los valores de R, G y B a hexadecimal
    r_hex = int((r + m) * 255)
    g_hex = int((g + m) * 255)
    b_hex = int((b + m) * 255)
    
    return "#{:02x}{:02x}{:02x}".format(r_hex, g_hex, b_hex)


def characteristic_callback(char, data):
    global state_sensor
    try:
        dato = int(data)
    except:
        dato = 0
    # dato = int.from_bytes(bytes=data, byteorder='little', signed=True)

    if char == UUID_ANGULO:
        datos["angulo"] = dato
    elif char == UUID_MAX_ANGULO:
        datos["angulo_max"] = dato
    elif char == UUID_MIN_ANGULO:
        datos["angulo_min"] = dato
    elif char == UUID_PROMEDIO:
        print("Angulo promedio recibido")
        datos["angulo_prom"] = dato
    elif char == UUID_ESTADO:
        datos["state_sensor"] = dato
        if dato == 4:
            client.publish('maximo', datos["angulo_max"])
            client.publish('promedio', datos["angulo_prom"])
            client.publish('minimo', datos["angulo_min"])
            client.publish('tiempo-subida', datos["t_subida"])
            client.publish('tiempo-puntillas', datos["t_alto"])
        # lbl_estado_sensor.configure(text=ESTADOS_SENSOR[dato])
        # state_sensor = dato
    elif char == UUID_TIEMPO_ALTO:
        datos["t_alto"] = dato/10.0
        # lbl_tiempo_arriba_tiempo.configure(text="{:.3f}".format(dato))
    elif char == UUID_TIEMPO_SUBIDA:
        datos["t_subida"] = dato/10.0
        # lbl_tiempo_subida_tiempo.configure(text="{:.3f}".format(dato))



def update_angulo(barra : customtkinter.CTkProgressBar, icono, label, dato, smooth=False):
    dato_smooth = dato/90.0
    if smooth:
        dato_smooth = (barra.get() + dato/90.0)/2.0
    barra.set(dato_smooth)
    barra.configure(progress_color=hsl_to_hex(dato, 72, 53), fg_color=hsl_to_hex(dato, 15, 30))
    label.configure(text=str(dato)+"º")
    label.configure(text_color=hsl_to_hex(dato, 72, 53))
    if icono != None:
        icono.place_configure(anchor=CENTER, relx=0.5, y=(140-dato_smooth*240))
        icono.configure(fg_color=hsl_to_hex(dato, 72, 53))


def button_event():
    global state
    global bt_inicio_pressed
    # if not device_connected:
    #     return
    if state == ST_IDLE:
        bt_inicio.configure(text="Reiniciar", fg_color=COLOR_ACCENT_RUN, hover_color=COLOR_ACCENT_2_RUN)
        frame_tiempos.configure(fg_color=COLOR_SECONDARY_RUN)
        frame_bar.configure(fg_color=COLOR_SECONDARY_RUN)
        root.configure(fg_color=COLOR_BACKGROUND_RUN)
        state = ST_RUNNING
    else:
        bt_inicio.configure(text="Iniciar", fg_color=COLOR_ACCENT_IDLE, hover_color=COLOR_ACCENT_2_IDLE)
        frame_tiempos.configure(fg_color=COLOR_SECONDARY_IDLE)
        frame_bar.configure(fg_color=COLOR_SECONDARY_IDLE)
        root.configure(fg_color=COLOR_BACKGROUND_IDLE)
        state = ST_IDLE
    bt_inicio_pressed = True


def close_app():
    global app_running
    app_running = False
    if npdp != None and npdp.is_open:
        npdp.close()


def process():
    if not npdp.is_open:
        icon_usb.place_forget()
    else:
        icon_usb.place_configure(anchor=NE, relx=(450-FRAME_PADDING/2)/450, y=FRAME_PADDING/2)

    update_angulo(bar_angulo, None, lbl_angulo, datos["angulo"], True)
    update_angulo(bar_angulo_prom, icon_prom, lbl_angulo_prom, datos["angulo_prom"], True)
    update_angulo(bar_angulo_max, icon_max, lbl_angulo_max, datos["angulo_max"], True)
    update_angulo(bar_angulo_min, icon_min, lbl_angulo_min, datos["angulo_min"], True)

    lbl_estado_sensor.configure(text=ESTADOS_SENSOR[datos["state_sensor"]])
    lbl_tiempo_arriba_tiempo.configure(text="{:.3f}".format(datos["t_alto"]))
    lbl_tiempo_subida_tiempo.configure(text="{:.3f}".format(datos["t_subida"]))



def callback(uuid, dato):
    # print("Callback")
    # print(uuid)
    # print(dato)
    characteristic_callback(uuid, dato)


def communication():
    global npdp

    if not app_running:
        return

    if not npdp.is_open:
        npdp.open()
        if npdp.is_open:
            print("Connected")
    else:
        npdp.update()


def communication_loop():
    while app_running:
        communication()


async def main():
    global device_connected
    global bt_inicio_pressed
    global thread_communication

    thread_communication = threading.Thread(target=communication_loop)
    thread_communication.start()

    while app_running:
        process()
        root.update()

        if bt_inicio_pressed:
            if state == ST_IDLE and npdp.is_open:
                npdp.write(UUID_PROCESAR, FLAG_OFF)
                # await client.write_gatt_char(characteristic_procesar, FLAG_OFF, response=True)
                print("PARAR")
            elif npdp.is_open:
                npdp.write(UUID_PROCESAR, FLAG_ON)
                # await client.write_gatt_char(characteristic_procesar, FLAG_ON, response=True)
                print("EMPEZAR")
            bt_inicio_pressed = False

        # print(time.time())
        # await asyncio.sleep(1.0/FPS)

    thread_communication.join()
    root.destroy()
    npdp.close()
    print("Finalizado")


customtkinter.set_appearance_mode("dark")
root = customtkinter.CTk(COLOR_BACKGROUND_IDLE)
root.title("Na Punta Dos Pes APP")
root.geometry("450x800")
root.protocol("WM_DELETE_WINDOW", close_app)

font_estado = customtkinter.CTkFont(family="", size=24)     # 16 - 30
font_variable = customtkinter.CTkFont(family="", size=16)   # 12 - 25
font_numero = customtkinter.CTkFont(family="", size=24)     # 22 - 30
font_tiempo = customtkinter.CTkFont(family="", size=20)     # 16 - 25
font_boton = customtkinter.CTkFont(family="", size=24)      # 16 - 50

# Frame Barras
FRAME_BAR_WIDTH = 400
FRAME_BAR_HEIGHT = 300
FRAME_PADDING = 24
FRAME_CORNER = 36

frame_bar = customtkinter.CTkFrame(master=root, width=FRAME_BAR_WIDTH, height=FRAME_BAR_HEIGHT,
                                   fg_color=COLOR_SECONDARY_IDLE, corner_radius=FRAME_CORNER)
frame_bar.place_configure(anchor=N, relx=225.0*1.0/450.0, rely=88.0*1.0/800.0)

frame_bar_int = customtkinter.CTkFrame(master=frame_bar, width=FRAME_BAR_WIDTH - FRAME_PADDING*2,
                                       height=FRAME_BAR_HEIGHT- FRAME_PADDING*2, fg_color="transparent")
frame_bar_int.place_configure(anchor=CENTER, relx=0.5, rely=0.5)

frame_bar_barras = customtkinter.CTkFrame(master=frame_bar_int, width=(FRAME_BAR_WIDTH - FRAME_PADDING*2)/2,
                                       height=FRAME_BAR_HEIGHT- FRAME_PADDING*2, fg_color="transparent")
frame_bar_barras.pack(side=RIGHT, expand=True, fill=BOTH)
frame_bar_barras.pack_propagate(False)

frame_bar_letra = customtkinter.CTkFrame(master=frame_bar_int,  width=(FRAME_BAR_WIDTH - FRAME_PADDING*2)/2,
                                       height=FRAME_BAR_HEIGHT- FRAME_PADDING*2, fg_color="transparent")
frame_bar_letra.pack(side=LEFT, expand=True, fill=BOTH)
frame_bar_letra.grid_propagate(False)

bar_angulo = customtkinter.CTkProgressBar(master=frame_bar_barras, orientation="vertical", width=26, height=FRAME_BAR_HEIGHT- FRAME_PADDING*2)
bar_angulo.pack(side=RIGHT, padx=4)
bar_angulo_min = customtkinter.CTkProgressBar(master=frame_bar_barras, orientation="vertical", width=26, height=FRAME_BAR_HEIGHT- FRAME_PADDING*2)
bar_angulo_min.pack(side=RIGHT, padx=4)
bar_angulo_prom = customtkinter.CTkProgressBar(master=frame_bar_barras, orientation="vertical", width=26, height=FRAME_BAR_HEIGHT- FRAME_PADDING*2)
bar_angulo_prom.pack(side=RIGHT, padx=4)
bar_angulo_max = customtkinter.CTkProgressBar(master=frame_bar_barras, orientation="vertical", width=26, height=FRAME_BAR_HEIGHT- FRAME_PADDING*2)
bar_angulo_max.pack(side=RIGHT, padx=4)

image_max = customtkinter.CTkImage(Image.open("icon_max_white.png"), size=(24,24))
icon_max = customtkinter.CTkLabel(bar_angulo_max, corner_radius=10, image=image_max, text="",
                                  fg_color="transparent")
icon_max.place_configure(anchor=CENTER, relx=0.5, rely=0.5)

image_min = customtkinter.CTkImage(Image.open("icon_min_white.png"), size=(24,24))
icon_min = customtkinter.CTkLabel(bar_angulo_min, corner_radius=10, image=image_min, text="",
                                  fg_color="transparent")
icon_min.place_configure(anchor=CENTER, relx=0.5, rely=0.5)

image_prom = customtkinter.CTkImage(Image.open("icon_avg_white.png"), size=(24,24))
icon_prom = customtkinter.CTkLabel(bar_angulo_prom, corner_radius=10, image=image_prom, text="",
                                  fg_color="transparent")
icon_prom.place_configure(anchor=CENTER, relx=0.5, rely=0.5)

lbl_angulo_max_title =  customtkinter.CTkLabel(frame_bar_letra, text="Ángulo máximo", font=font_variable)
lbl_angulo_max_title.grid(column=0, columnspan=1, row=0, rowspan=1, sticky="W")
lbl_angulo_max = customtkinter.CTkLabel(frame_bar_letra, text="--", font=font_numero)
lbl_angulo_max.grid(column=0, columnspan=1, row=1, rowspan=1, sticky="W", padx=(16, 0), pady=(2, 0))
lbl_angulo_prom_title =  customtkinter.CTkLabel(frame_bar_letra, text="Ángulo promedio", font=font_variable)
lbl_angulo_prom_title.grid(column=0, columnspan=1, row=2, rowspan=1, sticky="W", pady=(7, 0))
lbl_angulo_prom = customtkinter.CTkLabel(frame_bar_letra, text="--", font=font_numero)
lbl_angulo_prom.grid(column=0, columnspan=1, row=3, rowspan=1, sticky="W", padx=(16, 0), pady=(2, 0))
lbl_angulo_min_title =  customtkinter.CTkLabel(frame_bar_letra, text="Ángulo mínimo", font=font_variable)
lbl_angulo_min_title.grid(column=0, columnspan=1, row=4, rowspan=1, sticky="W", pady=(7, 0))
lbl_angulo_min = customtkinter.CTkLabel(frame_bar_letra, text="--", font=font_numero)
lbl_angulo_min.grid(column=0, columnspan=1, row=5, rowspan=1, sticky="W", padx=(16, 0), pady=(2, 0))
lbl_angulo_title =  customtkinter.CTkLabel(frame_bar_letra, text="Ángulo", font=font_variable)
lbl_angulo_title.grid(column=0, columnspan=1, row=6, rowspan=1, sticky="W", pady=(7, 0))
lbl_angulo = customtkinter.CTkLabel(frame_bar_letra, text="--", font=font_numero)
lbl_angulo.grid(column=0, columnspan=1, row=7, rowspan=1, sticky="W", padx=(16, 0), pady=(2, 0))

# Frame tiempos
FRAME_TIEMPOS_HEIGHT = 160

frame_tiempos = customtkinter.CTkFrame(master=root, width=FRAME_BAR_WIDTH, fg_color=COLOR_SECONDARY_IDLE, height=FRAME_TIEMPOS_HEIGHT, corner_radius=FRAME_CORNER)
frame_tiempos.place_configure(anchor=N, relx=225.0*1.0/450.0, rely=425.0*1.0/800.0)

frame_tiempos_int = customtkinter.CTkFrame(master=frame_tiempos, width=FRAME_BAR_WIDTH-FRAME_PADDING*2, height=FRAME_TIEMPOS_HEIGHT-FRAME_PADDING*2, fg_color="transparent")
frame_tiempos_int.place_configure(anchor=CENTER, relx=0.5, rely=0.5)
frame_tiempos_int.grid_propagate(False)

lbl_tiempo_subida = customtkinter.CTkLabel(frame_tiempos_int, text="Tiempo de subida", font=font_variable)
lbl_tiempo_subida.grid(column=0, columnspan=1, row=0, rowspan=1, sticky="W", padx=(0, 0), pady=(20, 0))
lbl_tiempo_subida_tiempo = customtkinter.CTkLabel(frame_tiempos_int, text="0.000", font=font_tiempo)
lbl_tiempo_subida_tiempo.grid(column=1, columnspan=1, row=0, rowspan=1, sticky="E", padx=(115, 0), pady=(20, 0))
lbl_tiempo_subida_seg = customtkinter.CTkLabel(frame_tiempos_int, text="s", font=font_tiempo)
lbl_tiempo_subida_seg.grid(column=2, columnspan=1, row=0, rowspan=1, sticky="E", padx=(5, 0), pady=(20, 0))

lbl_tiempo_arriba = customtkinter.CTkLabel(frame_tiempos_int, text="Tiempo de puntillas", font=font_variable)
lbl_tiempo_arriba.grid(column=0, columnspan=1, row=1, rowspan=1, sticky="W", padx=(0, 0), pady=(20, 0))
lbl_tiempo_arriba_tiempo = customtkinter.CTkLabel(frame_tiempos_int, text="0.000", font=font_tiempo)
lbl_tiempo_arriba_tiempo.grid(column=1, columnspan=1, row=1, rowspan=1, sticky="E", padx=(115, 0), pady=(20, 0))
lbl_tiempo_arriba_seg = customtkinter.CTkLabel(frame_tiempos_int, text="s", font=font_tiempo)
lbl_tiempo_arriba_seg.grid(column=2, columnspan=1, row=1, rowspan=1, sticky="E", padx=(5, 0), pady=(20, 0))

bt_inicio = customtkinter.CTkButton(master=root, text="Iniciar", command=lambda: button_event(),
                                    width=175, height=50, corner_radius=25, font=font_boton,
                                    fg_color=COLOR_ACCENT_IDLE)
bt_inicio.place_configure(anchor=N, relx=225.0*1.0/450, rely=615.0*1.0/800)

lbl_estado_sensor = customtkinter.CTkLabel(master=root, text=ESTADOS_SENSOR[0], text_color="white",
                                           font=font_estado, fg_color="transparent")
lbl_estado_sensor.place_configure(anchor=N, relx=225.0*1.0/450, rely=30.0*1.0/800.0)

image_usb = customtkinter.CTkImage(Image.open("icon_usb_white.png"), size=(24,24))
icon_usb = customtkinter.CTkLabel(root, corner_radius=10, image=image_usb, text="",
                                  fg_color="transparent")
icon_usb.place_configure(anchor=NE, relx=(450-FRAME_PADDING/2)/450, y=FRAME_PADDING/2)

customtkinter.deactivate_automatic_dpi_awareness()

npdp = NPDPDevice(callback=callback)

asyncio.run(main())