import asyncio


server_data = {}


def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(
        ClientServerProtocol,
        host,
        port
        )
    server = loop.run_until_complete(coro)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


class ClientServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        resp = self.process_data(data.decode())
        self.transport.write(resp.encode())

    def process_data(self, data):
        '''Парсит входящее сообщение от клиента'''
        command, metrics = data.split(' ', 1)
        if command == 'put':
            return self.put(metrics)
        elif command == 'get':
            return self.get(metrics)
        else:
            return 'error\nwrong command\n\n'

    @staticmethod
    def put(data):
        '''Парсит метрики и записывает их в хранилище сервера'''
        metric_name, metric_value, timestamp = data.split()
        if metric_name not in server_data:
            server_data[metric_name] = []
            server_data[metric_name].append((metric_value, timestamp))
        else:
            server_data[metric_name].append((metric_value, timestamp))
        return 'ok\n\n'

    @staticmethod
    def get(data):
        '''Отправляет клиенту строку с метриками из хранилища сервера'''
        metric_name = data.strip()
        if metric_name == '*':
            answer = 'ok\n'
            for name_metric in server_data:
                for about_metric in server_data[name_metric]:
                    answer += f'{name_metric} {about_metric[0]} {about_metric[1]}\n'
            answer += '\n'
            return answer
        else:
            metric = server_data.get(metric_name)
            if metric:
                answer = 'ok\n'
                for about_metric in metric:
                    answer += f'{metric_name} {about_metric[0]} {about_metric[1]}\n'
                answer += '\n'
                return answer
            else:
                return 'ok\n\n'


if __name__ == '__main__':
    run_server('127.0.0.1', 8888)
