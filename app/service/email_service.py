import logging as log
import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.conf.app_settings import email_settings


async def send_email(to, subject: str, body: str, attachment_path: str | None = None):
    """
    Send email when attachment_path is valid then send email with attachment
    :param to: Email address of the receiver. A list of addresses to send this mail to. A bare string will be treated as a list with 1 address
    :param subject: Subject of the email, The message to send
    :param body: Content of the email
    :param attachment_path: Path of the file to be attached
    :return: None
    """
    host = email_settings.SMTP_HOST
    port = email_settings.SMTP_PORT
    username = email_settings.SMTP_USERNAME
    password = email_settings.SMTP_PASSWORD
    tls = email_settings.SMTP_TLS

    msg = MIMEMultipart()
    msg['From'] = username
    msg['To'] = to
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # attach the file
    if attachment_path is not None and os.path.exists(attachment_path):
        with open(attachment_path, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename= {os.path.basename(attachment_path)}',
            )
            msg.attach(part)

    try:
        server = smtplib.SMTP(host=host, port=port)
        server.starttls()
        server.login(user=username, password=password)
        text = msg.as_string()
        server.sendmail(from_addr=username, to_addrs=to, msg=text)
        attachment_message = f"File: {attachment_path}" if attachment_path else ""
        log.info(f"Send email to {to} successfully, From: {username} {attachment_message}")
    except Exception as e:
        log.error(f"Failed to send email to {to}, Error: {e}")
        return False
    finally:
        server.quit()

    return True
