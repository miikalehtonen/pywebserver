import socket
import json
from threading import Thread
from utils import format_request


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

        print("Server is running at http://{}:{}".format(self.host, self.port))

        self._socket_listener()

    def _socket_listener(self):
        # Start listening connections. All connections will be processed in another thread
        while True:
            # Establish a connection
            client, address = self._socket.accept()

            client_thread = Thread(target=self._serve_client, args=(client, address[0],))
            client_thread.start()

    def _serve_client(self, client, address):
        request_str = client.recv(1024).decode()
        request = format_request(request_str)

        # General bad request
        if 'error' in request:
            self._send_response(client, status=request['error'])
            return

        # Page not found; implement custom 404 response later
        if not request['target'] in self.routes:
            self._send_response(client, status=404)
            return

        print(f"{address} {request['method']} {request['target']}")

        # Call target function for requested page
        default_response = ('', 200, 'text/html')
        response = self.routes[request['target']](request)
        response, status_code, content_type = response + default_response[len(response):]

        self._send_response(client, response, status_code, content_type)

    def _send_response(self, client, content: str = '', status: int = 200, content_type: str = 'text/html'):
        response_headers = {
            'Content-Type': f'{content_type}; encoding=utf8',
            'Content-Length': len(content),
            'Connection': 'close',
        }

        response_proto = 'HTTP/1.1'
        response_status_text = 'OK'

        response_headers_raw = ''.join('%s: %s\r\n' % (k, v) for k, v in response_headers.items())
        response = f"{response_proto} {status} {response_status_text}\r\n{response_headers_raw}\r\n{content}"

        client.send(response.encode(encoding="utf-8"))
        client.close()

