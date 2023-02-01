from socket_webserver import Socketserver
import json

server = Socketserver()

server.host = '0.0.0.0'
server.port = 8080


def index():
    return json.dumps({'Test value': 2}), 200, "application/json"


def home():
    return "<h1>This text is big</h1><p>This is small</p>", 200, "text/html"


routes = {
    '/': index,
    '/home': home
}
server.routes = routes

server.run()
