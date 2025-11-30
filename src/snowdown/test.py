from snowdown.notifications import send_notification
from datetime import datetime
from snowdown.customlog import Logger

log = Logger(debug=False)


servername = "server-1"
failreason = "pingtimeout"
now = datetime.now().astimezone()
timestamp = now.strftime("%Y-%m-%d %H:%M:%S %Z%z")
log.debug("Sending email...")
send_notification.send_email(servername=servername, failreason=failreason, timestamp=timestamp)
log.debug("Sending notification")
send_notification.send_ntfy(servername=servername, timestamp=timestamp, failreason=failreason)