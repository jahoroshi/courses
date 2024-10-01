'''Модуль вывода информации'''

def pct_graph_mem(pct):
    '''Рисует шкалу загруженности для блока вывода информации о памяти'''
    fil_blocks = int(pct / 1.65)
    emp_blocks = 60 - fil_blocks
    if pct < 49:
        color_scale = '\033[32m|\033[0m'
    elif pct < 79:
        color_scale = '\033[33m|\033[0m'
    else:
         color_scale = '\033[31m|\033[0m'
       
    bar = color_scale * fil_blocks + ' ' * emp_blocks
    return bar


def pct_graph_disk(pct):
    '''Рисует шкалу загруженности для блока вывода информации о дисках'''

    fil_blocks = int(pct / 10)
    emp_blocks = 10 - fil_blocks
    if pct < 85:
        сolor_scale = '\033[32m|\033[0m'
    else:
        сolor_scale = '\033[31m|\033[0m'

    bar = сolor_scale * fil_blocks + ' ' * emp_blocks
    return f'  {bar} {pct}%'



def draw_matrix(data, rows=40, cols=16):
    '''Рисует матрицу для монитора загрузки ЦПУ и отображает их загруженность'''
    
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
    
    
    
def display_disk_info(parametr):
    '''Выводит блок индикации загрузки дисков'''
    
    templ = "%-17s %8s %11s %11s %8s%% %8s"
    for key, value in parametr.items():
        print(templ % (
                key,
                value[0],
                value[1],
                value[2],
                pct_graph_disk(value[3]),
                value[4],
                ))
            

def display_memory_status(
    vm_used, vm_total, vm_pct, 
    swap_pct, swap_used, swap_total
    ):
    '''Выводит блок статуса памяти и свопа'''
    
    templ_vm = "%-5s :%s %s"
    templ_swap = "%-5s :%s %s"
    print(templ_vm % ("VM", pct_graph_mem(vm_pct), 
                       f'{vm_used}G/{vm_total}G') )
    print(templ_swap % ("Swap", pct_graph_mem(swap_pct),
                       f'{swap_used}G/{swap_total}G'))
   