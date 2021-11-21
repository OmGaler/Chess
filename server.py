import socket
from _thread import *

# server = "192.168.56.1"
server = "0.0.0.0"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(e)

s.listen(2)
print("Server started, waiting for connection")


def threadedClient(conn):
    reply = ""
    while True:
        try:
            data = conn.recv(2048*4)
            reply = data.decode("utf-8")
            if not data: #no data received
                print("Disconnected")
                break
            else:
                print("Received ", reply)
                print("Sending", reply)
            conn.sendall(str.encode(reply))
        except:
            break

while True:
    connection, address = s.accept()
    print("Connected to ", address)
    start_new_thread(threadedClient, (connection,))