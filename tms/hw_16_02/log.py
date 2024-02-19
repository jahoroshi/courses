import os, time, psutil

def clean_screen():
    if psutil.POSIX:
        os.system('clear')
    else:
        os.system('cls')
        
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


rows = 40
cols = 16
start_time = time.time()


scale_color = [
    '\033[32;1m█\033[0m',  # Green font
    '\033[33;1m█\033[0m',  # Yellow font
    '\033[34;1m█\033[0m',  # Blue font
    '\033[35;1m█\033[0m',  # Purple font
    '\033[36;1m█\033[0m',  # Cyan font
    '\033[37;1m█\033[0m',  # White font
    '\033[91;1m█\033[0m',  # Light red font
    '\033[93;1m█\033[0m'   # Light yellow font
]
data = [
    "2024-02-19 16:34:48,10.0,28.0,21.4,29.0,24.2,24.5,25.0,24.2",
    "2024-02-19 16:34:50,100.4,19.8,34.7,26.5,15.6,17.5,57.1,29.0",
    "2024-02-19 16:34:52,26.8,17.2,14.1,16.3,21.8,14.6,14.4,11.5",
    "2024-02-19 16:34:54,18.8,9.3,11.0,16.0,14.9,18.4,16.0,10.9",
    "2024-02-19 16:34:56,19.6,22.5,19.4,68.7,19.2,42.0,24.0,32.0",
]



while True:
    clean_screen()
    print("\033[33;40;1m%-10s%61s\033[0m" % (" CPU Usage Monitor", f'Run time: {str(int(time.time() - start_time))} sec '))
    
    draw_matrix(rows, cols, [row.split(',') for row in data])
    print("\033[33;40;1m  %-10s%-10s%-10s%-10s%-10s%-10s%-10s%-7s\033[0m" % ("CPU 1", "CPU 2", "CPU 3", "CPU 4", "CPU 5", "CPU 6", "CPU 7", "CPU 8"))

    time.sleep(1)
    data = data[::-1]
    data.append(f'2024-02-19 16:34:56,{",".join(map(str, psutil.cpu_percent(interval=1, percpu=True)))}')
    data = data[::-1]
    data.pop()  