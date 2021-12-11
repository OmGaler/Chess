import socket
import pickle

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.server = "10.11.250.207"
        # self.server = "172.23.170.234"
        # self.server = "192.168.56.1"
        self.server = "0.0.0.0"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.id = self.connect()
        print(self.id)

    def getID(self):
        return self.id

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048*4).decode()
        except:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return pickle.loads(self.client.recv(2048*2))
        except socket.error as e:
            print(e)

n = Network()
