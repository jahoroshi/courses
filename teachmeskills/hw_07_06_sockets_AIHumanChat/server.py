import select
import socket
import pickle

# sk - proj - l7B6pg12CiOZVNccu1JhT3BlbkFJrXL2iua4HIzO7snESglB

HOST = (socket.gethostname(), 10000)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(HOST)

server.listen()
print('Server now listening')

HEADER_LENGTH = 10
sockets_list = [server]
clients_list = {}

def receive_msg(client: socket.socket):
    try:
        msg_header = client.recv(HEADER_LENGTH)
        if not (len(msg_header)):
            return False

        msg_length = int(msg_header.decode('utf-8').strip())

        return {
            'header': msg_header,
            'data': client.recv(msg_length),
        }
    except:
        return False

while True:
    rs, _, xs = select.select(sockets_list, [], sockets_list)
    for _socket in rs:
        if _socket == server:
            client, address = server.accept()

            user = receive_msg(client)
            if user is False:
                continue
            sockets_list.append(client)
            clients_list[client] = user
            data = user['data']

            print(f'New client connected: {address} with data: {data.decode("utf-8")}')

        else:
            msg = receive_msg(_socket)
            if msg is False:
                print(f'Connection closed by {address}')
                sockets_list.remove(_socket)
                del clients_list[_socket]
                continue

            user = clients_list[_socket]

            for client in clients_list:
                if client is not _socket:
                    client.send(user['header']+user['data']+msg['header']+msg['data'])

        for _socket in xs:
            sockets_list.remove(_socket)
            del clients_list[_socket]




