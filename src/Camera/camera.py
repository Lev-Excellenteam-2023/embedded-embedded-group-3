import cv2
import threading
import numpy as np
import logging
from typing import Union
import time


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
        self.last_frame = np.zeros((480, 640, 3), np.uint8)

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

    def mse(self, new_frame: np.ndarray) -> float:
        """
        @summary:
            Compute the mean squared error between the provided image and the last frame.
        @param new_frame: np.ndarray
            The image to compare with the last frame.
        @return: float
            The mean squared error between the two images.
        """
        last_frame = self.last_frame
        mean_squared_error = np.sum((new_frame.astype("float") - last_frame.astype("float")) ** 2)
        mean_squared_error /= float(new_frame.size)  # Using size to count all elements in the array
        return float(mean_squared_error)  # Ensure the result is a float

    def isSimilarToLastFrame(self, frame: np.ndarray) -> bool:
        """
        @summary:
            check if the given frame is similar to the last frame.
            An image is similar to another image if there is no lot of difference between them.
        @param frame: np.ndarray
            the frame to check.
        @return: bool
            True if the given frame is similar to the last frame, False otherwise.
        """
        if not self.is_streaming:
            logging.error("Camera is not streaming!")
            return False

        # Compute the mean squared error between the given frame and the last frame
        error = self.mse(frame)  # Update this line

        # Update the last frame
        # self.last_frame = frame

        # Consider two frames to be similar if the error is below a threshold
        threshold = 1200
        return error < threshold

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

        if self.isSimilarToLastFrame(frame):
            return None
        self.last_frame = frame
        return frame

    def get_location(self) -> tuple:
        """
        @summary:
            get the location of the camera
        @return: tuple
            the location of the camera
        """
        return (31.770772026697788, 35.182087722966905)


# # main:
# counter = 0
# if __name__ == "__main__":
#     camera = Camera(1)
#     camera.streamOn()
#     while True:
#         time.sleep(0.1)
#         frame = camera.getCurrentFrame()
#         if frame is not None:
#             print("Different" + str(counter))
#             counter += 1
#             cv2.imshow("Frame", frame)
#             if cv2.waitKey(1) == ord('q'):
#                 break
