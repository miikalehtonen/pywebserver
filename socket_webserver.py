import socket
import json
from threading import Thread


class Socketserver:
    def __init__(self, host: str = '0.0.0.0', port: int = 8080):
        self.host = host
        self.port = port
        self.routes = {}

        self._socket = ...

    def run(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.bind((self.host, self.port))
        self._socket.listen(1)

        print("Server is running at {}:{}".format(self.host, self.port))

        self._socket_listener()

    def _socket_listener(self):
        while True:
            # Establish a connection
            client, address = self._socket.accept()

            client_thread = Thread(target=self._serve_client, args=(client,))
            client_thread.start()

            print("Got a connection from %s" % str(address))

    def _serve_client(self, client):
        response_content = ''
        status_code = 200
        content_type = 'text/html'

        request_str = client.recv(1024).decode()
        request = _format_request(request_str)

        if request['target'] in self.routes:
            response_content = self.routes[request['target']]()
            if len(response_content) == 3:  # In case where status code was provided
                response_content, status_code, content_type = response_content
            elif len(response_content) == 2:
                response_content, status_code = response_content

        response_headers = {
            'Content-Type': f'{content_type}; encoding=utf8',
            'Content-Length': len(response_content),
            'Connection': 'close',
        }

        response_headers_raw = ''.join('%s: %s\r\n' % (k, v) for k, v in response_headers.items())

        response_proto = 'HTTP/1.1'
        response_status = status_code
        response_status_text = 'OK'  # this can be random

        response = f"{response_proto} {response_status} {response_status_text}\r\n{response_headers_raw}\r\n{response_content}"
        client.send(response.encode(encoding="utf-8"))

        client.close()


# Parse client's raw http request
def _format_request(request_str: str):
    request = {}
    lines = request_str.split('\r\n')

    # Check if request start line is in correct format:
    start_line = lines[0].split()
    if len(start_line) != 3:
        return False  # Return invalid request

    request['method'] = start_line[0]
    request['target'] = start_line[1]

    return request
