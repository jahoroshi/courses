import socket
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from multiprocessing import Process, freeze_support
import time
from random import random

SRV_ADDR = ("127.0.0.1", 8008)


def connect(num):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(SRV_ADDR)

    req = f"Client number: {num}"
    sock.send(req.encode("utf-8"))
    data = sock.recv(2048)
    print(data.decode("utf-8"))
    time.sleep(random() / 100)
    req = f"Second data, num: {num}"
    sock.send(req.encode("utf-8"))
    data = sock.recv(2048)
    print(data.decode("utf-8"))
    sock.close()


workers = [Process(target=connect, args=(n,)) for n in range(200)]

if __name__ == "__main__":

    freeze_support()
    for w in workers:
        w.start()
