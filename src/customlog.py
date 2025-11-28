from datetime import datetime
from colorama import init, Fore, Style

init(autoreset=True)

class Logger:
    def __init__(self, debug=True):
        self.debug_enabled = debug

    def _t(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def _out(self, color, label, msg):
        print(f"{self._t()} [{label}] {color}{msg}{Style.RESET_ALL}")

    def debug(self, msg):
        if self.debug_enabled:
            self._out(Fore.CYAN, "DEBUG", msg)
    
    def debug(self, msg):
        if self.debug_enabled:
            self._out(Fore.CYAN, "DEBUG", msg)

    def info(self, msg):
        self._out(Fore.GREEN, "INFO", msg)

    def warn(self, msg):
        self._out(Fore.YELLOW, "WARN", msg)

    def error(self, msg):
        self._out(Fore.RED, "ERROR", msg)