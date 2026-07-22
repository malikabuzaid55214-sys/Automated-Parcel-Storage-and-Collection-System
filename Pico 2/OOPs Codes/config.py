# ============================================================
# SMART PARCEL SYSTEM
# PICO 2 W
# Configuration
# Version 2.0
# ============================================================

import board

# ============================================================
# System States
# ============================================================

IDLE            = 0
WAITING_PARCEL  = 1
STORING         = 2
WAITING_STUDENT = 3
COLLECTING      = 4
LOCKED          = 5
FULL            = 6

# ============================================================
# WiFi
# ============================================================

WIFI_SSID = "GOSTAV "
WIFI_PASSWORD = "LOVE3f3y3l"

WIFI_TIMEOUT = 15

# ============================================================
# Telegram
# ============================================================

BOT_TOKEN = "8859205436:AAGKJqtsiYN6o7PPm-V7B21jXIAqrWxdmD4"

# Retry sending Telegram messages if network fails
TELEGRAM_RETRIES = 3

# ============================================================
# Students Database
# ============================================================

STUDENTS = {

    "123": {

        "name": "AHmed",

        "chat_id": "8758468072",

        "language": "en"

    },

    "456": {

        "name": "Abdalla",

        "chat_id": "8375525508",

        "language": "en"

    },

    "555": {

        "name": "Malik",

        "chat_id": "1842342929",

        "language": "en"

    },

    "789": {

        "name": "Akram",

        "chat_id": "7191614965",

        "language": "en"

    }

}

# ============================================================
# Manager
# ============================================================

MANAGER = {

    "name": "Parcel Manager",

    "chat_id": "5202345821"

}

# ============================================================
# Manager Telegram Messages
# ============================================================

MANAGER_MESSAGES = {

    "parcel_stored":

        "📦 SMART PARCEL SYSTEM\n\n"
        "A parcel has been stored.\n\n"
        "Student : {name}\n"
        "ID      : {student_id}\n"
        "Floor   : {floor}",

    "time_exceeded":

        "⏰ SMART PARCEL SYSTEM\n\n"
        "Parcel was not collected.\n\n"
        "Student : {name}\n"
        "ID      : {student_id}\n"
        "Floor   : {floor}\n"
        "PIN     : {pin}",

    "storage_full":

        "⚠️ SMART PARCEL SYSTEM\n\n"
        "Storage is FULL.\n"
        "Please empty a locker.",

    "security_alert":

        "🚨 SMART PARCEL SYSTEM\n\n"
        "Security Alarm Triggered!\n"
        "Three incorrect PIN attempts detected."

}
# ============================================================
# Student Telegram Messages
# ============================================================

MESSAGES = {

    # --------------------------------------------------------
    # Welcome
    # --------------------------------------------------------

    "welcome": {

        "en":
        "🤖 SMART PARCEL SYSTEM\n\n"
        "Welcome!\n\n"
        "Available commands:\n"
        "/start\n"
        "/status\n"
        "/language",

        "ar":
        "🤖 نظام الطرود الذكي\n\n"
        "مرحباً بك\n\n"
        "الأوامر:\n"
        "/start\n"
        "/status\n"
        "/language",

        "hi":
        "🤖 स्मार्ट पार्सल सिस्टम\n\n"
        "स्वागत है!\n\n"
        "उपलब्ध कमांड:\n"
        "/start\n"
        "/status\n"
        "/language",

        "zh":
        "🤖 智能包裹系统\n\n"
        "欢迎！\n\n"
        "可用命令：\n"
        "/start\n"
        "/status\n"
        "/language",

        "ms":
        "🤖 SMART PARCEL SYSTEM\n\n"
        "Selamat Datang!\n\n"
        "Arahan:\n"
        "/start\n"
        "/status\n"
        "/language"

    },

    # --------------------------------------------------------
    # Parcel Arrival
    # --------------------------------------------------------

    "arrival": {

        "en":
        "📦 Your parcel has arrived!\n\n"
        "Floor : {floor}\n"
        "PIN   : {pin}",

        "ar":
        "📦 وصلت شحنتك!\n\n"
        "الطابق: {floor}\n"
        "الرقم السري: {pin}",

        "hi":
        "📦 आपका पार्सल आ गया है।",

        "zh":
        "📦 您的包裹已到达。\n\n"
        "楼层：{floor}\n"
        "密码：{pin}",

        "ms":
        "📦 Parcel anda telah tiba.\n\n"
        "Tingkat : {floor}\n"
        "PIN : {pin}"

    },

    # --------------------------------------------------------
    # Reminder
    # --------------------------------------------------------

    "warning": {

        "en":
        "⏰ Reminder!\n\n"
        "Please collect your parcel.",

        "ar":
        "⏰ تذكير\n\n"
        "يرجى استلام الطرد.",

        "hi":
        "⏰ कृपया अपना पार्सल ले लें।",

        "zh":
        "⏰ 提醒\n\n"
        "请尽快领取您的包裹。",

        "ms":
        "⏰ Peringatan!\n\n"
        "Sila ambil parcel anda."

    },
    
    # --------------------------------------------------------
    # Parcel Shifted
    # --------------------------------------------------------

    "shift": {

        "en":
        "📦 Parcel Updated\n\n"
        "Your parcel has been moved.\n\n"
        "New Floor : {floor}\n\n"
        "Your pickup PIN remains the same.",

        "ar":
        "📦 تم تحديث الطرد.\n\n"
        "تم نقل الطرد.\n\n"
        "الطابق الجديد : {floor}\n\n"
        "يبقى الرقم السري كما هو.",

        "hi":
        "📦 आपका पार्सल स्थानांतरित कर दिया गया।\n\n"
        "नई मंजिल : {floor}\n\n"
        "आपका PIN वही रहेगा।",

        "zh":
        "📦 包裹已更新。\n\n"
        "您的包裹已移动。\n\n"
        "新楼层：{floor}\n\n"
        "取件密码保持不变。",

        "ms":
        "📦 Parcel anda telah dipindahkan.\n\n"
        "Tingkat Baharu : {floor}\n\n"
        "PIN anda tidak berubah."

    },
    
    # --------------------------------------------------------
    # Collected
    # --------------------------------------------------------

    "collected": {

        "en":
        "✅ Parcel collected successfully.\n\nThank you!",

        "ar":
        "✅ تم استلام الطرد.\n\nشكراً لك.",

        "hi":
        "✅ पार्सल सफलतापूर्वक प्राप्त हुआ।",

        "zh":
        "✅ 包裹领取成功。",

        "ms":
        "✅ Parcel berjaya diambil.\n\nTerima kasih."

    },

    # --------------------------------------------------------
    # Status (No Parcel)
    # --------------------------------------------------------

    "status_none": {

        "en":
        "📭 You have no parcel.",

        "ar":
        "📭 لا يوجد لديك أي طرد.",

        "hi":
        "📭 आपके पास कोई पार्सल नहीं है।",

        "zh":
        "📭 您没有包裹。",

        "ms":
        "📭 Tiada parcel."

    },

    # --------------------------------------------------------
    # Status (Storage)
    # --------------------------------------------------------

    "status_storage": {

        "en":
        "📦 Your parcel is waiting.\n\nFloor : {floor}",

        "ar":
        "📦 الطرد بانتظارك.\n\nالطابق : {floor}",

        "hi":
        "📦 आपका पार्सल {floor} पर है।",

        "zh":
        "📦 您的包裹位于 {floor}。",

        "ms":
        "📦 Parcel anda berada di tingkat {floor}."

    },

    # --------------------------------------------------------
    # Language Menu
    # --------------------------------------------------------

    "language_menu": {

        "en":
        "🌍 Choose your language\n\n"
        "1 - English\n"
        "2 - العربية\n"
        "3 - हिन्दी\n"
        "4 - 中文\n"
        "5 - Bahasa Melayu"

    },

    # --------------------------------------------------------
    # Language Changed
    # --------------------------------------------------------

    "language_changed": {

        "en":
        "✅ Language changed successfully.",

        "ar":
        "✅ تم تغيير اللغة.",

        "hi":
        "✅ भाषा बदल दी गई।",

        "zh":
        "✅ 语言已更改。",

        "ms":
        "✅ Bahasa berjaya ditukar."

    }

}
# ============================================================
# LCD
# ============================================================

LCD_SDA = board.GP0
LCD_SCL = board.GP1

LCD_ADDRESS = 0x27

# ============================================================
# Matrix Keypad
# ============================================================

KEYPAD_ROWS = (

    board.GP10,
    board.GP11,
    board.GP12,
    board.GP13

)

KEYPAD_COLS = (

    board.GP14,
    board.GP15,
    board.GP16,
    board.GP21

)

# ============================================================
# Floor Gates
# ============================================================

THIRD_GATE_PIN = board.GP2
SECOND_GATE_PIN = board.GP3

# ============================================================
# Collection Doors
# ============================================================

GROUND_DOOR_PIN = board.GP6
SECOND_DOOR_PIN = board.GP8
THIRD_DOOR_PIN = board.GP26

# ============================================================
# LEDs
# ============================================================

GREEN_LED_PIN = board.GP18
RED_LED_PIN = board.GP19

# ============================================================
# Passive Buzzer
# ============================================================

BUZZER_PIN = board.GP20
BUZZER_FREQUENCY = 2500

# ============================================================
# UART
# ============================================================

UART_RX = board.GP17

# ============================================================
# Storage Status Output
# ============================================================

STORAGE_STATUS_PIN = board.GP28

# ============================================================
# Servo Settings
# ============================================================

THIRD_GATE_SPEED = 0.30
SECOND_GATE_SPEED = 0.30

GROUND_DOOR_SPEED = 0.30
SECOND_DOOR_SPEED = 0.30
THIRD_DOOR_SPEED = 0.30

SERVO_MOVE_TIME = 0.40

DOOR_OPEN_TIME = 7

# ============================================================
# Security
# ============================================================

ADMIN_PIN = "9999"

MAX_ATTEMPTS = 3

PIN_LENGTH = 4

# ============================================================
# Telegram Reminder Timers
# ============================================================

# Demo values

WARNING_TIME = 60

# ============================================================
# Display
# ============================================================

MESSAGE_DELAY = 2