import socket
import threading
import sys

HEADER_LENGTH = 10
SERVER = (socket.gethostname(), 10000)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
username = input('Enter your username: ').encode('utf-8')

client.connect(SERVER)
client.setblocking(0)
print('Connected to', SERVER)

header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client.send(header + username)

def receive_messages():
    while True:
        try:
            user_header = client.recv(HEADER_LENGTH)
            if not len(user_header):
                print("\nConnection closed by the server")
                sys.exit()
            user_length = int(user_header.decode('utf-8').strip())
            username = client.recv(user_length).decode('utf-8')

            msg_header = client.recv(HEADER_LENGTH)
            msg_length = int(msg_header.decode('utf-8').strip())
            msg = client.recv(msg_length).decode('utf-8')

            print(f'\r\033[K   {username}\'s message {msg}')
            print('Your message: ', end='', flush=True)
        except BlockingIOError:
            continue
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")
            sys.exit()

def send_messages():
    while True:
        try:
            msg = input('Your message: ').encode('utf-8')
            if msg:
                msg_header = f"{len(msg):<{HEADER_LENGTH}}".encode('utf-8')
                client.send(msg_header + msg)

        except Exception as e:
            print(f"\nAn error occurred while sending the message: {str(e)}")
            sys.exit()

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

send_thread = threading.Thread(target=send_messages)
send_thread.start()
