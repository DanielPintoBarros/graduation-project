import smtplib
import os
from dotenv import load_dotenv

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
load_dotenv('.env')

login = "verifyemailapiclient@gmail.com"#os.environ.get("EMAIL_SENDER_LOGIN")
passwd = "Ynb2Yepp"
port = os.environ.get("EMAIL_SENDER_PORT")
host = os.environ.get("EMAIL_SENDER_HOST")
    
def send_email(to, subject, body):
    server = smtplib.SMTP("localhost")
    server.ehlo()
    server.starttls()
    server.login(login, passwd)

    email_msg = MIMEMultipart()
    email_msg['From'] = login
    email_msg['To'] = to
    email_msg['Subject'] = subject

    email_msg.attach(MIMEText(body, 'html'))

    server.sendmail(email_msg['From'], email_msg['To'], email_msg.as_string())
    server.quit()
