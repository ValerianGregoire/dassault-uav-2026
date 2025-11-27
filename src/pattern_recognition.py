# This code requires to run pip install numpy==1.26.4

import numpy as np
import cv2
from cv2 import aruco
from mqtt_node import MqttNode
cap = cv2.VideoCapture(0)

class PatternRecognition(MqttNode):

    def __init__(self):
        super().__init__(name="_image", subscribe_topic=[])

        # Camera calibration matrices
        self.MTX = [ [589.15111735, 0., 327.91896476],
                [0., 596.54490138, 277.76024624],
                [0., 0., 1.] ]

        self.DIST = [[0.01007562, -0.01642674, -0.00228647, -0.00139072, 0.07697145]]

        self.total_error = 0.026350403678532683

        # ARUCO dimensions
        self.aruco_side = 0.1 # Marker side length in meters
        self.aruco_points_3d = [[-self.aruco_side/2, self.aruco_side/2, 0], # Top-left
                                [ self.aruco_side/2, self.aruco_side/2, 0], # Top-right
                                [ self.aruco_side/2,-self.aruco_side/2, 0], # Bottom-right
                                [-self.aruco_side/2,-self.aruco_side/2, 0]] # Bottom-left

        # ARUCO parameters
        aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_100)
        parameters = aruco.DetectorParameters()
        aruco_detector = aruco.ArucoDetector(aruco_dict, parameters)
        aruco_coordinates = np.array([5, 2, 3]).reshape((3, 1)) # Real world coordinates of the ARUCO markers

    while True:
        _, frame = cap.read()
        
        #lists of ids and the corners belonging to each id
        corners, ids, _ = aruco_detector.detectMarkers(frame)

        frame = aruco.drawDetectedMarkers(frame, corners)
        
        # Use solvePnP to estimate the pose of each marker
        if ids is not None:
            for i in range(len(ids)):
                retval, rvec, tvec = cv2.solvePnP( 
                    np.array(aruco_points_3d, dtype=np.float32),
                    np.array(corners[i][0], dtype=np.float32),
                    np.array(MTX, dtype=np.float32),
                    np.array(DIST, dtype=np.float32)
                )
                # Draw the axis for each marker
                frame = cv2.drawFrameAxes(frame, np.array(MTX, dtype=np.float32), np.array(DIST, dtype=np.float32), rvec, tvec, 0.05)
                
                # Draw the 3D coordinates on the marker
                corner = corners[i][0]
                cv2.putText(frame, f"X: {tvec[0][0]:.2f} m", (int(corner[0][0]), int(corner[0][1]-30)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)
                cv2.putText(frame, f"Y: {tvec[1][0]:.2f} m", (int(corner[0][0]), int(corner[0][1]-15)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)
                cv2.putText(frame, f"Z: {tvec[2][0]:.2f} m", (int(corner[0][0]), int(corner[0][1])), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 2)
                
            # Compute the camera position from ARUCO coordinates
            rvec_matrix = cv2.Rodrigues(rvec)[0]
            rvec_matrix = np.matrix(rvec_matrix).T
            camera_position = -rvec_matrix * np.matrix(tvec)
            camera_position += np.matrix(aruco_coordinates)
            print("Camera position: X: %f m, Y: %f m, Z: %f m" % (camera_position[0][0], camera_position[1][0], camera_position[2][0]))
        
        # Display the FPS on the frame
        fps = cap.get(cv2.CAP_PROP_FPS)
        cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        cv2.imshow("Frame", frame)
        if cv2.waitKey (1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()