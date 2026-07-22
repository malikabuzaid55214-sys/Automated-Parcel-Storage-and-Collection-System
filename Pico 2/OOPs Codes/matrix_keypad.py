# ============================================================
# SMART PARCEL SYSTEM
# PICO 2
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
                 column_pins):

        self.matrix = keypad.KeyMatrix(

            row_pins=row_pins,

            column_pins=column_pins,

            columns_to_anodes=False

        )

        self.code = ""
        self.title = ""

    # ========================================================
    # Read One Key
    # ========================================================

    def get_key(self):

        event = self.matrix.events.get()

        if event and event.pressed:

            key = self.KEYS[event.key_number]

            print("Key :", key)

            return key

        return None

    # ========================================================
    # Blocking PIN Reader
    # ========================================================

    def read_code(self,
                  lcd=None,
                  length=4,
                  title="Enter PIN"):

        code = ""

        if lcd:

            lcd.custom(

                "SMART PARCEL",

                title

            )

        while True:

            key = self.get_key()

            if key is None:

                continue

            # ------------------------------------------------
            # Number
            # ------------------------------------------------

            if key.isdigit():

                if len(code) < length:

                    code += key

                    if lcd:

                        lcd.custom(

                            title,

                            code

                        )

            # ------------------------------------------------
            # Clear
            # ------------------------------------------------

            elif key == "*":

                code = ""

                if lcd:

                    lcd.custom(

                        "Input Cleared",

                        ""

                    )

                time.sleep(1)

                if lcd:

                    lcd.custom(

                        title,

                        ""

                    )

            # ------------------------------------------------
            # Confirm
            # ------------------------------------------------

            elif key == "#":

                return code

    # ========================================================
    # Non-Blocking PIN Reader
    # ========================================================

    def process_code(self,
                     lcd=None,
                     length=4,
                     title="Enter PIN"):

        # Reset stored code if mode changed
        if title != self.title:

            self.title = title
            self.code = ""

        key = self.get_key()

        if key is None:

            return None

        # ------------------------------------------------
        # Number
        # ------------------------------------------------

        if key.isdigit():

            if len(self.code) < length:

                self.code += key

                if lcd:

                    lcd.custom(

                        title,

                        self.code

                    )

        # ------------------------------------------------
        # Clear
        # ------------------------------------------------

        elif key == "*":

            self.code = ""

            if lcd:

                lcd.custom(

                    "Input Cleared",

                    ""

                )

            time.sleep(1)

            if lcd:

                lcd.custom(

                    title,

                    ""

                )

        # ------------------------------------------------
        # Confirm
        # ------------------------------------------------

        elif key == "#":

            pin = self.code

            self.code = ""

            return pin

        return None

    # ========================================================
    # Wait For Specific Key
    # ========================================================

    def wait_for(self, wanted_key):

        while True:

            key = self.get_key()

            if key == wanted_key:

                return