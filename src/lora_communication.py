import serial
import json
import time
import numpy as np
from mqtt_node import MqttNode

class LoraCommunication(MqttNode):

    def __init__(self):
        self.type = "quadcopter" # Can be "quadcopter" or "plane"
        if self.type == "plane":
            self.topics = ["GPS_P", "ARUCO", "END"]
        else:
            self.topics = ["GPS_Q", "DETACH"]
        
        # Initialize MQTT node
        super().__init__(name="lora_communication", subscribe_topic=self.topics)
        
        self.commands = {
            "DETACH":0,
            "GPS_P":[0, 0, 0], # Plane GPS coordinates
            "GPS_Q":[0, 0, 0], # Quadcopter GPS coordinates
            "ARUCO":[], # Aruco marker coordinates (id, lat, lon) (up to 4 markers)
            "END":0
            }

        # UART connection to LoRa module
        self.uart = serial.Serial("/dev/ttyS1", baudrate=9600, timeout=1)
        time.sleep(2)  # Wait for the serial connection to initialize
        
    def on_message(self, client, userdata, message):
        # Get topic and payload
        topic = message.topic
        payload = message.payload.decode()
        
        # Update command values
        if topic in self.commands:
            self.commands[topic] = np.squeeze(json.loads(payload)).tolist()
            print(f"[MQTT] Received command - {topic}: {self.commands[topic]}")

    def publish_commands(self):
        # Publish command data
        for command, value in self.commands.items():
            self.client.publish(command, json.dumps(value))
            print("[MQTT] Published command - {}: {}".format(command, value))

    def send_lora(self):
        # Send all commands via uart
        for command, value in self.commands.items():
            message_body = str(value).replace(' ','')
            message = command + ' ' + message_body + '\n'
            self.uart.write(message.encode())
            print(f"[UART] Command sent: {message.strip()}")

    def receive_lora(self):
        while self.uart.in_waiting > 0:
            data = self.uart.readline().decode().strip()
            print(f"[UART] Data received: {data}")
            
            # Treat data
            received_data = data.split(' ')
            output_head = received_data[0]
            output_body = np.squeeze([json.loads(x) for x in received_data[1:]]).tolist()
            print(f"Data extracted : {output_head} {output_body}\n")
            
            # Add data to commands
            if self.type == "quadcopter" and output_head in ["GPS_Q", "DETACH"]:
                pass
            elif self.type == "plane" and output_head in ["GPS_P", "ARUCO", "END"]:
                pass
            else:
                self.commands[output_head] = output_body.copy()


if __name__ == "__main__":
    lora_communication = LoraCommunication()
    
    # Start MQTT node
    lora_communication.start()
    
    # Loop to send and receive data via LoRa
    while True:
        lora_communication.send_lora()
        lora_communication.receive_lora()





    
        
