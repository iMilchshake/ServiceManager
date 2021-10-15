from datetime import datetime

from ServiceManager.util.Config import LogLevel


class Logger:

    def __init__(self):
        self.file = open("jobs.log", "a")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()

    def log(self, message, logLevel: LogLevel = None, stdout=True):
        if logLevel is not None:
            message = f"[{logLevel.name.rjust(5)}] {message}"
        message = f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] {message}"
        self.file.write(message + "\n")

        if stdout:
            print(message)
