import os
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from celery import Celery

from models import Event, User

# Initialize Celery with broker and backend settings from environment variables
celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://redis:6379/0")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://redis:6379/0")


@celery.task(name='send_notification')
def send_notification(*args, **kwargs):
    """
    Celery task to send an email notification about an event.

    Args:
        args: Positional arguments containing event and user information.
        kwargs: Keyword arguments (not used in this example).
    """

    # # SMTP server configuration (replace with actual values)
    # smtp_server = ...
    # smtp_port = 587
    # smtp_user = ...
    # smtp_password = ...
    #
    # # Extract necessary data from args
    # from_email = ...
    # to_email = args.email  # The recipient's email address
    # subject = 'Event notification'
    # time_until_event = args.meeting_time - notification_time
    # hours_until_event = time_until_event.total_seconds() // 3600
    #
    # # Construct the email body
    # body = f'{args.name.capitalize()} will start in {int(hours_until_event)} hours.'
    #
    # # Create the email message
    # msg = MIMEMultipart()
    # msg['From'] = from_email
    # msg['To'] = to_email
    # msg['Subject'] = subject
    # msg.attach(MIMEText(body, 'plain'))
    #
    # try:
    #     # Connect to the SMTP server and send the email
    #     server = smtplib.SMTP(smtp_server, smtp_port)
    #     server.starttls()  # Upgrade the connection to a secure TLS connection
    #     server.login(smtp_user, smtp_password)
    #     server.send_message(msg)
    #     print(f'Email sent successfully to {to_email}')
    #
    # except Exception as e:
    #     # Print an error message if something goes wrong
    #     print(f'Failed to send email: {e}')
    #
    # finally:
    #     # Ensure the connection to the SMTP server is closed
    #     server.quit()
    #
    # # Uncomment the following line to test task execution
    print('🎉🎉🎉 It\'s work! 🎉🎉🎉')
