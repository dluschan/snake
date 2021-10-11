import network


class Player:
    def __init__(self):
        self.server = None
        self.nc = None
        self.main()

    def send(self, msg):
        if self.nc is None:
            self.nc = network.Client()
        self.nc.send(msg)

    def recv(self):
        if self.nc is None:
            self.nc = network.Client()
        return self.nc.recv()

    def start(self):
        print(":D")

    def main(self):
        if input('Подключиться к серверу (yes(y)/no(n))?: ').lower() == 'y':
            print(self.recv())
            self.send(input())
            print(self.recv())
            self.start()
        else:
            print('By!')
            exit(0)


if __name__ == "__name__":
    player = Player()
