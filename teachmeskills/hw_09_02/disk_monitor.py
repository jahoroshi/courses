import psutil, os, time

def bytes_to_gb(n):
    res = n / (1024 ** 3)
    return round(res, 2)

def clean_screen():
    if psutil.POSIX:
        os.system('clear')
    else:
        os.system('cls')
        
def percent_graph_mem(percent):
    fil_blocks = int(percent / 2)
    emp_blocks = 50 - fil_blocks
    if percent < 49:
        color_scale = '\033[32m|\033[0m'
    elif percent < 79:
        color_scale = '\033[33m|\033[0m'
    else:
         color_scale = '\033[31m|\033[0m'
       
    bar = color_scale * fil_blocks + ' ' * emp_blocks
    return bar

def percent_graph_disk(percent):
    fil_blocks = int(percent / 10)
    emp_blocks = 10 - fil_blocks
    if percent < 85:
        сolor_scale = '\033[32m|\033[0m'
    else:
        сolor_scale = '\033[31m|\033[0m'

    bar = сolor_scale * fil_blocks + ' ' * emp_blocks

    return f'  {bar} {percent}%'

def status_disk():
    templ_head = "\033[1m%-17s %5s %8s %8s %6s%% %7s\033[0m"
    templ = "%-17s %5s %8s %8s %6s%% %7s"
    print("\033[33;40;1m%-69s\033[0m" % ("Disk status"))

    print(templ_head % ("Device", "Total", "Used", "Free", "Use ", "               Type"))
    
    
    for part in psutil.disk_partitions(all=False):
        if part.fstype in ("ext4", "vfat"):
            usage = psutil.disk_usage(part.mountpoint)
            print(templ % (
                part.device,
                bytes_to_gb(usage.total),
                bytes_to_gb(usage.used),
                bytes_to_gb(usage.free),
                percent_graph_disk(usage.percent),
                part.fstype,
                ))

def status_cpu():
    templ_cpu_per = "%-4s :%s %11s"
    cpu_per = psutil.cpu_percent(interval=1, percpu=True)
    clean_screen()
    pr = '''
                                ●
                              <{ }>
                               / \ 
              '''
    print(pr)
    print("\033[33;40;1m%-69s\033[0m" % ("CPU status"))

    for i in range(len(cpu_per)):
        print(templ_cpu_per % (f'CPU {i}', percent_graph_mem(cpu_per[i]), cpu_per[i]))


def status_mem():
    vm = psutil.virtual_memory()
    swap = psutil.swap_memory()
    templ_vm = "%-5s :%s %s"
    templ_swap = "%-5s :%s %s"
    print("\033[33;40;1m%-69s\033[0m" % ("Memory status"))
    print(templ_vm % ("VM", percent_graph_mem(vm.percent), 
                       f'{bytes_to_gb(vm.used)}G/{bytes_to_gb(vm.total)}G') )
    print(templ_swap % ("Swap", percent_graph_mem(swap.percent),
                       f'{bytes_to_gb(swap.used)}G/{bytes_to_gb(swap.total)}G'))

if __name__ == '__main__':
    while True:
        status_cpu()
        print()
        status_mem()
        print()
        status_disk()
        time.sleep(1)
