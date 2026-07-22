# 📦 Automated Parcel Storage and Collection System

An embedded systems project developed using **Raspberry Pi Pico** and **Raspberry Pi Pico W** to automate parcel delivery, storage, and collection through secure PIN authentication and IoT-based Telegram notifications.

---

## 🎥 Project Demonstration

📺 Watch the full demonstration here:

**https://youtu.be/YOUR_VIDEO_LINK**

---

# 📖 System Overview

The Automated Parcel Storage and Collection System is designed to automate the parcel management process within a university environment.

The system consists of two independent subsystems:

- **Delivery Section (Pico 1)**
  - Validates student IDs
  - Controls the delivery gate
  - Detects parcel placement using a Laser-LDR sensor
  - Operates the conveyor
  - Sends parcel information to Pico 2 via UART

- **Storage & Collection Section (Pico 2 W)**
  - Receives parcel information
  - Assigns storage locations
  - Generates random collection PINs
  - Controls storage gates
  - Handles parcel collection
  - Sends Telegram notifications
  - Activates the security alarm after three incorrect PIN attempts

Communication between both controllers is achieved using:

- One-way UART
- GPIO storage status signal

---

# 🎯 Project Objectives

- Automate the parcel delivery process.
- Provide secure parcel collection using randomly generated PINs.
- Detect parcels automatically using a Laser-LDR sensor.
- Transfer parcel information between two Raspberry Pi Pico boards using UART.
- Provide real-time Telegram notifications.
- Improve parcel management efficiency and security.

---

# ⚙️ System Features

✅ Student ID verification

✅ Automatic delivery gate

✅ Laser-LDR parcel detection

✅ Conveyor automation

✅ Multi-floor storage

✅ Automatic parcel shifting

✅ Secure 4-digit PIN authentication

✅ Telegram notifications

✅ Security alarm

✅ Multi-language Telegram interface

---

# 🛠 Hardware Components

| Component | Quantity |
|-----------|---------:|
| Raspberry Pi Pico | 1 |
| Raspberry Pi Pico W | 1 |
| Matrix Keypad (4×4) | 2 |
| I2C LCD Display | 2 |
| Continuous Rotation Servo | 4 |
| 28BYJ-48 Stepper Motor | 1 |
| ULN2003 Driver | 1 |
| Laser Module | 1 |
| LDR Sensor | 1 |
| Passive Buzzer | 1 |
| LEDs | 2 |
| Push Buttons | As Required |
| Power Supply | 5V |

---

# 🏗 System Architecture

![System Architecture](images/system_architecture.png)

---

# 🔄 System Flowcharts

## Pico 1 – Delivery Process

![Pico1 Flowchart](images/pico1_flowchart.png)

---

## Pico 2 – Storage & Collection Process

![Pico2 Flowchart](images/pico2_flowchart.png)

---

# 🔌 Circuit Schematic

![Schematic](images/schematic.png)

---

# 📸 Prototype

## Overall System

![Prototype](images/prototype.jpg)

---

# 📲 Telegram Bot

The Telegram Bot provides:

- Parcel arrival notification
- Parcel collection confirmation
- Collection reminder
- Security alerts
- Manager notifications
- Multi-language support

---

# 🔄 System Workflow

1. Delivery personnel enters Student ID.
2. System validates Student ID.
3. Delivery gate opens.
4. Parcel interrupts Laser beam.
5. Conveyor transports parcel.
6. Pico 1 sends Student ID to Pico 2 via UART.
7. Pico 2 assigns storage location.
8. Telegram notification is sent.
9. Student enters collection PIN.
10. Parcel door opens.
11. Remaining parcels shift automatically.
12. Telegram confirms successful collection.

---

# 📂 Software Structure

## Pico 1

```
code.py
config.py
delivery.py
gate.py
laser.py
conveyor.py
lcd.py
matrix_keypad.py
uart.py
```

## Pico 2

```
code.py
config.py
locker.py
pickup.py
servo.py
telegram.py
uart.py
wifi_connect.py
buzzer.py
lcd.py
matrix_keypad.py
```

---

# 💡 Technologies Used

- CircuitPython
- Raspberry Pi Pico
- Raspberry Pi Pico W
- UART Communication
- GPIO Signaling
- Telegram Bot API
- Embedded Systems
- IoT

---

# 🚀 Future Improvements

- RFID authentication
- Fingerprint authentication
- Face recognition
- Mobile application
- Cloud database
- Camera integration
- Weight sensors
- Larger storage capacity

---

# 👨‍💻 Authors

Developed as an Embedded Systems Mini Project.

University Malaysia Perlis (UniMAP)

---

# 📜 License

This project is intended for educational purposes.
