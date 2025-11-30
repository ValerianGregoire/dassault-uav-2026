# Dassault UAV Challenge 2025–2026  
Automation Project – README

---

## Installation

### Python Version  
This project was developed and tested using **Python 3.11**.  
Using another version may lead to unexpected behavior.


### Required Python Libraries  
Install all dependencies with:

```bash
pip install numpy==1.26.4 matplotlib pillow opencv-python opencv-contrib-python==4.7.0.72 ultralytics tensorflow paho-mqtt pyserial pymavlink
```

### MQTT broker
Download Mosquitto here: [Mosquitto Official Website](https://mosquitto.org/download/)

Add the broker folder to the Path environment variable. It is located at C:\ProgramFiles\mosquitto by default.

--

## Execution
### Mosquitto broker launch
In a terminal, run :
mosquitto -v

The broker will start on port 1883 in verbose mode.

### Python launch
In multiple terminals, run each python script one by one.
A script to start all processes at once will be available in future versions of the project. 

--

## Scripts summary
### PX4-Bridge
The px4_bridge.py script manages serial communications via MAVLINK between the flight management unit (FMU) and the companion computer.

When a MAVLINK message is received from the FMU, its data is published in a MQTT topic of the same name (e.g., an ATTITUDE message will be published in the ATTITUDE topic). All data are published as dicts to simplify their use.

On the other hand, when attitude control commands or GPS calculated coordinates are published in MQTT topics such as _geo_loc or _att_cmd, their data are converted and sent via MAVLINK to the FMU for off-board control.

### Pilot
The pilot.py script manages attitude control of the drone for aerobatics in off-board mode. This  