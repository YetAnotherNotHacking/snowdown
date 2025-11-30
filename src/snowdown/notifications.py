import requests
import smtplib
from email.message import EmailMessage
from snowdown.settings import SDSettings

class send_notification:
    def send_email(servername, timestamp, failreason):
        # load all settings from the configs
        name = SDSettings.name
        smtp_host = SDSettings.mail_server
        smtp_port = SDSettings.mail_port
        username = SDSettings.mail_user
        password = SDSettings.mail_passphrase
        to_addr = SDSettings.mail_target
        subject = SDSettings.build_email_heading(servername=servername, failreason=failreason)
        body = SDSettings.build_email_body(name=name, servername=servername, timestamp=timestamp, failreason=failreason)

        msg = EmailMessage()
        msg["From"] = username
        msg["To"] = to_addr
        msg["Subject"] = subject
        msg.set_content(body)
        with smtplib.SMTP_SSL(smtp_host, smtp_port) as s:
            s.login(username, password)
            s.send_message(msg)
    
    def send_ntfy(servername, timestamp, failreason):
        title = SDSettings.ntfy_title
        endpoint = SDSettings.ntfy_endpoint
        message = SDSettings.build_notification_content(servername=servername, failreason=failreason)
        headers = {}
        headers["Title"] = title
        requests.post(endpoint, data=message.encode(), headers=headers)
        
