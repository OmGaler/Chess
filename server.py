import socket

host = "127.0.0.1"
port = 12345
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, port))
while True:
    s.listen(1)
    conn, addr = s.accept()
    data = conn.recv(2000)
    print(data.decode())
    break
