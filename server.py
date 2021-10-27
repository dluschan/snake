from network import Server
from json import dumps
from socket import timeout
from game import Game


class GameServer:

    def __init__(self):
        self.clients = []
        self.logins = []
        self.games = []
        self.server = Server()
        self.main()

    def main(self):
        while True:
            try:
                self.accept()
                self.logins.append(self.recv(self.clients[0][0]))
                print(self.logins)
                self.sendAll(dumps((0, self.games, self.logins)))
            except timeout:
                print('Клиент не отвечает')
                continue

    def game_loop(self):
        self.game = Game(self)
        self.game.update()
        while not self.game.game_over:
            command = self.recv(self.clients[0][0])
            if command == 'u':
                self.game.up()
            elif command == 'l':
                self.game.left()
            elif command == 'd':
                self.game.down()
            elif command == 'r':
                self.game.right()

    def accept(self):
        self.clients.append(self.server.accept())

    def send(self, client, msg):
        self.server.send(self.clients[0][0], msg)

    def sendAll(self, msg):
        for client in self.clients:
            self.send(client, msg)

    def recv(self, conn):
        return self.server.recv(conn)


if __name__ == "__main__":
    lobby = GameServer()
