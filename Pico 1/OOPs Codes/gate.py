# ============================================================
# SMART PARCEL SYSTEM
# PICO 1
# Gate Controller
# Version 1.0
# ============================================================

import time
import pwmio
from adafruit_motor import servo


class Gate:

    # ========================================================
    # Constructor
    # ========================================================

    def __init__(self,
                 pin,
                 speed=0.60,
                 move_time=0.40):

        pwm = pwmio.PWMOut(

            pin,

            frequency=50

        )

        self.servo = servo.ContinuousServo(pwm)

        self.speed = speed
        self.move_time = move_time

    # ========================================================
    # Open Gate
    # ========================================================

    def open(self):

        print("Opening Gate...")

        # Rotate servo
        self.servo.throttle = -self.speed

        time.sleep(self.move_time)

        # Stop servo
        self.servo.throttle = 0

    # ========================================================
    # Close Gate
    # ========================================================

    def close(self):

        print("Closing Gate...")

        # Rotate servo
        self.servo.throttle = self.speed

        time.sleep(self.move_time)

        # Stop servo
        self.servo.throttle = 0

    # ========================================================
    # Open Gate For Specific Time
    # ========================================================

    def open_for(self, seconds):

        self.open()

        time.sleep(seconds)

        self.close()

    # ========================================================
    # Stop Servo
    # ========================================================

    def stop(self):

        self.servo.throttle = 0

    # ========================================================
    # Reverse Servo Direction
    # ========================================================

    def reverse(self):

        self.speed = -self.speed