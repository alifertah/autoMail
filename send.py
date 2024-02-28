import smtplib
import sys, os
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.base import MIMEBase


load_dotenv()
file_to_send_name = os.getenv('ATTACHEMENT')
attachment = open(file_to_send_name, 'rb')

part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename= %s" % file_to_send_name)

sender_email = os.getenv('SENDER')
receiver_email = sys.argv[1]
password = os.getenv('PASSWORD')

message = MIMEMultipart()
message['From'] = sender_email
message['To'] = receiver_email
file = open('message.txt', 'rb')
content = file.read()
encoded_content = content.decode('utf-8')
message['Subject'] =  os.getenv('SUBJECT')

body = encoded_content
message.attach(MIMEText(body, 'plain'))
message.attach(part)


try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message.as_string())
    print('Email sent successfully!')
except Exception as e:
    print(f'An error occurred: {e}')
finally:
    server.quit()
