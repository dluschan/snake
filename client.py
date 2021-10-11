import network


class Player:
    def __init__(self):
        self.server = None
        self.s = None
        self.main()

    def send(self, msg):
        if self.s is None:
            self.s = network.Client()
        self.s.send(msg)

    def recv(self):
        if self.s is None:
            self.s = network.Client()
        return self.s.recv()

    def start(self):
        print(":D")

    def main(self):
        if input('Подключиться к серверу (yes(y)/no(n))?: ').lower() == 'y':
            print(self.recv())#Логиин
            self.send(input())
            print(self.recv())#Добро пожаловать
            print("Вход выполнен ")
            self.start()
        else:
            print('By!')
            exit(0)

player = Player()

