import os
import sys
import psutil
from psutil._common import bytes2human

def main():
    templ = "%-17s %8s %8s %8s"
    print(templ % ("Device", "Total", "Used", "Free",))
       
    usage = psutil.disk_usage('/dev/nvme0n1p5')
    print(templ % (
        bytes2human(usage.total),
        bytes2human(usage.used),
        bytes2human(usage.free),
        int(usage.percent),))

if __name__ == '__main__':
    sys.exit(main())
