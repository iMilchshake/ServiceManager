import subprocess
import sys
import traceback

from ServiceManager.email_service.email_service import send_service_fail_mail
from ServiceManager.util.config import LogLevel
from ServiceManager.util.logger import Logger


def run_service(cmd, service_name, log_level, log_file, cwd, shell):
    """
    runs a service
    :param log_file: path to file to add the log-messages in
    :param cmd: (bash) command to run
    :param service_name: name for the service
    :param log_level: log severity see LogLevel class
    :param cwd: working directory to run the command from.
                On default the current working directory will be used.
    :param shell: whether to run the command with shell-access (use this with caution,
                  https://stackoverflow.com/q/3172470/14502004)
    """

    with Logger(log_file) as logger:
        log_level = LogLevel[log_level]
        if log_level < LogLevel.NOLOG:
            logger.log(f"Starting service: '{service_name}'", log_level=LogLevel.INFO)

        # run command in subprocess
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd, shell=shell)
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
                f"Service '{service_name}' Finished {'Successfully' if status == 0 else f'with an Error! - Code({status})'}",
                log_level=LogLevel.INFO)

        # send email to admin
        if status != 0:
            logger.log("Sending email to admin!", log_level=LogLevel.INFO)
            try:
                send_service_fail_mail(service_name, "<br>".join(error))
                logger.log("Email has been sent!", log_level=LogLevel.INFO)
            except Exception as ex:
                logger.log("An error occurred while trying to send the email", log_level=LogLevel.INFO, stdout=True)
                logger.log(f"Exception: {ex}", log_level=LogLevel.ERROR, stdout=True)
                logger.log(f"Stack: {traceback.format_exc()}", log_level=LogLevel.ERROR, stdout=True)
