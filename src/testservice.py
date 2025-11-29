import requests
from customlog import Logger
import socket
import smtplib
import imaplib
from contextlib import closing

log = Logger(debug=True)

class check_service_up:
    def check_http(url, timeout=10):
        log.debug(f"Checking http url {url}")
        try:
            r = requests.get(url, allow_redirects=True, timeout=timeout)
            return r.status_code == 200
        except requests.RequestException as e:
            return False

    def check_minecraft(host, port=25565, timeout=5):
        log.debug(f"Checking MineCraft server {host} on port {port}")
        try:
            import mcstatus
            server = mcstatus.MinecraftServer(host, port)
            status = server.status()
            return status.players.online >= 0
        except Exception:
            return False

    def check_ssh(host, port=22, timeout=5):
        log.debug(f"Checking ssh connectivity to {host} on port {port}")
        try:
            with socket.create_connection((host, port), timeout=timeout):
                return True
        except Exception:
            return False

    def check_ping(host, count=1, timeout=1):
        try:
            result = subprocess.run(
                ["ping", "-c", str(count), "-W", str(timeout), host],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            return result.returncode == 0
        except Exception:
            return False