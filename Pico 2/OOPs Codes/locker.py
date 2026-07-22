# ============================================================
# locker.py
# SMART PARCEL SYSTEM
# Parcel Storage Manager
# Version 2.0
# ============================================================

import time
import random


class Locker:

    # ========================================================
    # Constructor
    # ========================================================

    def __init__(self,
                 lcd,
                 third_gate,
                 second_gate,
                 telegram=None):

        self.lcd = lcd

        self.third_gate = third_gate
        self.second_gate = second_gate

        # Telegram Object
        self.telegram = telegram

        # Storage Floors
        self.locker = {

            "GROUND": None,

            "SECOND": None,

            "THIRD": None

        }

        # Parcel Database
        self.database = {}

        # Current destination when storing
        self.current_floor = None

        # Mechanical Busy Flag
        self.busy = False

    # ========================================================
    # Generate Unique PIN
    # ========================================================

    def generate_pin(self):

        while True:

            pin = str(random.randint(1000, 9999))

            if pin not in self.database:

                return pin

    # ========================================================
    # Find Empty Floor
    # ========================================================

    def find_empty(self):

        if self.locker["GROUND"] is None:

            return "GROUND"

        elif self.locker["SECOND"] is None:

            return "SECOND"

        elif self.locker["THIRD"] is None:

            return "THIRD"

        return None

    # ========================================================
    # Store Parcel
    # ========================================================

    def store(self, student_id):

        floor = self.find_empty()

        if floor is None:

            return None

        pin = self.generate_pin()

        self.database[pin] = {

            "student": student_id,

            "floor": floor,

            "status": "WAITING"

        }

        self.locker[floor] = pin

        self.current_floor = floor

        print("--------------------------------")
        print("Parcel Stored")
        print("Student :", student_id)
        print("PIN     :", pin)
        print("Floor   :", floor)
        print("--------------------------------")

        self.lcd.custom(

            "Parcel Stored",

            floor

        )

        time.sleep(2)

        return pin

    # ========================================================
    # Move Newly Stored Parcel
    # ========================================================

    def move(self):

        self.busy = True

        floor = self.current_floor

        # ----------------------------------------------------
        # Ground Floor
        # ----------------------------------------------------

        if floor == "GROUND":

            self.lcd.custom(

                "Moving To",

                "Ground"

            )

            self.third_gate.open()

            time.sleep(2)

            self.second_gate.open()

            time.sleep(4)

            self.second_gate.close()

            time.sleep(2)

            self.third_gate.close()

        # ----------------------------------------------------
        # Second Floor
        # ----------------------------------------------------

        elif floor == "SECOND":

            self.lcd.custom(

                "Moving To",

                "Second"

            )

            self.third_gate.open()

            time.sleep(8)

            self.third_gate.close()

        # ----------------------------------------------------
        # Third Floor
        # ----------------------------------------------------

        elif floor == "THIRD":

            self.lcd.custom(

                "Stored At",

                "Third Floor"

            )

            time.sleep(2)

        self.lcd.custom(

            "Storage",

            "Completed"

        )

        time.sleep(2)

        self.busy = False
            # ========================================================
    # Remove Parcel
    # ========================================================

    def remove(self, pin):

        floor = self.database[pin]["floor"]

        print("--------------------------------")
        print("Removing Parcel")
        print("PIN   :", pin)
        print("Floor :", floor)
        print("--------------------------------")

        # Remove parcel from database

        del self.database[pin]

        # Empty floor

        self.locker[floor] = None

        # Shift remaining parcels

        self.shift_down(floor)


    # ========================================================
    # Shift Remaining Parcels
    # ========================================================

    def shift_down(self, empty_floor):

        self.busy = True

        # Allow student to move away first

        time.sleep(2)

        # ----------------------------------------------------
        # Ground Parcel Collected
        # ----------------------------------------------------

        if empty_floor == "GROUND":

            # ================================================
            # Second -> Ground
            # ================================================

            if self.locker["SECOND"] is not None:

                self.lcd.custom(

                    "Shifting",

                    "2nd->Ground"

                )

                self.second_gate.open()

                time.sleep(4)

                self.second_gate.close()

                pin = self.locker["SECOND"]

                self.locker["GROUND"] = pin
                self.locker["SECOND"] = None

                self.database[pin]["floor"] = "GROUND"

                student = self.database[pin]["student"]

                if self.telegram:

                    self.telegram.update_floor(

                        student,

                        "GROUND"

                    )

                    self.telegram.notify_shift(

                        student,

                        "GROUND"

                    )

                print("Second -> Ground")

            # ================================================
            # Third -> Second
            # ================================================

            if self.locker["THIRD"] is not None:

                self.lcd.custom(

                    "Shifting",

                    "3rd->Second"

                )

                self.third_gate.open()

                time.sleep(8)

                self.third_gate.close()

                pin = self.locker["THIRD"]

                self.locker["SECOND"] = pin
                self.locker["THIRD"] = None

                self.database[pin]["floor"] = "SECOND"

                student = self.database[pin]["student"]

                if self.telegram:

                    self.telegram.update_floor(

                        student,

                        "SECOND"

                    )

                    self.telegram.notify_shift(

                        student,

                        "SECOND"

                    )

                print("Third -> Second")

        # ----------------------------------------------------
        # Second Parcel Collected
        # ----------------------------------------------------

        elif empty_floor == "SECOND":

            if self.locker["THIRD"] is not None:

                self.lcd.custom(

                    "Shifting",

                    "3rd->Second"

                )

                self.third_gate.open()

                time.sleep(8)

                self.third_gate.close()

                pin = self.locker["THIRD"]

                self.locker["SECOND"] = pin
                self.locker["THIRD"] = None

                self.database[pin]["floor"] = "SECOND"

                student = self.database[pin]["student"]

                if self.telegram:

                    self.telegram.update_floor(

                        student,

                        "SECOND"

                    )

                    self.telegram.notify_shift(

                        student,

                        "SECOND"

                    )

                print("Third -> Second")

        # ----------------------------------------------------
        # Third Parcel Collected
        # ----------------------------------------------------

        elif empty_floor == "THIRD":

            print("No Parcel Above Third Floor")

        self.lcd.custom(

            "Shift",

            "Completed"

        )

        time.sleep(2)

        self.status()

        self.busy = False
            # ========================================================
    # Get Parcel
    # ========================================================

    def get(self, pin):

        return self.database.get(pin)

    # ========================================================
    # Check Empty
    # ========================================================

    def is_empty(self):

        return (

            self.locker["GROUND"] is None and
            self.locker["SECOND"] is None and
            self.locker["THIRD"] is None

        )

    # ========================================================
    # Check Full
    # ========================================================

    def is_full(self):

        return (

            self.locker["GROUND"] is not None and
            self.locker["SECOND"] is not None and
            self.locker["THIRD"] is not None

        )

    # ========================================================
    # Check Busy
    # ========================================================

    def is_busy(self):

        return self.busy

    # ========================================================
    # Show Locker Status
    # ========================================================

    def status(self):

        print()

        print("========== LOCKER ==========")

        for floor in ["GROUND", "SECOND", "THIRD"]:

            pin = self.locker[floor]

            if pin is None:

                print(floor, ": EMPTY")

            else:

                student = self.database[pin]["student"]

                print(

                    floor,

                    ":",

                    pin,

                    "Student:",

                    student

                )

        print("============================")
        print()