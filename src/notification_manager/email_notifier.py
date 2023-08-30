import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from re import fullmatch
import numpy
from .notify import Notify
from dotenv import load_dotenv
from os import environ
import logging
import cv2
from src.consts import TEMPLATE_BODY_HEADER, TEMPLATE_BODY_FOOTER, STYLE_TEMPLATE, PNG, EMAIL_SUBJECT


def validate_email(email: str) -> bool:
    """
    helper function to validate an email address input
    :param email: email address to be validated
    :return: bool
    """
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if fullmatch(regex, email):
        return True
    return False


class EmailNotifier(Notify):
    """
        A class for sending fire alert notifications via email.

        Attributes:
            system_email_address (str): The system's email address.
            recipient_list (list): A list of recipient email addresses.
            smtp_connection: The SMTP connection for sending emails.
    """

    def __init__(self):
        load_dotenv()
        self.system_email_address = environ.get("SYSTEM_EMAIL")
        self.recipient_list = list()
        self.smtp_connection = smtplib.SMTP('smtp.gmail.com', 587)
        self.smtp_connection.starttls()
        self.smtp_connection.login(self.system_email_address, environ.get("SYSTEM_EMAIL_PASSWORD"))

    def add_recipient_email(self, receiver_address: str) -> None:
        """
        add a new email address to list of recipients
        :param receiver_address: email address
        :return: None
        """
        if validate_email(receiver_address):
            self.recipient_list.append(receiver_address)

    def send_notification(self, image: numpy.ndarray, coordinates: tuple[float, float]) -> None:
        """
        send a fire alert email to a list of recipients
        :param image: photograph of fire
        :param coordinates: latitude and longitude coordinates of fire location
        :return: None
        """
        # encode the image to be able to attach to email
        _, encoded_image = cv2.imencode(PNG, image)
        image_bytes = encoded_image.tobytes()

        for recipient in self.recipient_list:
            self.__send_email(recipient, image_bytes, coordinates)

    def __send_email(self, receiver_email: str, image_data: bytes, coordinates: tuple[float, float]) -> None:
        """
        send a rendered fire alert notification email to a recipient
        :param receiver_email: receiver's email address
        :param image_data: opened and read fire image file
        :param coordinates:  latitude and longitude coordinates of fire location
        :return: None
        """
        message = self.__prepare_message_body(receiver_email, image_data, coordinates)
        try:
            self.smtp_connection.sendmail(self.system_email_address, receiver_email, message)
            logging.info(f"notification sent successfully to {receiver_email}")
        except smtplib.SMTPException as e:
            logging.error(f"Failed to send notification to {receiver_email}: {str(e)}")

    def __prepare_message_body(self, receiver_email: str, image_data: bytes, coordinates: tuple[float, float]) -> str:
        """
        prepare and message body template and content for sending as email
        param receiver_email: receiver's email address
        :param image_data: opened and read fire image file
        :param coordinates:  latitude and longitude coordinates of fire location
        :return: A string representing the formatted email message content
        """
        message = MIMEMultipart()
        message['From'] = self.system_email_address
        message['To'] = receiver_email
        message['Subject'] = EMAIL_SUBJECT

        html_template = STYLE_TEMPLATE + TEMPLATE_BODY_HEADER + f"""        
              <p class="Link">https://www.google.com/maps/search/?api=1&query={coordinates[0]}%2C{coordinates[1]}</p>
            """ + TEMPLATE_BODY_FOOTER

        message.attach(MIMEText(html_template, 'html'))
        fire_image = MIMEImage(image_data, name="fire_alert_image.jpg")
        message.attach(fire_image)
        return message.as_string()
