import sys
import traceback

from ServiceManager.service_manager import run_service
from ServiceManager.util.config import LogLevel
from ServiceManager.util.logger import Logger


def run():
    """ usage: python -m ServiceManager <terminal_command> <service_name> <log_level> """

    if len(sys.argv) == 4:
        try:
            cmd = sys.argv[1]
            service_name = sys.argv[2]
            log_level = LogLevel[sys.argv[3]]
            run_service(cmd, service_name, log_level)
        except Exception as err:
            with Logger() as logger:
                logger.log(f"service_manager.py was not able to launch the Service!", log_level=LogLevel.INFO,
                           stdout=True)
                logger.log(f"Error: {err}", log_level=LogLevel.ERROR, stdout=True)
                logger.log(f"Stack: {traceback.format_exc()}", log_level=LogLevel.ERROR, stdout=True)
                logger.log(f"Arguments: {sys.argv[1:]}", log_level=LogLevel.ERROR, stdout=True)
                logger.log("Sending email to admin!", log_level=LogLevel.INFO)
    else:
        with Logger() as logger:
            logger.log(f"service_manager.py has been called with invalid amount of arguments"
                       f" ({len(sys.argv)}, but should be 3)",
                       log_level=LogLevel.INFO, stdout=True)
