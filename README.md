<p align="center">
  <img src="Images/Banner.png" alt="Project Banner" width="100%">
</p>

<h1 align="center">
📦 Automated Parcel Storage and Collection System
</h1>

<p align="center">
An IoT-enabled embedded system for automated parcel delivery, storage, and secure collection using dual Raspberry Pi Pico microcontrollers.
</p>

<p align="center">

![Platform](https://img.shields.io/badge/Platform-Raspberry%20Pi%20Pico%20%26%20Pico%20W-C51A4A?style=for-the-badge)
![Language](https://img.shields.io/badge/Language-CircuitPython-3776AB?style=for-the-badge)
![Communication](https://img.shields.io/badge/Communication-UART%20%2B%20GPIO-2E8B57?style=for-the-badge)
![IoT](https://img.shields.io/badge/IoT-Telegram%20Bot-229ED9?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Completed-success?style=for-the-badge)

</p>

---

## 📖 Project Overview

The **Automated Parcel Storage and Collection System** is an embedded systems project developed to automate the complete parcel delivery, storage, and collection process within a university environment. The system combines **embedded control**, **IoT connectivity**, and **secure user authentication** to provide an efficient and reliable alternative to conventional manual parcel management.

The project is built around **two Raspberry Pi Pico microcontrollers** working cooperatively. The first controller manages parcel delivery, while the second controller handles parcel storage, secure collection, and IoT services. Communication between both controllers is achieved through **UART communication** and a dedicated **GPIO storage status signal**, enabling reliable synchronization throughout the system.

In addition to hardware automation, the system integrates a **Telegram Bot** that provides real-time parcel notifications, collection PIN delivery, security alerts, and multilingual user support, making the parcel collection process convenient, secure, and fully automated.

---

#  Core Features

| Feature | Description |
|:--------:|-------------|
| 📦 **Automated Parcel Delivery** | Automatically validates student IDs, opens the delivery gate, and transports parcels to the storage section. |
| 📡 **Laser–LDR Detection** | Detects parcel placement by monitoring the interruption of the laser beam and initiates conveyor movement automatically. |
| 🔄 **Smart Storage Management** | Stores parcels sequentially across the Ground, First, and Second floors while tracking storage availability. |
| 🔐 **Secure PIN Authentication** | Generates a unique 4-digit PIN for each parcel, ensuring that only authorized students can collect their parcels. |
| 🚪 **Automatic Parcel Collection** | Opens the appropriate collection door for 7 seconds after successful PIN verification. |
| 📤 **Automatic Parcel Shifting** | Remaining parcels are automatically shifted downward after collection to maximize storage efficiency. |
| 📲 **Telegram Bot Integration** | Sends parcel arrival notifications, collection confirmations, reminders, and security alerts in real time. |
| 🔗 **Dual Pico Communication** | Raspberry Pi Pico boards communicate through one-way UART and a dedicated GPIO storage status signal. |
| 🚨 **Security Alarm System** | Activates an audible alarm after three consecutive incorrect PIN attempts. |
| 🌐 **Multi-language Support** | Telegram Bot interface supports multiple languages for improved user accessibility. |

---

# 🔧 Hardware Components

The Automated Parcel Storage and Collection System integrates multiple electronic components to automate parcel delivery, storage, collection, and user interaction.

| Component | Quantity | Purpose |
|-----------|:--------:|---------|
| Raspberry Pi Pico | 1 | Controls the parcel delivery subsystem |
| Raspberry Pi Pico W | 1 | Controls parcel storage, collection, and IoT services |
| 4×4 Matrix Keypad | 2 | Student ID and PIN entry |
| Grove RGB LCD Display | 1 | User interface for the delivery subsystem |
| 16×2 I²C LCD Display | 1 | User interface for the storage and collection subsystem |
| Continuous Rotation Servo Motors | 6 | Delivery gate, storage gates, collection doors, and parcel shifting mechanism |
| 28BYJ-48 Stepper Motors | 2 | Conveyor belt and storage shifting mechanism |
| ULN2003 Driver Modules | 2 | Stepper motor drivers |
| Laser Module | 1 | Parcel detection |
| LDR Sensor | 1 | Detects interruption of the laser beam |
| Passive Buzzer | 1 | Security alarm |
| LEDs | 2 | Security status indicators |
| 5 V Power Supply | 1 | Powers the complete system |
