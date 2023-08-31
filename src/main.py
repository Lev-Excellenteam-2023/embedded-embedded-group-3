import numpy
from Camera.camera import Camera
from fire_detector.fire_detector import FireDetector
from notification_manager.email_notifier import EmailNotifier
from consts import MODEL_PATH, RECEIVER_EMAIL, EXTERNAL_CAM, WEBCAM


def main():
    camera: Camera = Camera(EXTERNAL_CAM)
    camera.streamOn()
    fire_detector: FireDetector = FireDetector(MODEL_PATH)
    email_notifier: EmailNotifier = EmailNotifier()
    email_notifier.add_recipient_email(RECEIVER_EMAIL)
    while True:
        captured_frame: numpy.ndarray = camera.getCurrentFrame()
        if captured_frame is None:
            continue
        if fire_detector.predict_image(captured_frame):
            email_notifier.send_notification(captured_frame, camera.get_location())


if __name__ == "__main__":
    main()
