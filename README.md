# Dassault UAV Challenge 2025–2026  
Automation Project – README

---

## 📦 Installation

### ✅ Python Version  
This project was developed and tested using **Python 3.11**.  
Using another version may lead to unexpected behavior.

---

### 📚 Required Python Libraries  
Install all dependencies with:

```bash
pip install numpy matplotlib pillow opencv-python ultralytics tensorflow paho-mqtt pyserial
```

## MQTT broker
Download Mosquitto here: [Mosquitto Official Website](https://mosquitto.org/download/)

Add the broker folder to the Path environment variable. It is located at C:\ProgramFiles\mosquitto by default.

# Running
## Mosquitto broker launch
In a terminal, run :
mosquitto -v

The broker will start on port 1883 in verbose mode.

## Python launch
In multiple terminals, run each python script one by one.