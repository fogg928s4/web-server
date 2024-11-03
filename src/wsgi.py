# Python Web Server Gateway Interface or WSGI
# wsgi allows us to use diff web fw with diff web servers
# this allows us to not make changes to the server when implementing a new fw
# it allows us to choose a fw that suits and benefits both the server and the app
# other langs have similar like Java's Servlet API and Ruby's Rack

import io
import queue
import socket
import sys

# create a WSGI Server class
class WSGIServer(object):
    # properties
    addressFamily = socket.AF_INET
    socketType = socket.SOCK_STREAM
    requestQueueSize = 1

    # initializes the server
    def __init__(self, server_address):
        self.listen_socket = listen_socket = socket.socket(
            self.addressFamily,
            self.socketType
        )
        # allow reuse same addr
        listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # bind
        listen_socket.bind(server_address)

        # ACTIVATE IT!!!
        listen_socket.listen(self.requestQueueSize)

        # get a server host name and port
        host, port = self.listen_socket.getsockname()[:2]
        self.server_name = socket.getfqdn(host)
        self.server_port = port

        # Headers set by FW/App
        self.headers_set = []

    # sets the application
    def set_app(self, application):
        self.application = application

    # run forever and ever
    def server_forever(self):
        listen_socket = self.listen_socket
        while True:
            # new client conn
            self.client_connection, client_address = listen_socket.accept()
            self.handle_one_request() # this will be defined in a moment dw

    def handle_one_request(self):
        # will handle only one request
        request_data = self.client_connection.recv(1024)
        self.request_data = request_data = request_data.decode('utf-8')

        # print formated data
        # print(''.join(f'< {line} \n' for line in request_data.splitlines()))
        # it'll basically print everything in one line, aka a for loop inside the print, not the most readable imo
        for line in request_data.splitlines():
            print(''.join(f'< {line} \n'))

        # env dictionary w/ req data
        env = self.get_environ()

        # Get back a result that will become the HTTP body and call our app
        result = self.application(env, self.start_response)

        # construct a response adn send to user
        self.finish_responsE(result)

    # Parses the request into lines and makes sure it's presented accordingly
    def parse_request(self,text):
        request_line = text.splitlines()[0]
        # CRLF
        request_line = request_line.strip('\r\n')
        # break request line into components and assign into the tuple
        (self.request_method,  # GET
         self.path,  # /hello
         self.request_version  # HTTP 1.1
         ) = request_line.split()

    def get_environ(self):
        # a dictionary :D
        env = {}

        # this section totally doesn't follow conventions so please clean it up
        # includes REQUIRED CGI VARIABLES
        env['REQUEST_METHOD'] = self.request_method  # GET
        env['PATH_INFO'] = self.path    # /hello
        env['SERVER_NAME'] = self.server_name   # localhost
        env['SERVER_PORT'] = str(self.server_port)  # 8888

        # includes REQUIRED WSGI VARIABLES
        env['wsgi.version'] = (1, 0)
        env['wsgi.url_scheme'] = 'http'
        env['wsgi.input'] = io.StringIO(self.request_data)  # not STDIN
        env['wsgi.errors'] = sys.stderr  # std error from system
        env['wsgi.multithread'] = False
        env['wsgi.multiprocess'] = False
        env['wsgi.run_once'] = False

        return env

    def start_response(self, status, response_headers, exc_info=None):
        # Server headers
        server_headers = [
            ('Date', 'Sat, 02 Nov 2024 5:33:22 GMT'),
            ('Server', 'WSGI Server 0.1')
        ]
        self.headers_set = [status, response_headers + server_headers]
        # WSGI spec says a start_response must return a 'write' callable
        # but we will ignore that ...for now (return self.finish_response)

    def finish_response(self, result):
        try:
            status, response_headers = self.headers_set
            # this will be sent to the client
            response = f'HTTP/1.1 {status}\r\n'
            # header in response headers will be wrtten info by info
            for header in response_headers:
                response += '{0}: {1}\r\n'.format(*header)
            response += '\r\n'
            for data in result:
                response += data.decode('utf-8')

            # print formatted resp data like curl does
            print(''.join(
                f'> {line} \n' for line in response.splitlines()
            ))
            # encode before sending for security
            response_bytes = response.encode()
            # PLEASE WORK FOR ALL LOVE
            self.client_connection.sendall(response_bytes)
        finally:
            self.client_connection.close()


# OUTSIDE THE CLASS

SERVER_ADDRESS = (HOST, PORT) = ('', 8888)

# start and make the server
def make_server(server_address, application):
    server = WSGIServer(server_address)
    server.set_app(application)
    return server

# this is the start point
if __name__ == '__main__':
    # if doesnt include an app, exits from the get-go
    if len(sys.argv) < 2:
        sys.exit('Provide a WSGI application as module:callable')

    # second arg, first one is program name like in C
    app_path = sys.argv[1]
    module, application = app_path.split(':')
    module = __import__(module)
    application = getattr(module, application)

    httpd = make_server(SERVER_ADDRESS, application)
    print(f'WSGI Running HTTP on port {PORT}...')
    httpd.server_forever()








