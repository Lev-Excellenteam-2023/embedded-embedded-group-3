import cv2
import threading
import numpy as np
import logging
from typing import Union


class Camera:
    def __init__(self, camera_id: int = 0) -> None:
        """
        @summary:
            initialize the camera object with the given camera id. 0 for PC camera, 1 for USB camera
        @param camera_id:
            the id of the camera to use:
            id=0: for PC camera
            id=1: for USB camera
        @ivar camera_id: int
            the id of the camera to use: 0 for PC camera, 1 for USB camera
        @ivar cap: cv2.VideoCapture
            the video capture object
        @ivar is_streaming: bool
            a flag to indicate if the camera is streaming or not
        """
        self.camera_id = camera_id
        self.cap = None
        self.is_streaming = False

    def streamOn(self) -> None:
        """
        @summary:
            start streaming from the camera
        """
        if self.cap is None:
            self.cap = cv2.VideoCapture(self.camera_id)

            if not self.cap.isOpened():
                logging.error(f"Camera with ID {self.camera_id} not found or is being used by another application!")
                self.cap = None
                return
            else:
                logging.info("Camera successfully initialized!")
                self.is_streaming = True
        else:
            logging.info("Camera is already streaming!")

    def showLive(self) -> None:
        """
        @summary:
            display the live feed from the camera
        """
        if not self.is_streaming:
            logging.error("Camera is not streaming!")
            return

        def display_feed():
            """
            @summary:
                a thread to display the live feed from the camera
            """
            while self.is_streaming:
                is_frame_available, frame = self.cap.read()
                if not is_frame_available:
                    logging.error("Error: Can't receive frame!")
                    break
                cv2.imshow('Live Camera Feed', frame)
                if cv2.waitKey(1) == ord('q'):
                    break

            cv2.destroyAllWindows()

        threading.Thread(target=display_feed).start()

    def getCurrentFrame(self) -> Union[np.ndarray, None]:
        """
        @summary: int
            get the current frame from the camera
        @return: np.ndarray
            the current frame from the camera
        """
        if not self.is_streaming:
            logging.error("Camera is not streaming!")
            return None

        is_frame_available, frame = self.cap.read()
        if not is_frame_available:
            logging.error("Error: Can't receive frame!")
            return None

        return frame
    
