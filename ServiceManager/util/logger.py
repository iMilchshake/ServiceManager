import os
from datetime import datetime

from ServiceManager.util.config import LogLevel


class Logger:

    def __init__(self):
        script_path = os.path.dirname(__file__)
        log_file_path = os.path.join(script_path, '../services.log')
        self.file = open(log_file_path, "a")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()

    def log(self, message, log_level: LogLevel = None, stdout=True):
        if log_level is not None:
            message = f"[{log_level.name.rjust(5)}] {message}"
        message = f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] {message}"
        self.file.write(message + "\n")

        if stdout:
            print(message)
