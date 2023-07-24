import socket
from email import parser
import mqtt_module
import time
import threading
from _thread import *
import logg

MAX_LINE = 64 * 1024
MAX_HEADER = 100

#Brocker info
broker_ip = '192.168.220.2'
port1 = 1883

#Client-Server info
topics = [
    ('gamedata', 1),
    ('instruction', 1)
]

#Сlient info
client_id = 'publish-1'
username = 'Kyala'
password = '123'

#Change to host IP
machine_ip = '10.0.41.64'


class Request:
    def __init__(self, method, uri, version, headers, rfile, ip):
        self.method = method
        self.uri = uri
        self.version = version
        self.headers = headers
        self.ip = ip
        self.rfile = rfile


class Request_message:
    def __init__(self, topic, info):
        self.topic = topic
        self.info = info

class Server:
    def __init__(self, ip, port, server_name):
        self.ip = ip
        self.port = port
        self.server_name = server_name
        self.client = mqtt_module.mqtt_unit(broker_ip, port1, client_id, topics, username, password)

    def mqtt_enable(self):
        self.client.connect()
        self.client.subscribe()
        self.client.client.loop_start()


    def server_enable(self):
        mqtt_thread = threading.Thread(target=self.mqtt_enable())
        mqtt_thread.start()

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)

        try:
            server_socket.bind((self.ip, self.port))
            server_socket.listen()

            while True:
                new_socket, from_addr = server_socket.accept()
                self.socket = new_socket
                logg.server_logger.info(f'Successful connection: {from_addr}')

                try:
                    self.server_client(new_socket)
                except Exception as e:
                    logg.server_logger.exception(f'Client serving failed {from_addr}')
                    #print('Client serving failed')
        finally:
            self.client.client.disconnect()
            self.client.client.loop_stop()
            #print('Server died')
            server_socket.close()
            logg.server_logger.exception(f'Server died')

    def server_client(self, socket):
        try:
            request = self.parse_request(socket)
            logg.server_logger.info(f'Successful request parsing')
            response = self.handle_request(socket, request)
            # self.send_response(socket, response)

        except ConnectionResetError:
            socket = None
            logg.server_logger.exception(f'Connection reset erorr')
        except Exception as e:
            logg.server_logger.exception(f'Erorr: {e}')
            self.send_error(socket, e)
        if socket:
            socket.close()

    def parse_request(self, socket: socket.socket):
        rfile = socket.makefile('rb')
        method, uri, version = self.parse_request_line(rfile)
        headers = self.parse_request_header(rfile)
        host = headers.get('Host')
        if version != 'HTTP/1.1' and version != 'HTTP/1.2':
            logg.server_logger.exception(f'Unexpected HTTP version')
            raise Exception(f'Unexpected HTTP version')
        if not host:
            logg.server_logger.exception(f'Bad request')
            raise Exception('Bad request')
        #if host not in (self.server_name, f'{self.ip}:{self.port}'):
            #logg.server_logger.exception(f'Not right connection: {host} != {self.server_name}, {self.ip}:{self.port}')
            #raise Exception(f'Not right connection')
        if host not in (self.server_name, f'{self.ip}', machine_ip):
            logg.server_logger.exception(f'Not right connection: {host} != {self.server_name}, {self.ip}, {machine_ip}')
            raise Exception(f'Not right connection')
        logg.server_logger.info(f'Request: {method}, {uri}, {version}, {headers}, {headers.get("X-Real-IP")}')
        return Request(method, uri, version, headers, rfile, headers.get('X-Real-IP'))

    def handle_request(self, socket, request):
        message_info = Request_message(request.headers.get('Topic'), request.headers.get('Info'))
        logg.server_logger.info(f'HTTP message: Topic: {message_info.topic}, Info: {message_info.info}')
        #print(message_info.topic, message_info.info)
        try:
            self.client.publish_message(message_info.topic, message_info.info)
            while True:
                if mqtt_module.global_message != "":
                    logg.server_logger.info(f'MQQT answer {mqtt_module.global_message}')
                    #print(mqtt_module.global_message)
                    break
            data = f'GET /device HTTP/1.1\r\n' \
            f'Host: {request.ip}\r\n' \
            f'Info: {mqtt_module.global_message} \r\n' \
            '\r\n'
            socket.sendall(bytes(data, encoding='utf-8'))
            mqtt_module.global_message = ""
        except:
            mqtt_module.global_message = ""
            logg.server_logger.exception(f'MQTT Error')
            #print('MQTT Error')

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
    #Change to docker container ip and port
    server = Server('192.168.220.4', 10101, 'proxy')
    server.server_enable()

if __name__ == "__main__":
    main()