# ============================================================
# SMART PARCEL SYSTEM
# PICO 1
# Conveyor Driver
# Version 1.0
# ============================================================

import time
import digitalio


class Conveyor:

    # ========================================================
    # Constructor
    # ========================================================

    def __init__(self,
                 motor1_pins,
                 motor2_pins,
                 run_time=35,
                 run_delay=0.001):

        self.run_time = run_time
        self.run_delay = run_delay

        self.motor1 = []
        self.motor2 = []

        # ----------------------------------------------------
        # Initialize Motor 1
        # ----------------------------------------------------

        for pin in motor1_pins:

            output = digitalio.DigitalInOut(pin)
            output.direction = digitalio.Direction.OUTPUT
            output.value = False

            self.motor1.append(output)

        # ----------------------------------------------------
        # Initialize Motor 2
        # ----------------------------------------------------

        for pin in motor2_pins:

            output = digitalio.DigitalInOut(pin)
            output.direction = digitalio.Direction.OUTPUT
            output.value = False

            self.motor2.append(output)

        # ----------------------------------------------------
        # Half-Step Sequence
        # ----------------------------------------------------

        self.sequence = [

            [1, 0, 0, 0],
            [1, 1, 0, 0],
            [0, 1, 0, 0],
            [0, 1, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 1],
            [0, 0, 0, 1],
            [1, 0, 0, 1]

        ]

        self.reverse = list(reversed(self.sequence))

        # ----------------------------------------------------
        # Smooth Acceleration Ramp
        # ----------------------------------------------------

        self.ramp = [

            0.004,
            0.003,
            0.002,
            0.0015,
            0.0012,
            0.0010

        ]

    # ========================================================
    # Execute One Half-Step
    # ========================================================

    def step(self, delay):

        for step_index in range(8):

            for i, value in enumerate(self.reverse[step_index]):

                self.motor1[i].value = value

            for i, value in enumerate(self.sequence[step_index]):

                self.motor2[i].value = value

            time.sleep(delay)

    # ========================================================
    # Smooth Acceleration
    # ========================================================

    def accelerate(self):

        for delay in self.ramp:

            for _ in range(150):

                self.step(delay)

    # ========================================================
    # Stop Motors
    # ========================================================

    def stop(self):

        for pin in self.motor1:

            pin.value = False

        for pin in self.motor2:

            pin.value = False

    # ========================================================
    # Run Conveyor
    # ========================================================

    def run(self, lcd=None):

        print("--------------------------------")
        print("Starting Conveyor...")
        print("--------------------------------")

        if lcd:

            lcd.conveyor()

        # Smooth acceleration
        self.accelerate()

        # Constant speed
        start = time.monotonic()

        while (time.monotonic() - start) < self.run_time:

            self.step(self.run_delay)

        # Stop motors
        self.stop()

        print("--------------------------------")
        print("Conveyor Finished")
        print("--------------------------------")

        if lcd:

            lcd.finished()

            time.sleep(2)