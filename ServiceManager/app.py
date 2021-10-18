import argparse
import sys
import traceback

from ServiceManager.email_service.email_service import send_service_fail_mail
from ServiceManager.service_manager import run_service
from ServiceManager.util.config import LogLevel
from ServiceManager.util.logger import Logger


def run():
    parser = argparse.ArgumentParser(description="A simple service manager", prefix_chars="/-",
                                     prog="python -m ServiceManager")
    parser.add_argument("cmd", type=str, help="a terminal command to run")
    parser.add_argument("name", type=str, help="the name for the service")
    parser.add_argument("--log", type=str, help="log severity", default="ERROR",
                        choices=["DEBUG", "ERROR", "INFO", "NOLOG"])
    parser.add_argument("--cwd", type=str, help="working directory to run the command from."
                                                "On default the current working directory will be used")
    parser.add_argument("--shell", action="store_true", help="enable shell mode")
    args = vars(parser.parse_args())

    try:
        run_service(args["cmd"], args["name"], args["log"], args["cwd"], args["shell"])
    except Exception as err:
        with Logger() as logger:
            logger.log(f"service_manager.py was not able to launch the Service!", log_level=LogLevel.INFO,
                       stdout=True)
            logger.log(f"Error: {err}", log_level=LogLevel.ERROR, stdout=True)
            logger.log(f"Stack: {traceback.format_exc()}", log_level=LogLevel.ERROR, stdout=True)
            logger.log(f"Arguments: {sys.argv[1:]}", log_level=LogLevel.ERROR, stdout=True)
            logger.log("Sending email to admin!", log_level=LogLevel.INFO)

            try:
                # send_service_fail_mail(args["name"])
                logger.log("Email has been sent!", log_level=LogLevel.INFO)
            except Exception as ex:
                logger.log("An error occurred while trying to send the email", log_level=LogLevel.INFO, stdout=True)
                logger.log(f"Exception: {ex}", log_level=LogLevel.ERROR, stdout=True)
                logger.log(f"Stack: {traceback.format_exc()}", log_level=LogLevel.ERROR, stdout=True)
