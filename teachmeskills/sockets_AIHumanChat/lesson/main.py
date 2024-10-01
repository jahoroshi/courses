import os
import signal
import time
import sys
import pathlib
from contextlib import suppress

WORK_FLAG = True


def signal_handler(sig, frame):
    frame.f_globals["WORK_FLAG"] = False


PID_FILE = pathlib.Path(".child.pid")


def worker(n):
    for i in range(n):
        print("WORKED:", i)
        if WORK_FLAG:
            time.sleep(10)
        else:
            return


pid = None

if sys.argv[-1] == "-r":
    print(sys.argv)
    print("START")
    pid = os.fork()
    print(1111, pid, '\n')
    if pid:
        print('general', pid)
        print(pid, '\n')
        with open(PID_FILE, "w") as pid_file:
            pid_file.write(str(pid))
    else:
        print('daughter')
        signal.signal(signal.SIGTERM, signal_handler)
        worker(4)
        PID_FILE.unlink(missing_ok=True)
elif sys.argv[-1] == "-k":
    with suppress(FileNotFoundError):
        with open(PID_FILE) as pid_file:
            pid = pid_file.readline().strip()
            os.kill(int(pid), signal.SIGTERM)
    PID_FILE.unlink(missing_ok=True)
else:
    ...

print("STOP", pid)
