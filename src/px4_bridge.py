from pymavlink import mavutil
from mqtt_node import MqttNode

class PX4Bridge(MqttNode):

    def __init__(self):
        super().__init__(name="px4_bridge", subscribe_topic=["att_cmd"])
        # Connexion MAVLink
        self.master = mavutil.mavlink_connection('COM12',baud=115200)  # Remplacez par l'adresse IP et le port appropriés
        self.data = {}
    # def on_message(self, client, userdata, message):
    #     print("Received message")
        
    #     # Publish position
    #     self.client.publish("telemetrie", json.dumps(data))


    def start(self):
        print("[PX4] En attente du heartbeat...")
        self.master.wait_heartbeat()
        print("[PX4] Heartbeat reçu — connexion OK")


        while True:
            msg = self.master.recv_match(blocking=True)
            if not msg:
                continue
            
            mtype = msg.get_type()

            temp_dict = {}
            for field in msg.get_fieldnames():
                temp_dict[field] = msg.__dict__[field]

            self.client.publish(mtype, str(temp_dict))
            with open("telemetrie.log", "w") as logfile:
                logfile.write(str(temp_dict) + "\n")

if __name__ == "__main__":
    # Instantiate objects
    px4_bridge = PX4Bridge()
    
    # Start MQTT node
    px4_bridge.start()
    





    
        
