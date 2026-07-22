# ============================================================
# SMART PARCEL SYSTEM
# PICO 2 W
# WiFi Connection Manager
# Version 2.0
# ============================================================

import time
import ssl

import wifi
import socketpool
import adafruit_requests


class WiFiConnect:

    # ========================================================
    # Constructor
    # ========================================================

    def __init__(self,
                 ssid,
                 password,
                 timeout=15):

        self.ssid = ssid
        self.password = password
        self.timeout = timeout

        self.pool = None
        self.requests = None

    # ========================================================
    # Connect to WiFi
    # ========================================================

    def connect(self):

        if self.is_connected():

            return True

        print("--------------------------------")
        print("Connecting WiFi...")
        print("--------------------------------")

        try:

            wifi.radio.connect(

                self.ssid,

                self.password,

                timeout=self.timeout

            )

            self.pool = socketpool.SocketPool(

                wifi.radio

            )

            self.requests = adafruit_requests.Session(

                self.pool,

                ssl.create_default_context()

            )

            print("--------------------------------")
            print("WiFi Connected")
            print("IP :", wifi.radio.ipv4_address)
            print("--------------------------------")

            return True

        except Exception as error:

            print("--------------------------------")
            print("WiFi Connection Failed")
            print(error)
            print("--------------------------------")

            return False

    # ========================================================
    # Check Connection
    # ========================================================

    def is_connected(self):

        return wifi.radio.connected

    # ========================================================
    # Reconnect
    # ========================================================

    def reconnect(self):

        if self.is_connected():

            return True

        print("WiFi Lost")

        for attempt in range(3):

            print("Reconnect Attempt", attempt + 1)

            if self.connect():

                return True

            time.sleep(2)

        return False

    # ========================================================
    # Requests Session
    # ========================================================

    def get_requests(self):

        return self.requests
