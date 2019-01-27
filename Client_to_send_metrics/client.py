import socket
import time


class ClientError(socket.error):
    """Общий класс исключений клиента"""
    pass


class Client:

    def __init__(self, host, port, timeout=None):
        '''Конструктор'''
        self.host = host
        self.port = port
        self.timeout = timeout

    def put(self, metric_name, metric_value, timestamp=int(time.time())):
        '''Метод put принимает первым аргументом название метрики, вторым численное
        значение, третьим - необязательный именованный аргумент timestamp. Метод put
        не возвращает ничего в случае успешной отправки и выбрасывает исключение
        ClientError в случае неуспешной.
        '''
        with socket.create_connection((self.host, self.port), self.timeout) as sock:
            try:
                sock.sendall(f'put {metric_name} {metric_value} {timestamp}\n'.encode('utf-8'))
                sock.recv(2048)
            except socket.error:
                raise ClientError

    def get(self, metric_name):
        '''Метод get принимает первым аргументом имя метрики, значения которой мы хотим
        выгрузить. Также вместо имени метрики можно использовать символ *, о котором
        говорилось в описании протокола. Метод get возвращает словарь с метриками
        в случае успешного получения ответа от сервера и выбрасывает исключение
        ClientError в случае неуспешного.
        '''
        data = {}
        with socket.create_connection((self.host, self.port), self.timeout) as sock:
            try:
                sock.sendall(f'get {metric_name}\n'.encode('utf-8'))
            except socket.error:
                raise ClientError
            server_data = sock.recv(1024).decode('utf-8').strip().split('\n')
        if server_data[0] == 'error':
            raise ClientError
        if len(server_data) == 1:
            return data
        else:
            for line in server_data[1:]:
                line = line.split()
                if line[0] not in data:
                    data[line[0]] = []
                data[line[0]].append((int(line[2]), float(line[1])))
                data[line[0]].sort(key=lambda x: x[0])
        if metric_name == '*':
            return data
        else:
            return {metric_name: data[metric_name]}
