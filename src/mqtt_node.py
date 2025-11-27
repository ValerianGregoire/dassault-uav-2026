import paho.mqtt.client as mqtt

class MqttNode:

    def __init__(self, name, subscribe_topic=list()):
        self.name = name
        self.broker = "localhost"
        self.client = mqtt.Client()
        self.client.connect(self.broker, 1883)
        self.subscribe_topic = subscribe_topic.copy()
        for topic in subscribe_topic:
            self.client.subscribe(topic)
        self.client.on_message = self.on_message
    
    def on_message(self, client, userdata, message):
        print(f"{self.name}: received ->", message.payload.decode())

    def start(self):
        print(f"[MQTT] {self.name}: waiting for messages...")
        self.client.loop_forever()

