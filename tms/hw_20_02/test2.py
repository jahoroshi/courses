import psutil
def processor_show():
    proc = psutil.process_iter()
    proc_dict = {key: [] for key in range(psutil.cpu_count())}
    templ_show_process = '%-10s %-10s %-10s %-10s %-10s %-10s %-10s %-10s'


    for process in proc:
        proc_dict[process.cpu_num()].append(process.name()[0:5])
    print(proc_dict)
    
    for el in proc_dict:
        proc_dict[el] = proc_dict[el][::-1]
    print(proc_dict)

    for j in range(70):
        row = 0
        # print(templ_show_process % tuple(proc_dict[i][j] for i in range(8)))
        row += 1
        
processor_show()
