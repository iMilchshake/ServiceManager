import sys
import traceback

from ServiceManager.job_manager import run_job
from ServiceManager.util.config import LogLevel
from ServiceManager.util.logger import Logger


def run():
    if len(sys.argv) == 4:
        try:
            cmd = sys.argv[1]
            job_name = sys.argv[2]
            log_level = LogLevel[sys.argv[3]]
            run_job(cmd, job_name, log_level)
        except Exception as err:
            with Logger() as logger:
                logger.log(f"JobManager.py was not able to launch the Service!", log_level=LogLevel.INFO, stdout=True)
                logger.log(f"Error: {err}", log_level=LogLevel.ERROR, stdout=True)
                logger.log(f"Stack: {traceback.format_exc()}", log_level=LogLevel.ERROR, stdout=True)
                logger.log(f"Arguments: {sys.argv[1:]}", log_level=LogLevel.ERROR, stdout=True)
                logger.log("Sending email to admin!", log_level=LogLevel.INFO)
    else:
        with Logger() as logger:
            logger.log(
                f"JobManager.py has been called with invalid amount of arguments ({len(sys.argv)}, but should be 3)",
                log_level=LogLevel.INFO, stdout=True)
