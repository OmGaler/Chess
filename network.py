# import socket


# class Network:
#     def __init__(self):
#         self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.server = "172.30.192.1"
#         self.port = 5555
#         self.addr = (self.server, self.port)
#         self.player = self.connect()

#     def getPlayer(self):
#         return self.player

#     def connect(self):
#         try:
#             self.client.connect(self.addr)
#             return self.client.recv(2048).decode()
#         except:
#             pass

#     def send(self, data):
#         try:
#             self.client.send(str.encode(data))
#             return self.client.recv(2048).decode()
#         except socket.error as e:
#             print(e)