import socket
server = socket.socket() 

server_ip = '192.168.0.201'  # Listen on all available interfaces
server_port = 8234  # Port to listen on

server.bind((server_ip, server_port)) 
server.listen(4) 
client_socket, client_address = server.accept()
print(client_address, "has connected")
while True:
    recvieved_data = client_socket.recv(1024)
    print(recvieved_data)