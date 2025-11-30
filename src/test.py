from mqtt_node import MqttNode
from time import sleep

class Test(MqttNode):

    def __init__(self):
        super().__init__(name="Test", subscribe_topic=[])

    def run(self):
        i = 0
        while True:
            self.client.publish("test_topic", f"Test message {i}")
            i += 1
            i %= 5000
            sleep(1)

if __name__ == "__main__":
    test = Test()
    test.run()