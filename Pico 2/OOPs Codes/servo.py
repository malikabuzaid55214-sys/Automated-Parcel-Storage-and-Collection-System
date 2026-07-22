# ============================================================
# SMART PARCEL SYSTEM
# PICO 2
# Continuous Servo Driver
# Version 1.0
# ============================================================

import time
import pwmio
from adafruit_motor import servo


class ContinuousServo:

    # ========================================================
    # Constructor
    # ========================================================

    def __init__(self,
                 pin,
                 speed=0.30,
                 move_time=0.40):

        pwm = pwmio.PWMOut(

            pin,

            frequency=50

        )

        self.servo = servo.ContinuousServo(pwm)

        self.speed = speed
        self.move_time = move_time

    # ========================================================
    # Open Servo
    # ========================================================

    def open(self):

        # Rotate servo
        self.servo.throttle = -self.speed

        time.sleep(self.move_time)

        # Stop servo
        self.servo.throttle = 0

    # ========================================================
    # Close Servo
    # ========================================================

    def close(self):

        # Rotate servo
        self.servo.throttle = self.speed

        time.sleep(self.move_time)

        # Stop servo
        self.servo.throttle = 0

    # ========================================================
    # Open Servo For Specific Time
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