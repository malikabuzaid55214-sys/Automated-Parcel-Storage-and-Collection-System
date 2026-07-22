# ============================================================
# SMART PARCEL SYSTEM
# PICO 1
# UART Sender
# Version 1.0
# ============================================================

import busio


class UARTSender:

    # ========================================================
    # Constructor
    # ========================================================

    def __init__(self,
                 tx_pin,
                 baudrate=9600):

        self.uart = busio.UART(

            tx=tx_pin,

            baudrate=baudrate

        )

    # ========================================================
    # Send Message
    # ========================================================

    def send(self, message):

        # Ensure every message ends with a newline
        if not message.endswith("\n"):

            message += "\n"

        self.uart.write(

            message.encode()

        )