# ============================================================
# SMART PARCEL SYSTEM
# PICO 2
# UART Receiver
# Version 1.0
# ============================================================

import busio


class UARTReceiver:

    # ========================================================
    # Constructor
    # ========================================================

    def __init__(self,
                 rx_pin,
                 baudrate=9600):

        self.uart = busio.UART(

            rx=rx_pin,

            baudrate=baudrate

        )

    # ========================================================
    # Receive UART Message
    # ========================================================

    def receive(self):

        if not self.uart.in_waiting:

            return None

        data = self.uart.readline()

        if data is None:

            return None

        return data.decode().strip()