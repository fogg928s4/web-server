# ITERATIVE WEB SERVER
# Handles several requests and avoids queues

import socket
import time

SERVER_ADDRESS = (HOST, PORT) = '', 8080
REQUEST_SIZE = 6

def handle_request(client_connection):
    request = client_connection.recv(1024)
    print(request.decode("utf-8"))
    http_response = b"""\
HTTP/1.1 200 OK

Hello Mom and Dad :D """
    # sends the response back
    client_connection.sendall(http_response)
    time.sleep(30)  # sleeps for 60 secs just for testing purposes

# Serves permanently
def serve_forever():
    # creates socket over tcp/ip
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # binds teh address and assigns local protocol to socket
    # this specs a port number, ip, or (n)either
    listen_socket.bind(SERVER_ADDRESS)  # server address and the sock
    # set options in order to restart with same address
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.listen(REQUEST_SIZE)  # as many as the req size est
    print(f'Serving HTTP on port {PORT} .....')

    # LOOP IT IN
    while True:
        client_connection, client_address = listen_socket.accept()
        handle_request(client_connection)
        client_connection.close()

# FIRE IT UP
if __name__ == '__main__':
    serve_forever()
