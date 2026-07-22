# ============================================================
# SMART PARCEL SYSTEM
# PICO 1
# Delivery Controller
# Version 1.0
# ============================================================

import time


class DeliverySystem:

    # ========================================================
    # Constructor
    # ========================================================

    def __init__(self,
                 lcd,
                 keypad,
                 gate,
                 laser,
                 conveyor,
                 uart,
                 storage_ready):

        self.lcd = lcd
        self.keypad = keypad
        self.gate = gate
        self.laser = laser
        self.conveyor = conveyor
        self.uart = uart
        self.storage_ready = storage_ready

    # ========================================================
    # One Complete Delivery Cycle
    # ========================================================

    def process(self):

        # ----------------------------------------------------
        # Verify Student ID
        # ----------------------------------------------------

        student = self.keypad.verify(self.lcd)

        if student is None:

            return

        # ----------------------------------------------------
        # Check Storage Availability
        # ----------------------------------------------------

        if not self.storage_ready.value:

            self.lcd.custom(

                "Storage Full",

                "Try Later",

                color=self.lcd.RED

            )

            print("--------------------------------")
            print(" STORAGE FULL")
            print("--------------------------------")

            time.sleep(2)

            self.lcd.ready()

            return

        print("--------------------------------")
        print("Delivery Started")
        print("Student :", student)
        print("--------------------------------")

        # ----------------------------------------------------
        # Open Delivery Gate
        # ----------------------------------------------------

        self.lcd.gate_open()

        self.gate.open()

        print("Waiting for parcel...")

        time.sleep(5)

        # ----------------------------------------------------
        # Close Delivery Gate
        # ----------------------------------------------------

        self.gate.close()

        self.lcd.gate_closed()

        time.sleep(1)

        # ----------------------------------------------------
        # Wait For Parcel Detection
        # ----------------------------------------------------

        self.laser.wait(self.lcd)

        # ----------------------------------------------------
        # Run Conveyor
        # ----------------------------------------------------

        self.conveyor.run(self.lcd)

        # ----------------------------------------------------
        # Send Student ID to Pico 2
        # ----------------------------------------------------

        message = f"STORE,{student}"

        print("UART ->", message)

        self.uart.send(message)

        time.sleep(0.2)

        # ----------------------------------------------------
        # Ready For Next Delivery
        # ----------------------------------------------------

        print("--------------------------------")
        print("Delivery Completed")
        print("Ready For Next Parcel")
        print("--------------------------------")

        self.lcd.ready()