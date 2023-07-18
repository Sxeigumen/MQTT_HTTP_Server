import socket
from email import parser

MAX_LINE = 64 * 1024
MAX_HEADER = 100


class Response:
    def __init__(self, status, reason, headers=None, body=None):
        self.status = status
        self.reason = reason
        self.headers = headers
        self.body = body


class Request:
    def __init__(self, method, uri, version, headers, rfile, ip):
        self.method = method
        self.uri = uri
        self.version = version
        self.headers = headers
        self.ip = ip
        self.rfile = rfile


class Request_message:
    def __init__(self, type, device, data, device_ip):
        self.type = type
        self.device = device
        self.device_ip = device_ip
        self.data = data


class Server:
    def __init__(self, ip, port, server_name):
        self.ip = ip
        self.port = port
        self.server_name = server_name

    def server_enable(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)

        try:
            server_socket.bind((self.ip, self.port))
            server_socket.listen()

            while True:
                new_socket, from_addr = server_socket.accept()
                self.socket = new_socket

                try:
                    self.server_client(new_socket)
                except Exception as e:
                    print('Client serving failed')
        finally:
            print('Server sucking cock')
            server_socket.close()

    def server_client(self, socket):
        try:
            request = self.parse_request(socket)
            response = self.handle_request(request)
            # self.send_response(socket, response)

        except ConnectionResetError:
            socket = None
        except Exception as e:
            self.send_error(socket, e)
        if socket:
            socket.close()

    def parse_request(self, socket: socket.socket):
        rfile = socket.makefile('rb')
        method, uri, version = self.parse_request_line(rfile)
        headers = self.parse_request_header(rfile)
        host = headers.get('Host')
        if version != 'HTTP/1.1' and version != 'HTTP/1.2':
            raise Exception(f'Unexpected HTTP version - {headers}')
        if not host:
            raise Exception('Bad request')
        if host not in (self.server_name, f'{self.ip}:{self.port}'):
            raise Exception(f'Not right connection - exected {self.ip}:{self.port} not {host}')
        return Request(method, uri, version, headers, rfile, headers.get('X-Forwarded-For'))

    def handle_request(self, request):
        print(request.headers, request.ip)

    def parse_request_header(self, rfile):
        headers = []
        while True:
            line = rfile.readline(MAX_LINE + 1)
            if len(line) > MAX_LINE:
                raise Exception('Header line is too long')
            if line in (b'\r\n', b'\n', b''):
                break
            headers.append(line)
            if len(headers) > MAX_HEADER:
                raise Exception('Too mane headers')
        headers_dict = b''.join(headers).decode('iso-8859-1')
        return parser.Parser().parsestr(headers_dict)

    def parse_request_line(self, rfile):
        raw = rfile.readline(MAX_LINE + 1)
        if len(raw) > MAX_LINE:
            raise Exception('Request line is too long')
        request_line = str(raw, 'iso-8859-1')
        request_line = request_line.rstrip('\r\n')
        words = request_line.split(' ')
        if len(words) != 3:
            raise Exception('Incorrect request line')
        return words


def main():
    server = Server('10.0.41.59', 10241, 'Opa')
    server.server_enable()


if __name__ == "__main__":
    main()