# ============================================================
# SMART PARCEL SYSTEM
# PICO 2 W
# Telegram Bot
# Version 4.0
# ============================================================

import time

from config import *


class TelegramBot:

    # ========================================================
    # Constructor
    # ========================================================

    def __init__(self,
                 bot_token,
                 requests):

        self.bot_token = bot_token
        self.requests = requests

        self.base_url = (
            "https://api.telegram.org/bot{}".format(
                bot_token
            )
        )

        # Telegram Polling

        self.offset = 0
        self.last_poll = 0
        self.poll_interval = 1

        # Pickup Reference

        self.pickup = None

        # Active Timers

        self.timers = {}

        # Waiting For Language Selection

        self.awaiting_language = {}

        # Current Languages

        self.languages = {}

        # Load default language from config

        for student_id, student in STUDENTS.items():

            self.languages[student_id] = student["language"]

    # ========================================================
    # Update HTTP Session
    # ========================================================

    def set_requests(self,
                     requests):

        self.requests = requests

    # ========================================================
    # Get Student
    # ========================================================

    def get_student(self,
                    student_id):

        return STUDENTS.get(student_id)

    # ========================================================
    # Get Chat ID
    # ========================================================

    def get_chat(self,
                 student_id):

        student = STUDENTS.get(student_id)

        if student:

            return student["chat_id"]

        return None

    # ========================================================
    # Get Student From Chat ID
    # ========================================================

    def get_student_by_chat(self,
                            chat_id):

        for student_id, student in STUDENTS.items():

            if str(student["chat_id"]) == str(chat_id):

                return student_id, student

        return None, None

    # ========================================================
    # Current Language
    # ========================================================

    def get_language(self,
                     student_id):

        return self.languages.get(

            student_id,

            "en"

        )

    # ========================================================
    # Localized Message
    # ========================================================

    def get_message(self,
                    key,
                    student_id,
                    **kwargs):

        language = self.get_language(

            student_id

        )

        if key not in MESSAGES:

            return ""

        message = MESSAGES[key].get(

            language,

            MESSAGES[key]["en"]

        )

        return message.format(

            **kwargs

        )

    # ========================================================
    # Send Telegram Message
    # ========================================================

    def send(self,
             chat_id,
             text):

        if self.requests is None:

            return False

        url = self.base_url + "/sendMessage"

        payload = {

            "chat_id": chat_id,

            "text": text

        }

        for attempt in range(

            TELEGRAM_RETRIES

        ):

            try:

                response = self.requests.post(

                    url,

                    json=payload

                )

                response.close()

                return True

            except Exception as error:

                print("--------------------------------")
                print("Telegram Error")
                print(error)
                print("Retry :", attempt + 1)
                print("--------------------------------")

                time.sleep(1)

        return False
        # ========================================================
    # Parcel Arrival
    # ========================================================

    def notify_arrival(self,
                       student_id,
                       pin,
                       floor):

        chat_id = self.get_chat(student_id)

        if chat_id is None:

            return

        message = self.get_message(

            "arrival",

            student_id,

            floor=floor,

            pin=pin

        )

        self.send(

            chat_id,

            message

        )

        # Start Reminder Timer

        self.timers[student_id] = {

            "pin": pin,

            "floor": floor,

            "time": time.monotonic(),

            "warning": False

        }

        print("--------------------------------")
        print("Telegram : Arrival Sent")
        print("Student  :", student_id)
        print("--------------------------------")

    # ========================================================
    # Reminder
    # ========================================================

    def notify_warning(self,
                       student_id):

        chat_id = self.get_chat(student_id)

        if chat_id is None:

            return

        message = self.get_message(

            "warning",

            student_id

        )

        self.send(

            chat_id,

            message

        )

        print("--------------------------------")
        print("Telegram : Reminder Sent")
        print("--------------------------------")

    # ========================================================
    # Parcel Shift
    # ========================================================

    def notify_shift(self,
                     student_id,
                     floor):

        chat_id = self.get_chat(student_id)

        if chat_id is None:

            return

        # Update timer floor

        if student_id in self.timers:

            self.timers[student_id]["floor"] = floor

        message = (

            "📦 Parcel Updated\n\n"

            "Your parcel has been moved.\n\n"

            "New Floor : {}\n\n"

            "Your pickup PIN remains the same."

        ).format(

            floor

        )

        self.send(

            chat_id,

            message

        )

        print("--------------------------------")
        print("Telegram : Shift Sent")
        print("--------------------------------")

    # ========================================================
    # Parcel Collected
    # ========================================================

    def notify_collected(self,
                         student_id):

        chat_id = self.get_chat(student_id)

        if chat_id is None:

            return

        message = self.get_message(

            "collected",

            student_id

        )

        self.send(

            chat_id,

            message

        )

        # Remove Timer

        self.timers.pop(

            student_id,

            None

        )

        print("--------------------------------")
        print("Telegram : Collected")
        print("--------------------------------")

    # ========================================================
    # Storage Full
    # ========================================================

    def notify_storage_full(self):

        self.send(

            MANAGER["chat_id"],

            MANAGER_MESSAGES["storage_full"]

        )

        print("--------------------------------")
        print("Telegram : Storage Full")
        print("--------------------------------")

    # ========================================================
    # Security Alert
    # ========================================================

    def notify_security(self):

        self.send(

            MANAGER["chat_id"],

            MANAGER_MESSAGES["security_alert"]

        )

        print("--------------------------------")
        print("Telegram : Security Alert")
        print("--------------------------------")

    # ========================================================
    # Parcel Stored (Manager)
    # ========================================================

    def notify_parcel_stored(self,
                             student_id,
                             floor):

        student = self.get_student(student_id)

        if student is None:

            return

        message = MANAGER_MESSAGES[

            "parcel_stored"

        ].format(

            name=student["name"],

            student_id=student_id,

            floor=floor

        )

        self.send(

            MANAGER["chat_id"],

            message

        )

        print("--------------------------------")
        print("Telegram : Manager Updated")
        print("--------------------------------")

    # ========================================================
    # Update Parcel Floor
    # ========================================================

    def update_floor(self,
                     student_id,
                     floor):

        if student_id in self.timers:

            self.timers[student_id]["floor"] = floor
         # ========================================================
    # Update Parcel Floor
    # ========================================================

    def update_floor(self,
                     student_id,
                     floor):

        if student_id in self.timers:

            self.timers[student_id]["floor"] = floor

    # ========================================================
    # Check Timers
    # ========================================================

    def check_timers(self):

        current = time.monotonic()

        for student_id in list(self.timers.keys()):

            timer = self.timers[student_id]

            if timer["warning"]:

                continue

            elapsed = current - timer["time"]

            if elapsed >= WARNING_TIME:

                timer["warning"] = True

                self.notify_warning(

                    student_id

                )

    # ========================================================
    # /start
    # ========================================================

    def handle_start(self,
                     chat_id,
                     student_id):

        self.send(

            chat_id,

            self.get_message(

                "welcome",

                student_id

            )

        )

    # ========================================================
    # /status
    # ========================================================

    def handle_status(self,
                      chat_id,
                      student_id):

        timer = self.timers.get(student_id)

        if timer is None:

            self.send(

                chat_id,

                self.get_message(

                    "status_none",

                    student_id

                )

            )

            return

        self.send(

            chat_id,

            self.get_message(

                "status_storage",

                student_id,

                floor=timer["floor"]

            )

        )

    # ========================================================
    # /language
    # ========================================================

    def handle_language(self,
                        chat_id,
                        student_id):

        self.awaiting_language[chat_id] = student_id

        self.send(

            chat_id,

            self.get_message(

                "language_menu",

                student_id

            )

        )
            # ========================================================
    # Language Selection
    # ========================================================

    def handle_language_selection(self,
                                  chat_id,
                                  student_id,
                                  text):

        value = text.strip().lower()

        language_map = {

            "1": "en",
            "en": "en",
            "english": "en",

            "2": "ar",
            "ar": "ar",
            "arabic": "ar",

            "3": "hi",
            "hi": "hi",
            "hindi": "hi",

            "4": "zh",
            "zh": "zh",
            "chinese": "zh",

            "5": "ms",
            "ms": "ms",
            "malay": "ms",
            "bahasa": "ms"

        }

        if value not in language_map:

            self.send(

                chat_id,

                "Invalid language."

            )

            return

        language = language_map[value]

        self.languages[student_id] = language

        STUDENTS[student_id]["language"] = language

        self.awaiting_language.pop(

            chat_id,

            None

        )

        self.send(

            chat_id,

            self.get_message(

                "language_changed",

                student_id

            )

        )

    # ========================================================
    # Unknown Command
    # ========================================================

    def unknown_command(self,
                        chat_id):

        self.send(

            chat_id,

            "Unknown command.\nUse /start, /status or /language."

        )

    # ========================================================
    # Telegram Polling
    # ========================================================

    def poll(self):

        if self.requests is None:

            return

        current = time.monotonic()

        if (current - self.last_poll) < self.poll_interval:

            return

        self.last_poll = current

        try:

            response = self.requests.get(

                self.base_url +

                "/getUpdates?offset={}".format(

                    self.offset

                )

            )

            data = response.json()

            response.close()

        except Exception as error:

            print("--------------------------------")
            print("Telegram Poll Error")
            print(error)
            print("--------------------------------")

            return

        if not data.get("ok"):

            return

        updates = data.get(

            "result",

            []

        )

        for update in updates:

            self.offset = update["update_id"] + 1

            if "message" not in update:

                continue

            message = update["message"]

            chat_id = str(

                message["chat"]["id"]

            )

            text = message.get(

                "text",

                ""

            ).strip()

            student_id, student = self.get_student_by_chat(

                chat_id

            )

            if student_id is None:

                self.send(

                    chat_id,

                    "❌ You are not registered."

                )

                continue

            # ------------------------------------
            # Waiting for language selection
            # ------------------------------------

            if chat_id in self.awaiting_language:

                self.handle_language_selection(

                    chat_id,

                    student_id,

                    text

                )

                continue

            command = text.lower()

            # ------------------------------------
            # Commands
            # ------------------------------------

            if command == "/start":

                self.handle_start(

                    chat_id,

                    student_id

                )

            elif command == "/status":

                self.handle_status(

                    chat_id,

                    student_id

                )

            elif command == "/language":

                self.handle_language(

                    chat_id,

                    student_id

                )

            else:

                self.unknown_command(

                    chat_id

                )