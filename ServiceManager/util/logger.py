from datetime import datetime

from ServiceManager.util.config import LogLevel


class Logger:

    def __init__(self, log_file):
        if log_file is None:
            log_file = "services.log"  # save to cwd with default name

        self.file = open(log_file, "a")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()

    def log(self, message, log_level: LogLevel = LogLevel.ERROR, stdout=True):
        message = f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] [{log_level.name.rjust(5)}] {message}"
        self.file.write(message + "\n")

        if stdout:
            print(message)
