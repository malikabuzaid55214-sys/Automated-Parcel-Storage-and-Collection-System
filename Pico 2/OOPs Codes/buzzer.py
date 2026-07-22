# ============================================================
# SMART PARCEL SYSTEM
# PICO 2
# Security System
# Version 3.0
# ============================================================

import time
import pwmio
import digitalio


class SecuritySystem:

    # ========================================================
    # Constructor
    # ========================================================

    def __init__(self,
                 green_pin,
                 red_pin,
                 buzzer_pin,
                 frequency=2500):

        # Green LED
        self.green = digitalio.DigitalInOut(green_pin)
        self.green.direction = digitalio.Direction.OUTPUT
        self.green.value = False

        # Red LED
        self.red = digitalio.DigitalInOut(red_pin)
        self.red.direction = digitalio.Direction.OUTPUT
        self.red.value = False

        # Passive Buzzer
        self.buzzer = pwmio.PWMOut(
            buzzer_pin,
            frequency=frequency,
            duty_cycle=0
        )

        # Alarm Status
        self.alarm_active = False

        # Blink Timer
        self.last_blink = 0
        self.blink_interval = 0.08

    # ========================================================
    # Turn Everything OFF
    # ========================================================

    def off(self):

        self.green.value = False
        self.red.value = False
        self.buzzer.duty_cycle = 0

    # ========================================================
    # Short Beep
    # ========================================================

    def beep(self, duration=0.20):

        self.buzzer.duty_cycle = 32768

        time.sleep(duration)

        self.buzzer.duty_cycle = 0

    # ========================================================
    # Success Feedback
    # ========================================================

    def success(self):

        self.off()

        self.green.value = True

        self.beep(0.20)

        time.sleep(0.20)

        self.green.value = False

    # ========================================================
    # Error Feedback
    # ========================================================

    def error(self):

        self.off()

        self.red.value = True

        self.beep(0.40)

        time.sleep(0.20)

        self.red.value = False

    # ========================================================
    # Enable Alarm
    # ========================================================

    def alarm(self):

        self.alarm_active = True

        self.green.value = False
        self.red.value = False

        # Continuous buzzer
        self.buzzer.duty_cycle = 32768

        self.last_blink = time.monotonic()

        print("--------------------------------")
        print("SECURITY ALARM ACTIVATED")
        print("--------------------------------")

    # ========================================================
    # Disable Alarm
    # ========================================================

    def stop_alarm(self):

        self.alarm_active = False

        self.off()

        print("--------------------------------")
        print("SECURITY ALARM CLEARED")
        print("--------------------------------")

    # ========================================================
    # Update Alarm (Non-Blocking)
    # ========================================================

    def update(self):

        if not self.alarm_active:

            return

        # Keep buzzer continuously ON
        self.buzzer.duty_cycle = 32768

        now = time.monotonic()

        if (now - self.last_blink) >= self.blink_interval:

            self.last_blink = now

            self.green.value = not self.green.value
            self.red.value = not self.red.value

    # ========================================================
    # Blink LEDs
    # ========================================================

    def blink(self,
              times=5,
              interval=0.15):

        for _ in range(times):

            self.green.value = True
            self.red.value = True

            time.sleep(interval)

            self.green.value = False
            self.red.value = False

            time.sleep(interval)

    # ========================================================
    # Alarm Status
    # ========================================================

    def is_alarm_active(self):

        return self.alarm_active