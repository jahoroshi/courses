import socket
import threading
import sys
from openai_chat import chat_with_gpt

HEADER_LENGTH = 10
SERVER = (socket.gethostname(), 10000)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
username = input('Enter your username: ')
username_encode = username.encode('utf-8')

client.connect(SERVER)
client.setblocking(0)
print('Connected to', SERVER)

header = f"{len(username_encode):<{HEADER_LENGTH}}".encode('utf-8')
client.send(header + username_encode)


def receive_messages():
    while True:
        try:
            user_header = client.recv(HEADER_LENGTH)
            if not len(user_header):
                print("\nConnection closed by the server")
                sys.exit()
            user_length = int(user_header.decode('utf-8').strip())
            sender_username = client.recv(user_length).decode('utf-8')

            msg_header = client.recv(HEADER_LENGTH)
            msg_length = int(msg_header.decode('utf-8').strip())
            msg = client.recv(msg_length).decode('utf-8')

            if msg:
                gpt_msg = chat_with_gpt(msg, username)
                if gpt_msg is None:
                    continue
                msg_to_server = gpt_msg.encode('utf-8')
                msg_header = f"{len(msg_to_server ):<{HEADER_LENGTH}}".encode('utf-8')
                client.send(msg_header + msg_to_server)

                print(f'\033[30;47;1m {" "*3} %-10s %-10s\033[0m' % (sender_username, msg))
                print(f'\033[33;40;1m %-10s %-10s\033[0m' % (username, gpt_msg))
        except BlockingIOError:
            continue
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")
            sys.exit()


receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

