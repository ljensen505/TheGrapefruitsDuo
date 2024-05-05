import smtplib
from email.mime.text import MIMEText
from os import getenv

from app.constants import HOST


def send_email(subject: str, body: str) -> None:
    """
    Sends an email using the Gmail SMTP server.

    :param str subject: The subject of the email
    :param str body: The body of the email
    """
    password = getenv("APP_PASSWORD")
    email = getenv("EMAIL")
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = HOST
    smtp_server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    smtp_server.login(HOST, password)  # type: ignore
    smtp_server.sendmail(HOST, [email], msg.as_string())  # type: ignore
    smtp_server.quit()
