import multiprocessing as mp
import random
import time
import os


def worker1(num, queue):
    print("START:", num)
    print("SELF PID:", os.getpid())
    print("PARENT PID:", os.getppid())
    queue.put(f"process: {os.getpid()}. data: {num} fdfsfdfdsfsdfdfsdfsdfsdfsdfsdfsdfdsfsdffdsfsdfs")
    time.sleep(random.randrange(5, 10))
    data = queue.get()
    print(data, 'p1')
    print("STOP:", num)


def worker2(num, queue):
    print("START:", num)
    print("SELF PID:", os.getpid())
    print("PARENT PID:", os.getppid())
    time.sleep(random.randrange(1, 5))
    data = queue.get()
    print(data, 'p2')
    queue.put(f"process: {os.getpid()}. data: {num}")
    print("STOP:", num)


if __name__ == '__main__':
    mp.freeze_support()
    q = mp.Queue()
    worker_1 = mp.Process(target=worker1, args=(1, q))
    worker_2 = mp.Process(target=worker2, args=(2, q))
    print("SELF_PARENT:", os.getpid(), '\n')

    worker_1.start()
    worker_2.start()

    worker_1.join()
    worker_2.join()

    print("parent stop")
