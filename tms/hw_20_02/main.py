import psutil, os, time
import dsp_info
import get_info

def clean_screen():
    if psutil.POSIX:
        os.system('clear')
    else:
        os.system('cls')
           
start_time = time.time()
# current_time = time.strftime('%Y-%m-%d %H:%M:%S')

 
def main():  
    
    flag = 15
    while flag:
        clean_screen()
        # Start CPU usage
        print("\033[33;40;1m%-10s%61s\033[0m" % (" CPU Usage Monitor", f'Run time: {str(int(time.time() - start_time))} sec '))
        dsp_info.draw_matrix([row.split(',') for row in get_info.stack])
        print("\033[33;40;1m  %-10s%-10s%-10s%-10s%-10s%-10s%-10s%-7s\033[0m" % ("CPU 1", "CPU 2", "CPU 3", "CPU 4", "CPU 5", "CPU 6", "CPU 7", "CPU 8")) 
        # End CPU usage
        print()
        # Start memory status
        print("\033[33;40;1m%-79s\033[0m" % ("Memory status"))
        dsp_info.display_memory_status(*get_info.get_vm_info(), *get_info.get_swap_info())
        # End memory status
        print()
        # Start disk status
        print("\033[33;40;1m%-79s\033[0m" % ("Disk status"))
        print("\033[1m%-17s %8s %11s %11s %7s%% %19s\033[0m" % ("Device", "Total", "Used", "Free", "Use ", "Type"))
        dsp_info.display_disk_info(get_info.get_disk_info())    
        # End disk status    
        time.sleep(1)
        get_info.stack_data()
        flag -= 1 

if __name__ == '__main__':
    main()
