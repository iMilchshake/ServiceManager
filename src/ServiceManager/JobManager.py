import subprocess
import sys

from ServiceManager.util.Config import LogLevel


def _runCmd(cmd):
    """ runs a given command in a subprocess and returns its status-code, output and error
        DONT CALL THIS DIRECTLY, Call runJob() instead!
     """

    encoding = sys.stdout.encoding
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = p.communicate()
    status = p.returncode
    output = list(map(lambda row: row.decode(encoding), output.split(b'\r\n')))
    error = list(map(lambda row: row.decode(encoding), error.split(b'\r\n')))
    return status, output, error


def runJob(cmd, jobName, logLevel):
    """ runs """
    if logLevel < LogLevel.NOTHING:
        print(f"[LOG]: Starting Job '{jobName}'")

    status, output, error = _runCmd(cmd)

    if logLevel <= LogLevel.ERRORS and len(error) > 1:
        print("[ERRORS]:")
        print("\n".join(error))

    if logLevel == logLevel.DEBUG and len(output) > 1:
        print("[DEBUG]:")
        print("\n".join(output))

    if logLevel <= LogLevel.ERRORS:
        print(f"[LOG]: Job '{jobName}' Finished {'Successfully' if status == 0 else 'with an Error!'}")


if __name__ == "__main__":
    runJob("python ServiceManager/TestService.py", "testJob", logLevel=LogLevel.DEBUG)
