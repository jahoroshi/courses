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

def log_status_cpu(func):
    def cpu_usage():
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')
        with open("courses/tms/hw_16_02/log_cpu_usage.txt", "a+") as log:
           log.write(f'{current_time},{",".join(map(str, func()))}\n')
                      
    return cpu_usage

@log_status_cpu
def status_cpu():
    templ_cpu_per = "%-4s :%s %11s"
    cpu_per = psutil.cpu_percent(interval=1, percpu=True)
    clean_screen()
    print("\033[33;40;1m%-69s\033[0m" % ("CPU status"))

    for i in range(len(cpu_per)):
        print(templ_cpu_per % (f'CPU {i}', percent_graph_mem(cpu_per[i]), cpu_per[i]))
    return cpu_per     


if __name__ == '__main__':
    period = int(input("\033[36;41m%-28s\033[0m" % ("Установите период профилирования: ")))
    while period:
        status_cpu()
        time.sleep(1)
        period -= 1
