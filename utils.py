# Parse client's raw http request
def format_request(request_str: str):
    request = {}
    lines = request_str.split('\r\n')

    # Check if request start line is in correct format:
    start_line = lines[0].split()
    if len(start_line) != 3:
        return {'error': 400}  # Return invalid request

    request['method'] = start_line[0]
    request['target'] = start_line[1]

    return request
