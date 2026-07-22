# ============================================================
# SMART PARCEL SYSTEM
# PICO 2 W
# Main Program
# Version 2.0
# ============================================================

import digitalio

from config import *

from lcd import LCD
from matrix_keypad import MatrixKeypad
from servo import ContinuousServo
from buzzer import SecuritySystem
from locker import Locker
from pickup import PickupSystem
from uart import UARTReceiver

from wifi_connect import WiFiConnect
from telegram import TelegramBot


# ============================================================
# LCD
# ============================================================

lcd = LCD(

    LCD_SCL,

    LCD_SDA,

    LCD_ADDRESS

)

lcd.custom(

    "SMART PARCEL",

    "Starting..."

)

# ============================================================
# Matrix Keypad
# ============================================================

keypad = MatrixKeypad(

    row_pins=KEYPAD_ROWS,

    column_pins=KEYPAD_COLS

)

# ============================================================
# UART
# ============================================================

uart = UARTReceiver(

    UART_RX

)

# ============================================================
# Security System
# ============================================================

security = SecuritySystem(

    GREEN_LED_PIN,

    RED_LED_PIN,

    BUZZER_PIN,

    BUZZER_FREQUENCY

)

# ============================================================
# Floor Gates
# ============================================================

third_gate = ContinuousServo(

    THIRD_GATE_PIN,

    THIRD_GATE_SPEED,

    SERVO_MOVE_TIME

)

second_gate = ContinuousServo(

    SECOND_GATE_PIN,

    SECOND_GATE_SPEED,

    SERVO_MOVE_TIME

)

# ============================================================
# Collection Doors
# ============================================================

ground_door = ContinuousServo(

    GROUND_DOOR_PIN,

    GROUND_DOOR_SPEED,

    SERVO_MOVE_TIME

)

second_door = ContinuousServo(

    SECOND_DOOR_PIN,

    SECOND_DOOR_SPEED,

    SERVO_MOVE_TIME

)

third_door = ContinuousServo(

    THIRD_DOOR_PIN,

    THIRD_DOOR_SPEED,

    SERVO_MOVE_TIME

)

# ============================================================
# Door Dictionary
# ============================================================

doors = {

    "GROUND": ground_door,

    "SECOND": second_door,

    "THIRD": third_door

}

# ============================================================
# WiFi
# ============================================================

lcd.custom(

    "Connecting",

    "WiFi..."

)

wifi = WiFiConnect(

    WIFI_SSID,

    WIFI_PASSWORD

)

wifi.connect()

# ============================================================
# Telegram
# ============================================================

telegram = TelegramBot(

    BOT_TOKEN,

    wifi.get_requests()

)

# ============================================================
# Locker
# ============================================================

locker = Locker(

    lcd,

    third_gate,

    second_gate,
    
    telegram

)

# ============================================================
# Pickup System
# ============================================================

pickup = PickupSystem(

    lcd=lcd,

    keypad=keypad,

    security=security,

    locker=locker,

    doors=doors,

    admin_pin=ADMIN_PIN,

    telegram=telegram,

    door_open_time=DOOR_OPEN_TIME

)

telegram.pickup = pickup

# ============================================================
# Storage Status Output
# ============================================================

storage_status = digitalio.DigitalInOut(

    STORAGE_STATUS_PIN

)

storage_status.direction = digitalio.Direction.OUTPUT

storage_status.value = True

# ============================================================
# Startup
# ============================================================

print("======================================")
print(" SMART PARCEL SYSTEM")
print(" PICO 2 W")
print("======================================")

print("WiFi Connected")

print("Telegram Ready")

print("System Ready")

lcd.ready()

# ============================================================
# Main Loop
# ============================================================

while True:

    # --------------------------------------------------------
    # Alarm Update
    # --------------------------------------------------------

    security.update()

    # --------------------------------------------------------
    # Storage Status
    # --------------------------------------------------------

    storage_status.value = not locker.is_full()

    # --------------------------------------------------------
    # WiFi Reconnect
    # --------------------------------------------------------

    wifi.reconnect()

    telegram.set_requests(

        wifi.get_requests()

    )

    # --------------------------------------------------------
    # UART Receive
    # --------------------------------------------------------

    message = uart.receive()

    if message:

        print("UART :", message)

        parts = message.split(",")

        if len(parts) == 2:

            command = parts[0]

            student = parts[1]

            if command == "STORE":

                pickup.receive(student)

        else:

            print("Invalid UART Message")

    # --------------------------------------------------------
    # Student Keypad
    # --------------------------------------------------------

    pickup.check_pin()

    # --------------------------------------------------------
    # Telegram
    # --------------------------------------------------------

    pickup.check_telegram()
