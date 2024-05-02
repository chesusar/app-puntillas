import serial
import serial.tools.list_ports
import asyncio


class NPDPDevice:
    NPDP_VID = 4292
    NPDP_PID = 60000
    
    def __init__(self) -> None:
        self.is_open = False
    
    
    async def open(self):
        puertos = serial.tools.list_ports.comports()
        # print(len(puertos))
        for p in puertos:
            # print(p.device)
            # print(p.description)
            # print(p.vid)
            # print(p.pid)
            # print("---")
            if p.vid == self.NPDP_VID and p.pid == self.NPDP_PID:
                print("Connecting to " + p.device)
                self.is_open = True
    
    
    def close(self):
        if self.is_open:
            pass


async def main():
    npdp = NPDPDevice()
    while True:
        await npdp.open()
        if npdp.is_open:
            print("Connected")
            npdp.close()
            break
        await asyncio.sleep(0.1)


asyncio.run(main())
