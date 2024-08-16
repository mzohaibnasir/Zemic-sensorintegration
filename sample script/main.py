import socket
import threading
import datetime
import time

# 定义服务器的主机和端口specify server host and port
HOST = '192.168.0.201'
PORT = 8234
#get parameter command
#hex_array = [0x02, 0x01, 0x04, 0x00, 0x51, 0x50, 0x03, 0x00, 0xa9, 0x03]
#get aisle weight command
# hex_array = [0x02, 0x01, 0x04, 0x00, 0x51, 0x50, 0x06, 0x00, 0xac, 0x03]
hex_array =[0x02, 0x01, 0x0B, 0x00 , 0x57 , 0x50 , 0x03 , 0x00 , 0x01 , 0x0A , 0x00 , 0x00 , 0x00 , 0x02 , 0x02 , 0xC5 , 0x03
]
#get loadcell weight command
#hex_array = [0x02, 0x01, 0x04, 0x00, 0x51, 0x50, 0x07, 0x00, 0xad, 0x03]
# 创建一个 TCP/IP socket Creat a TCP/IP socket
print("server ip:", HOST)
print("server port:", PORT)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 绑定服务器地址和端口 binding sever address and port
server_socket.bind((HOST, PORT))

# 开始监听传入的连接 Start listening coming connection
server_socket.listen(1)
print('Waiting for a client to connect...')

# 存储与客户端连接的socket列表 storage the socket list of connecting to clients
client_sockets = []


def handle_client(client_socket):
    while True:
        try:
            # 接收客户端发送的消息receive message from client
            msg = client_socket.recv(1024)
            time1 = datetime.datetime.now()
            if msg:
                # 广播消息给所有其他客户端broadcast the message to all clients
                #broadcast_message(msg, client_socket)

                #print(time1)
                # print("msg", msg)
                hex_a = list(msg)
                print("[ %s ] receive from %s : %s" % (time1, addr, hex_a))
                #time.sleep(0.01)
                response = bytes(hex_array)
                time2 = datetime.datetime.now()
                client_socket.sendall(response)
                print("[ %s ] send to client: %s" %(time2, response))
        except:
            # 发生异常时，移除客户端连接并关闭socket。 when there is error, remove client and close socket.
            index = client_sockets.index(client_socket)
            client_sockets.remove(client_socket)
            client_socket.close()

            break


def broadcast_message(msg, sender_socket):
    for client_socket in client_sockets:
        if client_socket != sender_socket:
            client_socket.sendall(msg.encode())


while True:
    # 等待客户端连接. wait for clients connection
    client_socket, addr = server_socket.accept()

    # print('与客户端 {0} 进行连接'.format(addr))
    print('Connecting with client {0}'.format(addr))


    # 将新连接的客户端加入到列表中 add new client to list
    client_sockets.append(client_socket)

    response = bytes(hex_array)
    # print(f"hex_array: {hex_array}")
    print("send to client:", hex_array)
    client_socket.sendall(response)
    # print("send to client:", hex_array)
    # 创建一个线程来处理该客户端的消息 creat a thread to handle message from clients
    thread = threading.Thread(target=handle_client, args=(client_socket,))
    thread.start()
