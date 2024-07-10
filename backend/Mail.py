import smtplib
from dotenv import load_dotenv
import os
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 

type Email = str

load_dotenv()
TO_USER = "testbenchonly@gmail.com"

BODY = """
    <html>
        <body>
        <p>This is an html email</p>
        </body>
    </html>
"""
class Email():
    @classmethod
    # https://www.geeksforgeeks.org/send-mail-gmail-account-using-python/
    # https://mailtrap.io/blog/python-send-email-gmail/
    def send_email(cls, recipients: list[Email], subject: str, body: str, attachments: list[MIMEBase] = [], is_html: bool = False):
        # creates SMTP session
        with smtplib.SMTP('smtp.gmail.com', 587) as s:
            # start TLS for security
            s.starttls()
            # Authentication
            s.login(os.getenv("EMAIL_USERNAME"), os.getenv("EMAIL_PASSWORD"))

            # message to be sent
            message = MIMEMultipart()
            message["Subject"] = subject
            message["To"] = ",".join(recipients)
            message.attach(MIMEText(body, "plain" if not is_html else "html"))

            for attachment in attachments:
                message.attach(attachment)

            s.sendmail(os.getenv("EMAIL_USERNAME"), recipients, message.as_string())

if __name__ == "__main__":
    Email.send_email(["testbenchonly5@gmail.com"], "Header2", "this is it")