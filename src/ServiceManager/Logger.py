from datetime import datetime

from ServiceManager.util.Config import LogLevel


def log(message, logLevel: LogLevel = None, stdout=True):
    with open("jobs.log", "a") as file:
        if logLevel is not None:
            message = f"[{logLevel.name.rjust(6)}] {message}"
        message = f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] {message}"
        file.write(message + "\n")

        if stdout:
            print(message)

