import socket
import sys
from Utility import INPUTS_LENGTH


class Player:
    def __init__(self, port, address):
        self.port = int(port)
        self.address = address
        self.multiple: [[]] = []
        self.plains: [] = []
        self.keys: [] = []

    def receive(self):
        """
        接收其他player的z的分片
        :return:
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.address, self.port))
            s.listen(1)
            conn, addr = s.accept()
            with conn:
                i = INPUTS_LENGTH
                while i != 0:
                    data = conn.recv(18).decode()
                    if data[0] == "P":
                        self.plains.append(data[1:])
                    else:
                        self.keys.append(data[1:])
                    i -= 1

        print(self.plains)
        print(self.keys)

    def send(self):
        """
        发送z的分片
        :return:
        """
        pass

    def process(self):
        """
        计算z的分片
        :return:
        """


if __name__ == "__main__":
    args = sys.argv
    # player = Player(args[2], args[1])
    player = Player("5001", "localhost")
    player.receive()
    # player.receive()
