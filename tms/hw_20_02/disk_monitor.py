import psutil, os, time

def bytes_to_gb(n):
    res = n / (1024 ** 3)
    return round(res, 2)

def clean_screen():
    if psutil.POSIX:
        os.system('clear')
    else:
        os.system('cls')
           
# start Matrix
def draw_matrix(rows, cols, data):
    matrix = [['\033[33m.\033[0m' for _ in range(rows)] for _ in range(cols)]
    c = 0
    for k in range(8):
        for i in range(5):
            val = int(float(data[i][k+1]))
            height = int(val**0.6)     
            for j in range(cols - 1, cols - 1 - height, -1):
                if j >= 0:
                    matrix[j][i+c] = scale_color[k]
        c += 5
    for row in matrix:
        print(' '.join(row))
        
def log_status_cpu(func):
    def cpu_usage():
        with open("/home/jahoroshi4y/Документы/Courses/courses/tms/hw_16_02/log_cpu_usage.txt", "a+") as log:
           log.write(f'{time.strftime("%Y-%m-%d %H:%M:%S")},{",".join(map(str, func()))}\n')
                                   
    return cpu_usage

@log_status_cpu
def stack_data():
    global data
    current_status = psutil.cpu_percent(interval=1, percpu=True)
    data = data[::-1]
    data.append(f'{time.strftime("%Y-%m-%d %H:%M:%S")},{",".join(map(str, current_status))}')
    data = data[::-1]
    data.pop() 
    return current_status

rows = 40
cols = 16
start_time = time.time()
current_time = time.strftime('%Y-%m-%d %H:%M:%S')

scale_color = [
    '\033[32;1m█\033[0m',  
    '\033[33;1m█\033[0m',  
    '\033[34;1m█\033[0m',  
    '\033[35;1m█\033[0m',  
    '\033[36;1m█\033[0m',  
    '\033[37;1m█\033[0m',  
    '\033[91;1m█\033[0m',  
    '\033[93;1m█\033[0m'   
]
data = [
    "2024-02-19 16:34:48,10.0,28.0,21.4,29.0,24.2,24.5,25.0,24.2",
    "2024-02-19 16:34:50,100.4,19.8,34.7,26.5,15.6,17.5,57.1,29.0",
    "2024-02-19 16:34:52,26.8,17.2,14.1,16.3,21.8,14.6,14.4,11.5",
    "2024-02-19 16:34:54,18.8,9.3,11.0,16.0,14.9,18.4,16.0,10.9",
    "2024-02-19 16:34:56,19.6,22.5,19.4,68.7,19.2,42.0,24.0,32.0",
]
# end Matrix
        
def percent_graph_mem(percent):
    fil_blocks = int(percent / 1.5)
    emp_blocks = 60 - fil_blocks
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
    templ_head = "\033[1m%-17s %8s %11s %11s %7s%% %19s\033[0m"
    templ = "%-17s %8s %11s %11s %8s%% %8s"
    print("\033[33;40;1m%-79s\033[0m" % ("Disk status"))

    print(templ_head % ("Device", "Total", "Used", "Free", "Use ", "Type"))
    
    
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
    print("\033[33;40;1m%-79s\033[0m" % ("Memory status"))
    print(templ_vm % ("VM", percent_graph_mem(vm.percent), 
                       f'{bytes_to_gb(vm.used)}G/{bytes_to_gb(vm.total)}G') )
    print(templ_swap % ("Swap", percent_graph_mem(swap.percent),
                       f'{bytes_to_gb(swap.used)}G/{bytes_to_gb(swap.total)}G'))

if __name__ == '__main__':
    flag = 3
    while flag:
        clean_screen()
        print("\033[33;40;1m%-10s%61s\033[0m" % (" CPU Usage Monitor", f'Run time: {str(int(time.time() - start_time))} sec '))
        
        draw_matrix(rows, cols, [row.split(',') for row in data])
        print("\033[33;40;1m  %-10s%-10s%-10s%-10s%-10s%-10s%-10s%-7s\033[0m" % ("CPU 1", "CPU 2", "CPU 3", "CPU 4", "CPU 5", "CPU 6", "CPU 7", "CPU 8"))

               
        print()
        status_mem()
        print()
        status_disk()
        time.sleep(1)
        stack_data()
        flag -= 1 

