import subprocess
import sys

from ServiceManager.Logger import Logger
from ServiceManager.util.Config import LogLevel


def _runCmd(cmd):
    """ runs a given command in a subprocess and returns its status-code, output and error
        DONT CALL THIS DIRECTLY, Call runJob() instead!
     """

    encoding = sys.stdout.encoding
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = p.communicate()
    status = p.returncode
    output = list(filter(lambda msg: len(msg) > 0, map(lambda row: row.decode(encoding), output.split(b'\r\n'))))
    error = list(filter(lambda msg: len(msg) > 0, map(lambda row: row.decode(encoding), error.split(b'\r\n'))))
    return status, output, error


def runJob(cmd, jobName, logLevel):
    """ runs """
    with Logger() as logger:
        if logLevel < LogLevel.NO_LOG:
            logger.log(f"Starting Job '{jobName}'", logLevel=LogLevel.INFO)

        status, output, error = _runCmd(cmd)

        if logLevel == logLevel.DEBUG:
            for o in output:
                logger.log(o, logLevel=LogLevel.DEBUG)

        if logLevel <= LogLevel.ERRORS:
            for e in error:
                logger.log(e, logLevel=LogLevel.ERRORS)

        if logLevel < LogLevel.NO_LOG:
            logger.log(f"Job '{jobName}' Finished {'Successfully' if status == 0 else 'with an Error!'}",
                       logLevel=LogLevel.INFO)


if __name__ == "__main__":
    runJob("python ServiceManager/TestService.py", "testJob", logLevel=LogLevel.DEBUG)
