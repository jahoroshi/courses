import socket
from time import sleep
from random import random

SRV_ADDR = ("127.0.0.1", 8008)

srv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
srv_sock.bind(SRV_ADDR)
srv_sock.listen(10)

while True:
    client, addr = srv_sock.accept()
    data = client.recv(2048)
    print(data.decode("utf-8"))
    sleep(random() / 10)
    response = f"client {addr}, resp: "
    client.send(response.encode("utf-8") + data)
    client.close()
