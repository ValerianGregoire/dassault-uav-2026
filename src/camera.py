import cv2
import libcamera
from picamera2 import Picamera2
from mqtt_node import MqttNode
import numpy as np

class Camera(MqttNode):

    def __init__(self):
        super().__init__(name="camera", subscribe_topic=[])
        
        # Configure the camera
        self.picam2 = Picamera2()
        self.picam2.preview_configuration.main.size = (640,480)  #resolution
        self.picam2.preview_configuration.main.format = "RGB888"
        self.picam2.preview_configuration.transform = libcamera.Transform(hflip=1, vflip=1)  #rotate image
        self.picam2.preview_configuration.controls.FrameRate = 30.0  #fps
        self.picam2.preview_configuration.align()
        self.picam2.configure("preview")
        self.picam2.start()

    def capture_frame(self):
        array = self.picam2.capture_array()
        
        # Display the image locally for debugging
        cv2.imshow("Original frame", array.copy())
        
        if cv2.waitKey(1) & 0xFF == ord("q") :
            pass
        
        # Equalize the RGB histogram to improve contrast
        for i in range(3):
            array[:,:,i] = cv2.equalizeHist(array[:,:,i])
        
        # Publish the captured frame as a JPG image over MQTT
        _, buffer = cv2.imencode('.jpg', array)
        jpg_bytes = buffer.tobytes()
        print("Publishing image")
        self.client.publish("_image", jpg_bytes)

if __name__ == "__main__":
    camera = Camera()
    
    while True:
        camera.capture_frame()



