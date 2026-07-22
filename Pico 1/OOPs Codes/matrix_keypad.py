# ============================================================
# SMART PARCEL SYSTEM
# PICO 1
# Matrix Keypad Driver
# Version 1.0
# ============================================================

import keypad
import time


class MatrixKeypad:

    # ========================================================
    # Key Layout
    # ========================================================

    KEYS = [

        "1", "2", "3", "A",
        "4", "5", "6", "B",
        "7", "8", "9", "C",
        "*", "0", "#", "D"

    ]

    # ========================================================
    # Constructor
    # ========================================================

    def __init__(self,
                 row_pins,
                 column_pins,
                 valid_ids=None):

        self.matrix = keypad.KeyMatrix(

            row_pins=row_pins,

            column_pins=column_pins,

            columns_to_anodes=False

        )

        self.valid_ids = valid_ids or ()

    # ========================================================
    # Read One Key
    # ========================================================

    def get_key(self):

        event = self.matrix.events.get()

        if event and event.pressed:

            return self.KEYS[event.key_number]

        return None

    # ========================================================
    # Read Student ID
    # ========================================================

    def read_student_id(self, lcd=None):

        student_id = ""

        if lcd:

            lcd.ready()

        while True:

            key = self.get_key()

            if key is None:

                continue

            print("Key:", key)

            # ------------------------------------------------
            # Number
            # ------------------------------------------------

            if key.isdigit():

                if len(student_id) < 3:

                    student_id += key

                    if lcd:

                        lcd.custom(

                            "Student ID",

                            student_id

                        )

            # ------------------------------------------------
            # Clear
            # ------------------------------------------------

            elif key == "*":

                student_id = ""

                if lcd:

                    lcd.custom(

                        "Input Cleared",

                        ""

                    )

                    time.sleep(1)

                    lcd.ready()

            # ------------------------------------------------
            # Confirm
            # ------------------------------------------------

            elif key == "#":

                return student_id

    # ========================================================
    # Verify Student ID
    # ========================================================

    def verify(self, lcd=None):

        while True:

            student = self.read_student_id(lcd)

            # ------------------------------------------------
            # Valid Student ID
            # ------------------------------------------------

            if student in self.valid_ids:

                if lcd:

                    lcd.correct(student)

                    time.sleep(1)

                return student

            # ------------------------------------------------
            # Invalid Student ID
            # ------------------------------------------------

            if lcd:

                lcd.wrong(student)

                time.sleep(2)

                lcd.ready()