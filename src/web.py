#!/usr/bin/python3.11

# For Python 3.7+
import socket

HOST, PORT = '', 8888

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.listen(1)
# just a msg as to where it's serving
print(f'Serving HTTP on port https://localhost:{PORT} ...')

while True:
    client_connection, client_address = listen_socket.accept()
    request_data = client_connection.recv(1024)
    print("Request data is: ")
    print(request_data.decode('utf-8'))
    # it works when it feels like it wants to work otherwise it doesn't
    # try writing it somewhere else and then paste
    # otherwise it won't work for some god knows why reason
    http_response = b"""\
    HTTP/1.1 200 OK

    Hello Mom and Dad :D
    """

    client_connection.sendall(http_response)
    # sends the http to the client
    client_connection.close()
