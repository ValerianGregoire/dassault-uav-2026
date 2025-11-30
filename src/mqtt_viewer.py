import paho.mqtt.client as mqtt
import json

if __name__ == "__main__":
    def on_message(client, userdata, msg):
        try:
            payload = json.loads(msg.payload.decode())
            print(f"[{msg.topic}]")
            print(json.dumps(payload, indent=2))
        except json.JSONDecodeError:
            print(f"[{msg.topic}] {msg.payload.decode()}")

    # MQTT client creation
    client = mqtt.Client(client_id="MQTT_Viewer")
    client.on_message = on_message

    # Connection to MQTT broker
    client.connect("localhost", 1883)

    # Subscribe to a topic
    client.subscribe("#") # '#' to subscribe to all topics

    print("Waiting for MQTT messages... (CTRL+C to quit)")
    client.loop_forever()
