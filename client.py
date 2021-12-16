import socket


turn = ["W", "B"]
host = "127.0.0.1"
port = 12345

while True:
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((host,port))
    st = turn[0]
    byt = st.encode() + "'s turn"
    s.send(byt)
    turn.reverse()
    break
