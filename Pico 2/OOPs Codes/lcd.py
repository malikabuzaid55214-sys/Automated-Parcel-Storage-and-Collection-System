# ============================================================
# SMART PARCEL SYSTEM
# PICO 2
# 16x2 I2C LCD Driver
# Version 1.0
# ============================================================

import time
import busio


class LCD:

    # ========================================================
    # LCD Constants
    # ========================================================

    LCD_BACKLIGHT = 0x08
    ENABLE = 0x04
    RS = 0x01

    # ========================================================
    # Constructor
    # ========================================================

    def __init__(self,
                 scl_pin,
                 sda_pin,
                 address=0x27):

        self.address = address

        self.i2c = busio.I2C(scl_pin, sda_pin)

        while not self.i2c.try_lock():
            pass

        self.initialize()

    # ========================================================
    # Low-Level Functions
    # ========================================================

    def write(self, data):

        self.i2c.writeto(

            self.address,

            bytes([data | self.LCD_BACKLIGHT])

        )

    def toggle(self, data):

        self.write(data | self.ENABLE)

        time.sleep(0.001)

        self.write(data & ~self.ENABLE)

        time.sleep(0.001)

    def send(self, value, mode):

        high = value & 0xF0
        low = (value << 4) & 0xF0

        self.toggle(high | mode)
        self.toggle(low | mode)

    def command(self, cmd):

        self.send(cmd, 0)

    def data(self, value):

        self.send(value, self.RS)

    # ========================================================
    # LCD Functions
    # ========================================================

    def clear(self):

        self.command(0x01)

        time.sleep(0.01)

    def cursor(self, col, row):

        rows = [0x80, 0xC0]

        self.command(rows[row] + col)

    def print(self, text):

        for c in text[:16]:

            self.data(ord(c))

    # ========================================================
    # Display Two Lines
    # ========================================================

    def show(self,
             line1="",
             line2=""):

        self.clear()

        self.cursor(0, 0)
        self.print(line1)

        self.cursor(0, 1)
        self.print(line2)

    # ========================================================
    # Ready Screens
    # ========================================================

    def ready(self):

        self.show(

            "SMART PARCEL",

            "Enter PIN"

        )

    def waiting(self):

        self.show(

            "SMART PARCEL",

            "Waiting..."

        )

    def storage_full(self):

        self.show(

            "STORAGE FULL",

            "Call Staff"

        )

    def locked(self):

        self.show(

            "SYSTEM LOCKED",

            "CALL ADMIN"

        )

    def success(self,
                message="Success"):

        self.show(

            "SUCCESS",

            message

        )

    def error(self,
              message="Wrong PIN"):

        self.show(

            "ERROR",

            message

        )

    def custom(self,
               line1="",
               line2=""):

        self.show(

            line1,

            line2

        )

    # ========================================================
    # LCD Initialization
    # ========================================================

    def initialize(self):

        time.sleep(0.05)

        self.command(0x33)
        self.command(0x32)
        self.command(0x28)
        self.command(0x0C)
        self.command(0x06)
        self.command(0x01)

        time.sleep(0.05)