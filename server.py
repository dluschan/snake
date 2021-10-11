import network
import socket
import game


class Lobby:
    def __init__(self):
        self.clients = []
        # [(conn, addr)]
        self.server = network.Server()
        self.main()

    def main(self):
        ans = ''
        while ans != 'q':
            print('a - установить соединение с новым клиентом')
            print('s - начать игру')
            print('q - quit')
            ans = input('Введите команду(a/w/s/q): ')
            if ans == 'a':
                try:
                    self.accept()
                except socket.timeout:
                    print('Клиент не отвечает')
                    continue
            elif ans == 's':
                game.Game()
            elif ans == 'q':
                print('By!')
                exit(0)
            else:
                print('Команда не распознана')

    def accept(self):
        self.clients.append(self.server.accept())
        print('Установлена связь с клиентом', self.clients[-1][1][1])
        self.send((self.clients[-1][0]), 'Введите ваш логин:')
        s = self.recv(self.clients[-1][0])
        print('Clients Login = ' + s)
        self.send(self.clients[-1][0], 'Добро пожаловать ' + s)

    def send(self, conn, msg):
        self.server.send(conn, msg)

    def recv(self, conn):
        return self.server.recv(conn)


if __name__ == "__name__":
    lobby = Lobby()
