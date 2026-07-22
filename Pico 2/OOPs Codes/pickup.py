# ============================================================
# pickup.py
# Student Pickup & Parcel Controller
# Version 3.0
# ============================================================

import time


class PickupSystem:

    # ========================================================
    # Constructor
    # ========================================================

    def __init__(self,
                 lcd,
                 keypad,
                 security,
                 locker,
                 doors,
                 admin_pin,
                 telegram=None,
                 door_open_time=7):

        self.lcd = lcd
        self.keypad = keypad
        self.security = security
        self.locker = locker
        self.doors = doors

        self.admin_pin = admin_pin
        self.telegram = telegram

        self.door_open_time = door_open_time

        # Wrong PIN counter
        self.attempts = 0

        # LCD flags
        self.busy_screen = False
        self.lock_screen = False

    # ========================================================
    # Door Countdown
    # ========================================================

    def countdown(self):

        for sec in range(self.door_open_time, 0, -1):

            self.lcd.custom(

                "Collect Parcel",

                "Closing {}".format(sec)

            )

            time.sleep(1)

    # ========================================================
    # Safe Telegram Helper
    # ========================================================

    def notify(self, func, *args):

        if self.telegram is None:

            return

        try:

            func(*args)

        except Exception as error:

            print("--------------------------------")
            print("Telegram Error")
            print(error)
            print("--------------------------------")

    # ========================================================
    # Check PIN
    # ========================================================

    def check_pin(self):

        # ----------------------------------------------------
        # SECURITY LOCK
        # ----------------------------------------------------

        if self.security.alarm_active:

            # Show lock screen only once

            if not self.lock_screen:

                self.lcd.custom(

                    "SYSTEM LOCKED",

                    "ADMIN PIN"

                )

                self.lock_screen = True

            pin = self.keypad.process_code(

                lcd=self.lcd,

                length=4,

                title="ADMIN PIN"

            )

            if pin is None:

                return

            # Correct Admin PIN

            if pin == self.admin_pin:

                self.security.stop_alarm()

                self.attempts = 0

                self.lock_screen = False

                self.lcd.custom(

                    "System",

                    "Unlocked"

                )

                time.sleep(2)

                # Office parcel menu will be added in Part 3

                self.lcd.ready()

            return

        # ----------------------------------------------------
        # LOCKER BUSY
        # ----------------------------------------------------

        if self.locker.is_busy():

            if not self.busy_screen:

                self.lcd.custom(

                    "System Busy",

                    "Please Wait"

                )

                self.busy_screen = True

            return

        if self.busy_screen:

            self.busy_screen = False

            self.lcd.ready()

        # ----------------------------------------------------
        # READ PIN
        # ----------------------------------------------------

        pin = self.keypad.process_code(

            lcd=self.lcd,

            length=4,

            title="Enter PIN"

        )

        if pin is None:

            return

        # ----------------------------------------------------
        # ADMIN LOGIN
        # ----------------------------------------------------

        if pin == self.admin_pin:

            self.security.success()

            self.attempts = 0

            self.lcd.custom(

                "Administrator",

                "Access"

            )

            time.sleep(2)

            # Admin menu will replace this in Part 3

            self.lcd.ready()

            return

        # ----------------------------------------------------
        # STUDENT PIN
        # ----------------------------------------------------

        parcel = self.locker.get(pin)

        if parcel:

            # Office parcels cannot be collected by students

            if parcel["status"] == "OFFICE":

                self.lcd.custom(

                    "Parcel In",

                    "Office"

                )

                time.sleep(2)

                self.lcd.custom(

                    "Contact",

                    "Administrator"

                )

                time.sleep(2)

                self.lcd.ready()

                return

            if parcel["status"] == "WAITING":

                self.attempts = 0

                self.security.success()

                self.collect(pin)

                return

        # ----------------------------------------------------
        # WRONG PIN
        # ----------------------------------------------------

        self.attempts += 1

        self.security.error()

        self.lcd.custom(

            "Wrong PIN",

            "Attempt {}/3".format(self.attempts)

        )

        time.sleep(2)

        if self.attempts >= 3:

            self.security.alarm()

            self.lock_screen = False

            self.notify(

                self.telegram.notify_security

            )

            return

        self.lcd.ready()
            # ========================================================
    # Receive Parcel
    # ========================================================

    def receive(self, student_id):

        self.lcd.custom(

            "Parcel Arrived",

            student_id

        )

        time.sleep(2)

        # ----------------------------------------------------
        # Store Parcel
        # ----------------------------------------------------

        pin = self.locker.store(student_id)

        if pin is None:

            self.lcd.storage_full()

            self.notify(

                self.telegram.notify_storage_full

            )

            return

        # ----------------------------------------------------
        # Move Parcel Into Locker
        # ----------------------------------------------------

        self.locker.move()

        parcel = self.locker.get(pin)

        floor = parcel["floor"]

        # ----------------------------------------------------
        # Telegram
        # ----------------------------------------------------

        self.notify(

            self.telegram.notify_arrival,

            student_id,

            pin,

            floor

        )

        self.notify(

            self.telegram.notify_parcel_stored,

            student_id,

            floor

        )

        # ----------------------------------------------------
        # LCD
        # ----------------------------------------------------

        self.lcd.custom(

            "PIN Generated",

            "Check Telegram"

        )

        print("--------------------------------")
        print("Parcel Stored")
        print("Student :", student_id)
        print("PIN     :", pin)
        print("Floor   :", floor)
        print("--------------------------------")

        time.sleep(2)

        self.lcd.ready()


    # ========================================================
    # Collect Parcel (Student)
    # ========================================================

    def collect(self, pin):

        parcel = self.locker.get(pin)

        if parcel is None:

            return

        floor = parcel["floor"]

        student_id = parcel["student"]

        door = self.doors[floor]

        self.lcd.custom(

            floor,

            "Door Opening"

        )

        door.open()

        self.countdown()

        self.lcd.custom(

            "Closing Door",

            "Please Wait"

        )

        door.close()

        self.locker.remove(pin)

        self.security.success()

        self.notify(

            self.telegram.notify_collected,

            student_id

        )

        self.lcd.custom(

            "Parcel",

            "Collected"

        )

        time.sleep(2)

        self.lcd.custom(

            "Thank You",

            "Have A Nice Day"

        )

        time.sleep(2)

        self.lcd.ready()


    # ========================================================
    # Move Parcel To Office
    # ========================================================

    def move_to_office(self, pin):

        parcel = self.locker.get(pin)

        if parcel is None:

            return

        if parcel["status"] == "OFFICE":

            return

        parcel["status"] = "OFFICE"

        self.lcd.custom(

            "Parcel Moved",

            "To Office"

        )

        print("--------------------------------")
        print("Parcel Moved To Office")
        print("PIN :", pin)
        print("--------------------------------")

        time.sleep(2)

        self.lcd.ready()


    # ========================================================
    # Admin Collect Office Parcel
    # ========================================================

    def collect_office(self, pin):

        parcel = self.locker.get(pin)

        if parcel is None:

            return False

        if parcel["status"] != "OFFICE":

            return False

        floor = parcel["floor"]

        student_id = parcel["student"]

        door = self.doors[floor]

        self.lcd.custom(

            "Office Parcel",

            floor

        )

        time.sleep(1)

        door.open()

        self.countdown()

        self.lcd.custom(

            "Closing Door",

            "Please Wait"

        )

        door.close()

        self.locker.remove(pin)

        self.notify(

            self.telegram.notify_collected,

            student_id

        )

        self.lcd.custom(

            "Office Parcel",

            "Collected"

        )

        time.sleep(2)

        self.lcd.ready()

        return True
        # ========================================================
    # Administrator Office Menu
    # ========================================================

    def admin_menu(self):

        office = self.locker.office_parcels()

        if len(office) == 0:

            self.lcd.custom(

                "No Office",

                "Parcels"

            )

            time.sleep(2)

            self.lcd.ready()

            return

        self.lcd.custom(

            "Office Parcel",

            "Press #"

        )

        while True:

            key = self.keypad.get_key()

            if key == "#":

                break

            if key == "*":

                self.lcd.ready()

                return

            time.sleep(0.05)

        # --------------------------------------------
        # Collect every office parcel
        # --------------------------------------------

        for pin, parcel in office:

            self.collect_office(pin)

        self.lcd.custom(

            "Office",

            "Completed"

        )

        time.sleep(2)

        self.lcd.ready()


    # ========================================================
    # Telegram Services
    # ========================================================

    def check_telegram(self):

        if self.telegram is None:

            return

        self.telegram.check_timers()

        self.telegram.poll()