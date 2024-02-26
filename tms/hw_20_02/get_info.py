''' Модуль сбора параметров'''

import psutil, time, json

# Stack данных доя функции draw_matrix() из модуля dsp.info
# В функции stack_data() текущего модуля новые параметры добавляются в начало и удаляется последняя строка
# В этом модуле изменяется, в модуле main используется для рисования матрицы (модуль вывода информации dsp_info)
stack = [
    "1970-01-01 00:00:00,10.0,10.0,10.0,10.0,10.0,10.0,10.0,10.0",
    "1970-01-01 00:00:00,10.0,10.0,10.0,10.0,10.0,10.0,10.0,10.0",
    "1970-01-01 00:00:00,10.0,10.0,10.0,10.0,10.0,10.0,10.0,10.0",
    "1970-01-01 00:00:00,10.0,10.0,10.0,10.0,10.0,10.0,10.0,10.0",
    "1970-01-01 00:00:00,10.0,10.0,10.0,10.0,10.0,10.0,10.0,10.0",
]

def bytes_to_human(n):
    '''Конвертер байт в гигабайты'''
    
    res = n / (1024 ** 3)
    return round(res, 2)

def log_write(file_name):
    '''Главный декоратор'''
    
    def decorator(func):
        def wrapper():
            info = func()
            data = {
                'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
                'data': info
            }

            with open(f"hw_20_02/{file_name}", "a+") as log:
                log.write(json.dumps(data) + '\n')
            return info
        return wrapper
    return decorator


@log_write('log_cpu_usage.txt')
def stack_data():
    '''Новые параметры процессоров добавляев в начало, последнюю строку удаляет'''
    
    global stack
    current_status = psutil.cpu_percent(interval=1, percpu=True)
    stack = stack[::-1]
    stack.append(f'{time.strftime("%Y-%m-%d %H:%M:%S")},{",".join(map(str, current_status))}')
    stack = stack[::-1]
    stack.pop()
    return current_status


@log_write("log_disk.txt")
def get_disk_info():
    '''Собирает информацию по дискам, пакует в словарь для отправки {имя раздела: данные}'''
    
    parametr = {}
    for part in psutil.disk_partitions(all=False):
        if part.fstype in ("ext4", "vfat"):
            usage = psutil.disk_usage(part.mountpoint)
            parametr[part.device] = [
                bytes_to_human(usage.total), bytes_to_human(usage.used), bytes_to_human(usage.free), usage.percent, part.fstype
                ]
    return parametr
    
    
@log_write("log_vm.txt")
def get_vm_info():
    '''Получает данные по виртуальной памяти'''
    
    vm = psutil.virtual_memory()
    vm_used = bytes_to_human(vm.used)
    vm_total = bytes_to_human(vm.total)
    vm_pct = vm.percent
    return vm_used, vm_total, vm_pct


@log_write("log_swap.txt")
def get_swap_info():
    '''Получает данные по SWAP'''
    
    swap = psutil.swap_memory()
    swap_used = bytes_to_human(swap.used)
    swap_total = bytes_to_human(swap.total)
    swap_pct = swap.percent
    return swap_used, swap_total, swap_pct


