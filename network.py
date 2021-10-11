from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR


class Connection:
    timeout = 5
    address = '127.0.0.1'
    port = 1234
    players = 2
    coding = 'utf-8'


class Client:
    """Сетевая часть клиента.
    Занимается созданием и подключением сокета, а также отправкой и получением сообщений через него."""
    def __init__(self):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.connect((Connection.address, Connection.port))

    def send(self, msg):
        """Отправка сообщения на сервера"""
        self.socket.send(msg.encode(Connection.coding))

    def recv(self, size = 1024):
        """Получение сообщения заданного размера от сервера"""
        return self.socket.recv(size).decode(Connection.coding)


class Server:
    """Сетевая часть сервера.
    Занимается созданием сокета, установлением связи с клиентами, а также и получением и отправкой им сообщений."""
    def __init__(self):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.settimeout(Connection.timeout)
        self.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.socket.bind((Connection.address, Connection.port))
        self.socket.listen(Connection.players)

    def accept(self):
        """Установление связи с клиентом"""
        return self.socket.accept()

    def send(self, conn, msg):
        """Отправка сообщения на клиент"""
        conn.send(msg.encode(Connection.coding))

    def recv(self, conn, size=1024):
        """Получение сообщения заданного размера от клиента"""
        return conn.recv(size).decode(Connection.coding)
