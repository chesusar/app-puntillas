import serial
import serial.tools.list_ports
import asyncio
import time


class NPDPDevice:
    NPDP_VID = 4292
    NPDP_PID = 60000
    PROTOCOL_BT = 0
    PROTOCOL_PORT = 1
    
    def __init__(self, callback, protocol = PROTOCOL_PORT) -> None:
        self.is_open = False
        self.callback = callback
        self.protocol = protocol
        self.serial = None
        self.recibido : bytes = b''
    

    def __del__(self):
        if self.protocol == self.PROTOCOL_PORT and self.serial.is_open:
            self.serial.close()


    def open(self):
        # await asyncio.sleep(0.1)
        puertos = serial.tools.list_ports.comports()
        for p in puertos:
            # print(p.device)
            # print(p.description)
            # print(p.vid)
            # print(p.pid)
            if p.vid == self.NPDP_VID and p.pid == self.NPDP_PID:
                print("Connecting to " + p.device)
                self.serial = serial.Serial(timeout=0)
                self.serial.baudrate = 115200
                self.serial.port = p.device
                try:
                    self.serial.open()
                except:
                    print("Port cannot be opened")
                else:
                    self.is_open = True
                
                break
    
    
    def close(self):
        if self.protocol == self.PROTOCOL_PORT and self.serial.is_open:
            self.is_open = False
            self.serial.close()
            print("NPDP closed")
    

    def update(self):
        if self.protocol == self.PROTOCOL_PORT and self.serial.is_open:
            self.recibido += self.serial.read_until(b"\n")
            decoded = self.recibido.decode()
            
            if decoded.find("\n") != -1:
                decoded = decoded.removesuffix("\n")
                decoded = decoded.split(' ')
                if len(decoded) == 2:
                    self.callback(decoded[0], decoded[1])
                self.recibido = b""
    

    def write(self, uuid, dato):
        if self.protocol == self.PROTOCOL_PORT and self.serial.is_open:
            # encoded = uuid + " " + str(dato) + "\n"
            # encoded = dato.encode()
            self.serial.write(dato)


# async def main():
#     npdp = NPDPDevice(callback=callback)
#     while True:
#         await npdp.open()
#         if npdp.is_open:
#             print("Connected")
#             break
#         await asyncio.sleep(0.1)
    
#     for i in range(50):
#         npdp.update()
#         print(time.time())
#         await asyncio.sleep(0.1)
    
#     npdp.close()


# def callback(uuid, dato):
#     print("Callback")
#     print(uuid)
#     print(dato)

# asyncio.run(main())
