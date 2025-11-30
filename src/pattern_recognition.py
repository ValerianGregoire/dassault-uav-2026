# This code requires to run pip install numpy==1.26.4

import numpy as np
import cv2
from cv2 import aruco
from mqtt_node import MqttNode
cap = cv2.VideoCapture(0)

class PatternRecognition(MqttNode):

    def __init__(self):
        super().__init__(name="pattern_recognition", subscribe_topic=["_image","ATTITUDE"])

        # Camera calibration matrices
        self.MTX = [[589.15111735, 0., 327.91896476],
                    [0., 596.54490138, 277.76024624],
                    [0., 0., 1.]]

        self.DIST = [[0.01007562, -0.01642674, -0.00228647, -0.00139072, 0.07697145]]

        self.total_error = 0.026350403678532683

        # ARUCO parameters
        self.aruco_side = 0.1 # Marker side length in meters
        self.aruco_coordinates = {}
        self.aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_100)

        # Do not touch
        self.aruco_points_3d = [[-self.aruco_side/2, self.aruco_side/2, 0], # Top-left
                                [ self.aruco_side/2, self.aruco_side/2, 0], # Top-right
                                [ self.aruco_side/2,-self.aruco_side/2, 0], # Bottom-right
                                [-self.aruco_side/2,-self.aruco_side/2, 0]] # Bottom-left
        self.aruco_detector = aruco.ArucoDetector(self.aruco_dict, aruco.DetectorParameters())

    def on_message(self, client, userdata, message):
        # When an image is received over MQTT

        # Decode the image
        nparr = np.frombuffer(message.payload, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Equalize histogram on rgb channels
        for i in range(3):
            frame[:,:,i] = cv2.equalizeHist(frame[:,:,i])

        # Find ARUCO markers
        corners, ids, _ = self.aruco_detector.detectMarkers(frame)

        # Update frame with detected markers
        frame = aruco.drawDetectedMarkers(frame, corners)

        # Use solvePnP to estimate the pose of each marker
        if ids is not None:
            for i in range(len(ids)):
                retval, rvec, tvec = cv2.solvePnP( 
                    np.array(self.aruco_points_3d, dtype=np.float32),
                    np.array(corners[i][0], dtype=np.float32),
                    np.array(self.MTX, dtype=np.float32),
                    np.array(self.DIST, dtype=np.float32))

                # Draw the axis for each marker
                frame = cv2.drawFrameAxes(frame, np.array(self.MTX, dtype=np.float32), np.array(self.DIST, dtype=np.float32), rvec, tvec, 0.05)

                # Draw the 3D coordinates on the marker
                corner = corners[i][0]
                cv2.putText(frame, f"X: {tvec[0][0]:.2f} m", (int(corner[0][0]), int(corner[0][1]-30)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)
                cv2.putText(frame, f"Y: {tvec[1][0]:.2f} m", (int(corner[0][0]), int(corner[0][1]-15)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)
                cv2.putText(frame, f"Z: {tvec[2][0]:.2f} m", (int(corner[0][0]), int(corner[0][1])), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 2)

            # Compute the camera position using an average of all detected markers
            rvec_matrix = cv2.Rodrigues(rvec)[0]
            rvec_matrix = np.matrix(rvec_matrix).T

            for id in self.aruco_coordinates:
                aruco_coord = self.aruco_coordinates[id]
                camera_position = -rvec_matrix * np.matrix(tvec)
                camera_position += np.matrix(aruco_coord)
                print("Camera position from marker %d: X: %f m, Y: %f m, Z: %f m" % (id, camera_position[0][0], camera_position[1][0], camera_position[2][0]))

    while True:
        _, frame = cap.read()

        # Display the FPS on the frame
        fps = cap.get(cv2.CAP_PROP_FPS)
        cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("Frame", frame)
        if cv2.waitKey (1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
