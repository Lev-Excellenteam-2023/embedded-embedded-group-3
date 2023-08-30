import tensorflow as tf
import cv2
import numpy as np
from typing import Tuple
from src.consts import IMAGE_SIZE


class FireDetector:
    def __init__(self, model_path: str):
        """
        Initialize a FireDetector instance with a pre-trained model.
        Args:
            model_path (str): The path to the pre-trained model.
        """
        self.__model = tf.keras.models.load_model(model_path)

    @staticmethod
    def __resize_and_pad_image(image: np.ndarray, output_size: Tuple[int, int]) -> np.ndarray:
        """
        Resize an image to the specified size while maintaining its original aspect ratio.
        If necessary, pad the image to achieve the exact size.
        Args:
            image (np.ndarray): The image to resize.
            output_size (tuple): A tuple (width, height) specifying the desired output size (e.g., (128, 128)).
        Returns:
            np.ndarray: The resized and padded image as a NumPy array.
        """
        original_height, original_width, _ = image.shape
        target_width, target_height = output_size
        aspect_ratio = original_width / original_height

        if aspect_ratio > 1:
            new_width = target_width
            new_height = int(target_width / aspect_ratio)
        else:
            new_height = target_height
            new_width = int(target_height * aspect_ratio)

        resized_img = cv2.resize(image, (new_width, new_height))
        padded_img = np.zeros((target_height, target_width, 3), dtype=np.uint8)

        left = (target_width - new_width) // 2
        upper = (target_height - new_height) // 2
        right = left + new_width
        lower = upper + new_height
        padded_img[upper:lower, left:right] = resized_img
        return padded_img

    @staticmethod
    def __filter_by_color(image: np.ndarray) -> bool:
        """
        Detect fire or smoke in an image based on color filtering.

        Args:
            image (np.ndarray): The image to analyze.

        Returns:
            bool: True if fire or smoke is detected, False otherwise.
        """
        frame_smooth = cv2.GaussianBlur(image, (7, 7), 0)
        hsv_image = cv2.cvtColor(frame_smooth, cv2.COLOR_BGR2HSV)

        lower_fire = np.array([0, 74, 200])
        upper_fire = np.array([22, 170, 235])

        lower_smoke = np.array([95, 11, 150])
        upper_smoke = np.array([105, 45, 190])

        mask_fire = cv2.inRange(hsv_image, lower_fire, upper_fire)
        mask_smoke = cv2.inRange(hsv_image, lower_smoke, upper_smoke)
        mask_fire = cv2.add(mask_smoke, mask_fire)

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        dilate = cv2.dilate(mask_fire, kernel, iterations=2)
        contours_fire, _ = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for cont in contours_fire:
            x, y, w, h = cv2.boundingRect(cont)
            if w > 10 and h > 5 and cv2.contourArea(cont) > 60:
                return True
        return False

    def predict_image(self, image: np.ndarray) -> bool:
        """
        Predict whether an image contains fire or smoke.
        Args:
            image (np.ndarray): The image to predict.
        Returns:
            bool: True if fire or smoke is detected, False otherwise.
        """
        desired_shape = (IMAGE_SIZE, IMAGE_SIZE)
        resized_image = FireDetector.__resize_and_pad_image(image, desired_shape)
        if not FireDetector.__filter_by_color(resized_image):
            return False
        preprocessed_image = resized_image.astype('float32') / 255.0
        preprocessed_image = np.expand_dims(preprocessed_image, axis=0)
        predictions = self.__model.predict(preprocessed_image, verbose=0)
        return predictions[0][0] <= 0.5
