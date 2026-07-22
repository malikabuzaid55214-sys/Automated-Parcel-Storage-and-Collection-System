# ============================================================
# SMART PARCEL SYSTEM
# PICO 1
# Grove RGB LCD Driver
# Version 1.0
# ============================================================

import time
import busio


class GroveLCD:

    # ========================================================
    # LCD I2C Addresses
    # ========================================================

    LCD_ADDR = 0x3E
    RGB_ADDR = 0x62

    # ========================================================
    # RGB Colors
    # ========================================================

    OFF     = (0, 0, 0)
    RED     = (255, 0, 0)
    GREEN   = (0, 255, 0)
    BLUE    = (0, 0, 255)
    YELLOW  = (255, 255, 0)
    CYAN    = (0, 255, 255)
    MAGENTA = (255, 0, 255)
    WHITE   = (255, 255, 255)

    # ========================================================
    # Constructor
    # ========================================================

    def __init__(self, scl_pin, sda_pin):

        self.i2c = busio.I2C(scl_pin, sda_pin)

        while not self.i2c.try_lock():
            pass

        self.initialize()

    # ========================================================
    # Low Level Functions
    # ========================================================

    def command(self, cmd):

        self.i2c.writeto(
            self.LCD_ADDR,
            bytes([0x80, cmd])
        )

    def data(self, value):

        self.i2c.writeto(
            self.LCD_ADDR,
            bytes([0x40, value])
        )

    def clear(self):

        self.command(0x01)

        time.sleep(0.05)

    def home(self):

        self.command(0x02)

        time.sleep(0.05)

    def cursor(self, col, row):

        rows = [0x80, 0xC0]

        self.command(rows[row] + col)

    def print(self, text):

        for c in text[:16]:

            self.data(ord(c))

    # ========================================================
    # High Level Functions
    # ========================================================

    def show(self, line1="", line2=""):

        self.clear()

        self.cursor(0, 0)
        self.print(line1)

        self.cursor(0, 1)
        self.print(line2)

    # ========================================================
    # RGB Backlight
    # ========================================================

    def color(self, rgb):

        r, g, b = rgb

        self.i2c.writeto(self.RGB_ADDR, bytes([0x00, 0x00]))
        self.i2c.writeto(self.RGB_ADDR, bytes([0x01, 0x00]))
        self.i2c.writeto(self.RGB_ADDR, bytes([0x08, 0xAA]))

        self.i2c.writeto(self.RGB_ADDR, bytes([0x04, r]))
        self.i2c.writeto(self.RGB_ADDR, bytes([0x03, g]))
        self.i2c.writeto(self.RGB_ADDR, bytes([0x02, b]))

    # ========================================================
    # Ready-Made Screens
    # ========================================================

    def ready(self):

        self.color(self.BLUE)

        self.show(
            "Parcel System",
            "Enter ID"
        )

    def waiting(self):

        self.color(self.YELLOW)

        self.show(
            "Place Parcel",
            "Waiting..."
        )

    def detected(self):

        self.color(self.YELLOW)

        self.show(
            "Parcel Found",
            "Moving..."
        )

    def conveyor(self):

        self.color(self.CYAN)

        self.show(
            "Conveyor",
            "Running..."
        )

    def finished(self):

        self.color(self.GREEN)

        self.show(
            "Delivery Done",
            "Thank You"
        )

    def gate_open(self):

        self.color(self.GREEN)

        self.show(
            "Gate Open",
            "Place Parcel"
        )

    def gate_closed(self):

        self.show(
            "Gate Closed",
            ""
        )

    def correct(self, student):

        self.color(self.GREEN)

        self.show(
            "ID Correct",
            student
        )

    def wrong(self, student):

        self.color(self.RED)

        self.show(
            "Wrong ID",
            student
        )

    def custom(self, line1="", line2="", color=None):

        if color is not None:

            self.color(color)

        self.show(line1, line2)

    # ========================================================
    # LCD Initialization
    # ========================================================

    def initialize(self):

        self.command(0x38)
        self.command(0x39)
        self.command(0x14)
        self.command(0x70)
        self.command(0x56)
        self.command(0x6C)

        time.sleep(0.2)

        self.command(0x38)
        self.command(0x0C)
        self.command(0x01)

        time.sleep(0.05)