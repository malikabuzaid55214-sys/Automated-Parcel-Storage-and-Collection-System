# ============================================================
# SMART PARCEL SYSTEM
# PICO 1
# Laser Sensor Driver
# Version 1.0
# ============================================================

import time
from analogio import AnalogIn


class LaserSensor:

    # ========================================================
    # Constructor
    # ========================================================

    def __init__(self,
                 pin,
                 threshold=400,
                 max_lux=1000):

        self.ldr = AnalogIn(pin)

        self.threshold = threshold
        self.max_lux = max_lux

    # ========================================================
    # Map Value
    # ========================================================

    def map_value(self,
                  x,
                  in_min,
                  in_max,
                  out_min,
                  out_max):

        return int(

            (x - in_min)

            * (out_max - out_min)

            / (in_max - in_min)

            + out_min

        )

    # ========================================================
    # Raw ADC Reading
    # ========================================================

    def raw(self):

        return self.ldr.value

    # ========================================================
    # Light Intensity
    # ========================================================

    def lux(self):

        value = self.map_value(

            self.raw(),

            65535,
            0,

            0,
            self.max_lux

        )

        return max(

            0,

            min(self.max_lux, value)

        )

    # ========================================================
    # Parcel Detection
    # ========================================================

    def detected(self):

        return self.lux() < self.threshold

    # ========================================================
    # Wait For Parcel
    # ========================================================

    def wait(self, lcd=None):

        print("Waiting For Parcel...")

        if lcd:

            lcd.waiting()

        while True:

            lux = self.lux()

            print("Lux :", lux)

            if lux < self.threshold:

                print("Parcel Detected!")

                if lcd:

                    lcd.detected()

                time.sleep(1)

                return True

            time.sleep(0.2)

    # ========================================================
    # Monitor Sensor
    # ========================================================

    def monitor(self):

        while True:

            print(

                "Raw :", self.raw(),

                " Lux :", self.lux()

            )

            time.sleep(0.2)