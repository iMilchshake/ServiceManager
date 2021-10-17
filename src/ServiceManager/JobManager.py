import os
import subprocess
import sys
import traceback

from ServiceManager.EmailService.EmailService import send_job_fail_mail
from ServiceManager.Logger import Logger
from ServiceManager.util.Config import LogLevel


def run_job(cmd, job_name, log_level):
    """ runs """
    with Logger() as logger:
        if log_level < LogLevel.NOLOG:
            logger.log(f"Starting Job '{job_name}'")

        # run command in subprocess
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = p.communicate()
        status = p.returncode
        encoding = sys.stdout.encoding
        output = list(filter(lambda msg: len(msg) > 0, map(lambda row: row.decode(encoding), output.split(b'\r\n'))))
        error = list(filter(lambda msg: len(msg) > 0, map(lambda row: row.decode(encoding), error.split(b'\r\n'))))

        if log_level == log_level.DEBUG:
            for o in output:
                logger.log(o, log_level=LogLevel.DEBUG)

        if log_level <= LogLevel.ERROR:
            for e in error:
                logger.log(e, log_level=LogLevel.ERROR)

        if log_level < LogLevel.NOLOG:
            logger.log(
                f"Job '{job_name}' Finished {'Successfully' if status == 0 else f'with an Error! - Code({status})'}",
                log_level=LogLevel.INFO)

        # send email to admin
        if status != 0:
            logger.log("Sending email to admin!", log_level=LogLevel.INFO)
            try:
                send_job_fail_mail(job_name)
            except Exception as ex:
                logger.log("An error occurred while trying to send the email", log_level=LogLevel.INFO, stdout=True)
                logger.log(f"Exception: {ex}", log_level=LogLevel.ERROR, stdout=True)
                logger.log(f"Stack: {traceback.format_exc()}", log_level=LogLevel.ERROR, stdout=True)


if __name__ == "__main__":

    print(os.getcwd())

    # JobManager.py <cmd> <jobName> <logLevel>
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
