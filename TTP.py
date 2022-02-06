from gf256 import GF256
import random
import socket


class TTP:
    def __init__(self):
        self.players = []
        self.plains: [[]] = None
        self.keys: [[]] = None

    def add_player(self, player: list):
        self.players.append((player[0], player[1]))

    def generate_shares(self, inputs, mode="plain"):
        if mode == "plain":
            self.plains = [[] for _ in range(len(self.players))]
        else:
            self.keys = [[] for _ in range(len(self.players))]

        for i in range(len(inputs)):
            shares = []
            for j in range(len(self.players) - 1):
                shares.append(GF256(random.randint(0, 255)))
            shares.append(inputs[i] - sum(shares, GF256(0)))

            for j in range(len(self.players)):
                if mode == "plain":
                    self.plains[j].append(shares.pop())
                else:
                    self.keys[j].append(shares.pop())

    def send_shares(self, mode="plain"):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            for i in range(len(self.players)):
                s.connect((self.players[i][0], self.players[i][1]))
                if mode == "plain":
                    for plain in self.plains[i]:
                        s.sendall(("P" + str(plain)).encode())
                else:
                    for key in self.keys[i]:
                        s.sendall(("K" + str(key)).encode())


if __name__ == "__main__":
    ttp = TTP()
    ttp.add_player(["localhost", 5001])
    ttp.add_player(["localhost", "5002"])
    # while True:
    #     player = input("please input play:  ").split(" ")
    #     # print(player)
    #     if len(player) != 2:
    #         break
    #     ttp.add_player(player)
    ttp.generate_shares([GF256(i) for i in range(16)], mode="plain")
    ttp.generate_shares([GF256(i) for i in range(16)], mode="key")
    ttp.send_shares(mode="plain")
    # ttp.send_shares(mode="key")
    print(ttp.plains)
    print(ttp.keys)
