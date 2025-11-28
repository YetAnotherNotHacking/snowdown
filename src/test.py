from notifications import send_notification
from datetime import datetime


servername = "server-1"
failreason = "pingtimeout"
now = datetime.now().astimezone()
timestamp = now.strftime("%Y-%m-%d %H:%M:%S %Z%z")
print("Sending email...")
send_notification.send_email(servername=servername, failreason=failreason, timestamp=timestamp)
print("Sending notification")
send_notification.send_ntfy(servername=servername, timestamp=timestamp, failreason=failreason)