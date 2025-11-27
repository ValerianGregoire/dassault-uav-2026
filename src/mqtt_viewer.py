import paho.mqtt.client as mqtt
import json

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        print(f"[{msg.topic}]")
        print(json.dumps(payload, indent=2))
    except json.JSONDecodeError:
        print(f"[{msg.topic}] {msg.payload.decode()}")

# Créer le client MQTT (API version 1 pour compatibilité)
client = mqtt.Client(client_id="MQTT_Viewer")

client.on_message = on_message

# Connexion au broker
broker_address = "localhost"
client.connect(broker_address, 1883)

# Subscribe to a topic
client.subscribe("#") # '#' to subscribe to all topics

print("En attente des messages MQTT... (CTRL+C pour quitter)")
client.loop_forever()
