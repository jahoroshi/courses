psutil.cpu_times() время работы системного процессора,
psutil.cpu_percent() текущая загрузка ЦП в процентах, "psutil.cpu_percent(interval=None, percpu=False)"

psutil.cpu_times_percent() то же, что psutil.cpu_times(percpu=True),
psutil.cpu_count() количество логических и физических процессоров,
psutil.cpu_stats() различная статистика ЦП,
psutil.cpu_freq() частота ЦП,
psutil.getloadavg() средняя загрузка системы,
psutil.boot_time() время загрузки системы.

psutil.virtual_memory() статистика об использовании системной памяти RAM,
psutil.swap_memory() статистика об использовании SWAP,

psutil.disk_partitions() все смонтированные разделы диска,
psutil.disk_usage() статистика использования диска для раздела,
psutil.disk_io_counters() общесистемная статистика дискового ввода-вывода;

psutil.net_io_counters() общесистемная статистика сетевого ввода-вывода,
psutil.net_connections() общесистемные соединения сокетов,
psutil.net_if_addrs() адреса, связанные с каждой сетевой картой,
psutil.net_if_stats() информацию о каждой сетевой карте,

psutil.pids() список текущих запущенных PID,
psutil.process_iter() итератор всех запущенных процессов,
psutil.pid_exists() проверяет, существует ли данный PID,
psutil.wait_procs() вызывается, когда один из ожидающих процессов завершается,

psutil.sensors_temperatures() показания температуры оборудования,
psutil.sensors_fans() скорость аппаратных вентиляторов,
psutil.sensors_battery() информация о состоянии батареи,


