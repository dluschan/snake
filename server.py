from network import Server
from socket import timeout
from game import Game


class GameServer:

    def __init__(self):
        self.clients = []
        self.games = []
        self.server = Server()
        self.main()

    def main(self):
        while True:
            try:
                self.accept()
                self.game_loop()
            except timeout:
                print('Клиент не отвечает')
                continue

    def game_loop(self):
        self.game = Game(self)
        self.game.update()
        while not self.game.game_over:
            command = self.recv(self.client[0])
            if command == 'u':
                self.game.up()
            elif command == 'l':
                self.game.left()
            elif command == 'd':
                self.game.down()
            elif command == 'r':
                self.game.right()

    def accept(self):
        self.client = self.server.accept()

    def send(self, msg):
        self.server.send(self.client[0], msg)

    def recv(self, conn):
        return self.server.recv(conn)


if __name__ == "__main__":
    lobby = Lobby()
