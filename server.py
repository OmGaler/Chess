import socket
host = "127.0.0.1"
port = 12345
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((host,port))
while True:
    s.listen(1)
    conn, addr = s.accept()
    data = conn.recv(2000)
    print(data.decode())
    
# import socket, select

# port = 12345
# socket_list = []
# users = {}
# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# server_socket.bind(('',port))
# server_socket.listen(5)
# socket_list.append(server_socket)
# while True:
    
    
    
    
    
    
    
    
#     ready_to_read,ready_to_write,in_error = select.select(socket_list,[],[],0)
#     for sock in ready_to_read:
#         if sock == server_socket:
#             connect, addr = server_socket.accept()
#             socket_list.append(connect)
#             connect.sendto(str(addr))

#             # connect.sendto("You are connected from:" + str.encode(addr))
#         else:
#             try:
#                 data = sock.recv(2048)
#                 if data.startswith("#"):
#                     users[data[1:].lower()]=connect
#                     print("User " + data[1:] + " added.")
#                     connect.sendto("Your user detail saved as : "+str.encode(data[1:]))
#                 elif data.startswith("@"):
#                     users[data[1:data.index(':')].lower()].sendto(data[data.index(':')+1:])
#             except:
#                 continue

# server_socket.close()