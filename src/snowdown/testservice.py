import requests
from snowdown.customlog import Logger
import socket
import subprocess
from concurrent.futures import ThreadPoolExecutor, TimeoutError

log = Logger(debug=True)

# timeout
def _timeout_wrapper(func, *args, **kwargs):
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(func, *args, **kwargs)
        try:
            return future.result(timeout=15)  # hard limit
        except TimeoutError:
            log.debug(f"{func.__name__} timed out after 15 seconds without a retrun")
            return False
        except Exception:
            return False


class check_service_up:

    @staticmethod
    def check_http(url, timeout=10):
        def inner():
            log.debug(f"Checking http url {url}")
            try:
                r = requests.get(url, allow_redirects=True, timeout=timeout)
                return r.status_code == 200
            except requests.RequestException:
                return False
        return _timeout_wrapper(inner)

    @staticmethod
    def check_minecraft(host, port=25565, timeout=5):
        def inner():
            log.debug(f"Checking MineCraft server {host} on port {port}")
            try:
                import mcstatus
                server = mcstatus.MinecraftServer(host, port)
                status = server.status()
                return status.players.online >= 0
            except Exception:
                return False
        return _timeout_wrapper(inner)

    @staticmethod
    def check_ssh(host, port=22, timeout=5):
        def inner():
            log.debug(f"Checking ssh connectivity to {host} on port {port}")
            try:
                with socket.create_connection((host, port), timeout=timeout):
                    return True
            except Exception:
                return False
        return _timeout_wrapper(inner)

    @staticmethod
    def check_ping(host, count=1, timeout=1):
        def inner():
            try:
                result = subprocess.run(
                    ["ping", "-c", str(count), "-W", str(timeout), host],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                return result.returncode == 0
            except Exception:
                return False
        return _timeout_wrapper(inner)
