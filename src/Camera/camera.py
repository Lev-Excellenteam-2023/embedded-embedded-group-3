import cv2
import threading
import time
import numpy as np


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

            # Check if the camera opened successfully
            if not self.cap.isOpened():
                print(f"Error: Camera with ID {self.camera_id} not found or is being used by another application!")
                self.cap = None
                return
            else:
                print("Camera successfully initialized!")
                self.is_streaming = True
        else:
            print("Camera is already streaming!")

    def showLive(self) -> None:
        """
        @summary:
            display the live feed from the camera
        """
        if not self.is_streaming:
            print("Error: Camera is not streaming!")
            return

        def display_feed():
            """
            @summary:
                a thread to display the live feed from the camera
            """
            while self.is_streaming:
                is_frame_available, frame = self.cap.read()
                if not is_frame_available:
                    print("Error: Can't receive frame!")
                    break
                cv2.imshow('Live Camera Feed', frame)
                if cv2.waitKey(1) == ord('q'):
                    break

            cv2.destroyAllWindows()

        threading.Thread(target=display_feed).start()

    def SaveCurrentFrame(self, path: str) -> None:
        """
        @summary:
            save the current frame to the given path.
            the name of the file will be frame_<current_time>.jpg
        """
        if not self.is_streaming:
            print("Error: Camera is not streaming!")
            return

        ret, frame = self.cap.read()
        if not ret:
            print("Error: Can't receive frame!")
            return

        name = path + f'frame_{time.time()}.jpg'
        cv2.imwrite(name, frame)

    def getCurrentFrame(self) -> np.ndarray:
        """
        @summary: int
            get the current frame from the camera
        @return: np.ndarray
            the current frame from the camera
        """
        if not self.is_streaming:
            print("Error: Camera is not streaming!")
            return np.array([])  # Return an empty numpy array for consistency

        is_frame_available, frame = self.cap.read()
        if not is_frame_available:
            print("Error: Can't receive frame!")
            return np.array([])  # Return an empty numpy array for consistency

        return frame

    def showFrame(self, frame: np.ndarray) -> None:
        cv2.imshow('Displayed Frame', frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
