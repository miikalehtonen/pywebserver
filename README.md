# pywebserver
A Python webserver made almost completely from scratch using just the socket library. This does not require any module installations to run.

**Note**:  This is an experimental project only and should not be used for actual web projects. For actual projects, use Django, Flask, etc.

## Features
Currently supports just basic things. More features are coming later.
- Simple paging system
- Ability to handle different request methods (GET, POST, PUT, DELETE)
- Return any content-type and HTTP status code
- Custom host and port
## Usage/Example
You can either use 'main.py' demo script or build your own

**main.py:**


```python
from socket_webserver import Socketserver
import json

# Creating server instance
server = Socketserver()

# Configuring host and port
server.host = '127.0.0.1'
server.port = 8080


""" Two example functions to return response. Upper one returns simple html response and lower one returns json response
    You could create something like views.py for handler functions and urls.py for routes
    'request' contains dictionary of all the request arguments currently supported """


def home(request):
    html = '''
    <h1>This text is big</h1>
    <p>This is small</p>    
    '''
    return html, 200, "text/html"


def demo(request):
    data = {
        'name': 'Custom api endpoint made with pywebserver',
        'target': request['target'],
        'data': [x * 2 for x in range(30)]
    }
    return json.dumps(data), 200, "application/json"


routes = {
    '/': home,
    '/home': demo
}

server.routes = routes  # Apply routes for server
server.run()

```

