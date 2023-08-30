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

    def predict_image(self, image: np.ndarray) -> bool:
        """
        Predict whether an image contains fire.

        Args:
            image (np.ndarray): The image to predict.

        Returns:
            bool: True if fire is detected, False otherwise.
        """
        desired_shape = (IMAGE_SIZE, IMAGE_SIZE)
        resized_image = FireDetector.__resize_and_pad_image(image, desired_shape)
        preprocessed_image = resized_image.astype('float32') / 255.0
        preprocessed_image = np.expand_dims(preprocessed_image, axis=0)
        predictions = self.__model.predict(preprocessed_image, verbose=0)
        return predictions[0][0] <= 0.5
