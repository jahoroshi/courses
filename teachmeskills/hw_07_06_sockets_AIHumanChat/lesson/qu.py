from subprocess import Popen, PIPE
import os


proc = Popen(("ls", "-al", os.getenv("HOME")), stdout=PIPE, stdin=PIPE)
# proc = Popen(("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "www.google.com"), stdout=PIPE, stdin=PIPE)
s_out, s_err = proc.communicate()

print(s_out.decode("utf-8"))
