import smtplib
from email.message import EmailMessage
from loguru import logger
import os

GMAIL_USER = os.environ.get("GMAIL_USER")
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD")

def send_confirmation_email(to_email: str, confirmation_url: str):
    """
    Send a confirmation email to the user.
    
    Args:
        to_email (str): The recipient's email address.
        confirmation_link (str): The link for email confirmation.
    """
    msg = EmailMessage()
    msg['Subject'] = 'Email Confirmation'
    msg['From'] = GMAIL_USER
    msg['To'] = to_email
    msg.set_content(f"Please confirm your email by clicking the link: {confirmation_url}")

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            smtp.send_message(msg)
        logger.success(f"Confirmation email sent to {to_email}")
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {e}")

def send_verification_code_email(to_email: str, code: str):
    """
    Send a verification code email to the user.
    """
    msg = EmailMessage()
    msg['Subject'] = 'Your Verification Code'
    msg['From'] = GMAIL_USER
    msg['To'] = to_email
    msg.set_content(f"Your verification code is: {code}")

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            smtp.send_message(msg)
        logger.success(f"Verification code email sent to {to_email}")
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {e}")
