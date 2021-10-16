import os
import subprocess
import sys
import traceback

from ServiceManager.EmailService.EmailService import sendJobFailMail
from ServiceManager.Logger import Logger
from ServiceManager.util.Config import LogLevel


def runJob(cmd, jobName, logLevel):
    """ runs """
    with Logger() as logger:
        if logLevel < LogLevel.NOLOG:
            logger.log(f"Starting Job '{jobName}'", logLevel=LogLevel.INFO)

        # run command in subprocess
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = p.communicate()
        status = p.returncode
        encoding = sys.stdout.encoding
        output = list(filter(lambda msg: len(msg) > 0, map(lambda row: row.decode(encoding), output.split(b'\r\n'))))
        error = list(filter(lambda msg: len(msg) > 0, map(lambda row: row.decode(encoding), error.split(b'\r\n'))))

        if logLevel == logLevel.DEBUG:
            for o in output:
                logger.log(o, logLevel=LogLevel.DEBUG)

        if logLevel <= LogLevel.ERROR:
            for e in error:
                logger.log(e, logLevel=LogLevel.ERROR)

        if logLevel < LogLevel.NOLOG:
            logger.log(
                f"Job '{jobName}' Finished {'Successfully' if status == 0 else f'with an Error! - Code({status})'}",
                logLevel=LogLevel.INFO)

        # send email to admin
        if status != 0:
            logger.log("Sending email to admin!", logLevel=LogLevel.INFO)
            try:
                sendJobFailMail(jobName)
            except Exception as ex:
                logger.log("An error occurred while trying to send the email", logLevel=LogLevel.INFO, stdout=True)
                logger.log(f"Exception: {ex}", logLevel=LogLevel.ERROR, stdout=True)
                logger.log(f"Stack: {traceback.format_exc()}", logLevel=LogLevel.ERROR, stdout=True)


if __name__ == "__main__":

    print(os.getcwd())

    # JobManager.py <cmd> <jobName> <logLevel>
    if len(sys.argv) == 4:
        try:
            cmd = sys.argv[1]
            jobName = sys.argv[2]
            logLevel = LogLevel[sys.argv[3]]
            runJob(cmd, jobName, logLevel)
        except Exception as err:
            with Logger() as logger:
                logger.log(f"JobManager.py was not able to launch the Service!", logLevel=LogLevel.INFO, stdout=True)
                logger.log(f"Error: {err}", logLevel=LogLevel.ERROR, stdout=True)
                logger.log(f"Stack: {traceback.format_exc()}", logLevel=LogLevel.ERROR, stdout=True)
                logger.log(f"Arguments: {sys.argv[1:]}", logLevel=LogLevel.ERROR, stdout=True)
                logger.log("Sending email to admin!", logLevel=LogLevel.INFO)
    else:
        with Logger() as logger:
            logger.log(
                f"JobManager.py has been called with invalid amount of arguments ({len(sys.argv)}, but should be 3)",
                logLevel=LogLevel.INFO, stdout=True)
