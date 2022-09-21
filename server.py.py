from socket import *
from _thread import *


def threaded(connection_socket):
    print('here..')

    try:
        message = connection_socket.recv(1024)
        print(message)
        message = message.decode()
        print(message)
        filename = message.split()[1]
        with open(filename[1:]) as f:
            # f = open(filename[1:])
            output_data = f.readlines()
        print(output_data)

        connection_socket.send(f'{message.split()[2]} 200 OK\r\n'.encode())
        if filename[1:] == 'style.css':
            connection_socket.send('Content-Type:text/css\r\n'.encode())
        else:
            connection_socket.send('Content-Type:text/html\r\n'.encode())
        connection_socket.send('Connection:keep-alive\r\n'.encode())
        connection_socket.send('\r\n'.encode())

        for i in range(0, len(output_data)):
            connection_socket.send(output_data[i].encode())

        connection_socket.send("\r\n\r\n".encode())
    except IOError:
        connection_socket.send(f'HTTP/1.1 404 Not Found\r\n'.encode())
        connection_socket.send('Content-Type:text/html\r\n'.encode())
        connection_socket.send("\r\n".encode())
        connection_socket.send('<h1>File not Found</h1>'.encode())
        connection_socket.send("\r\n\r\n".encode())
        connection_socket.close()


def main():
    server_socket = socket(AF_INET, SOCK_STREAM)

    server_socket.bind(('', 8080))
    server_socket.listen(1)

    while True:
        try:
            print('Ready to serve...')
            connection_socket, addr = server_socket.accept()
            print(connection_socket.getsockname())
            print(addr)
            start_new_thread(threaded, (connection_socket,))
        except SO_ERROR:
            print('Exit')
            break

    server_socket.close()


if __name__ == '__main__':
    main()
