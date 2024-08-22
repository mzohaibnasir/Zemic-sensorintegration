# handle -ve values 

import socket
import threading
import datetime
import struct

# Specify server host and port
HOST = '192.168.0.129'
PORT = 8235

# Commands
GET_WEIGHT = [0x02, 0x01, 0x04, 0x00, 0x51, 0x50, 0x06, 0x00, 0xac, 0x03]
TARE = [0x02, 0x01, 0x04, 0x00, 0x57, 0x50, 0x06, 0x00, 0xB2, 0x03]

getweight_counter = 0

def hexArrayToByteStream(hex_array):
    return bytes(hex_array)

def decode_weight(weight_bytes):
    # Interpret bytes as a signed 32-bit integer
    weight = struct.unpack('<i', bytes(weight_bytes))[0]
    weight_in_grams = weight * 0.1
    return weight_in_grams

def send_command_and_handle_response(client_socket, command):
    global getweight_counter
    print(f"getweight_counter: {getweight_counter}")
    
    response = hexArrayToByteStream(command)
    client_socket.sendall(response)
    
    msg = client_socket.recv(1024)
    time1 = datetime.datetime.now()
    
    if msg:
        hex_a = list(msg)
        print(f'hex_a: {hex_a} --weight 0: {decode_weight(hex_a[8:-2][1:5])}, weight 1: {decode_weight(hex_a[8:-2][-4:])}')
        print("continuous...")
    
    if command == GET_WEIGHT:
        getweight_counter += 1

def handle_client(client_socket):
    global getweight_counter
    
    while True:
        try:
            if getweight_counter >= 3600:  # Adjusted to 30 for demonstration
                print("Performing tare operation...")
                send_command_and_handle_response(client_socket, TARE)
                getweight_counter = 0
            
            send_command_and_handle_response(client_socket, GET_WEIGHT)
            
        except Exception as e:
            print(f"Error: {e}")
            if client_socket in client_sockets:
                client_sockets.remove(client_socket)
            client_socket.close()
            break

# The rest of your code remains the same
print("server ip:", HOST)
print("server port:", PORT)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(2)
print('Waiting for client connection...')

client_sockets = []

while True:
    client_socket, addr = server_socket.accept()
    print('Connecting to client {0}'.format(addr))
    client_sockets.append(client_socket)
    
    send_command_and_handle_response(client_socket, GET_WEIGHT)
    print("Initial")
    
    thread = threading.Thread(target=handle_client, args=(client_socket,))
    thread.start()

