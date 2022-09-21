from socket import *
import sys

n = sys.argv
print(n)

server_name = sys.argv[1]
server_port = sys.argv[2]
filename = sys.argv[3]

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((server_name, int(server_port)))

GET_message = f'GET /{filename} HTTP/1.1\r\n'

client_socket.send(GET_message.encode())

received_data = []

while True:
    message = client_socket.recv(1024).decode()
    received_data.append(message)
    if message == '\r\n\r\n':
        break

print('From Server: \n', received_data)

client_socket.close()



