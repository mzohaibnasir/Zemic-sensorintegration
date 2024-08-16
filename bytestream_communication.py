import socket

# Server settings
server_ip = '192.168.0.201'  # Listen on all available interfaces
server_port = 8234  # Port to listen on

# The low byte goes first, and high byte behind
# Create and bind the server socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((server_ip, server_port))
    server_socket.listen()

    print(f"Server listening on {server_ip}:{server_port}")

    # Accept a connection
    conn, addr = server_socket.accept()
    with conn:
        print(f"Connected by {addr}")

        # Define the command to send
        # command = bytes([
        #     0x02,  # start
        #     0x31,  # adressiD 
        #     0x51, # address class
        #     0x50, # command code
        #     0x01, 0x00, # parametrs
        #     0xc0, 0xa8, 0x01, 0x1b, 0xe7, 0x23,  # check
        #     0x03 # end
        #     ])  # Example command
        # command = [0x02, 0x01, 0x04, 0x00, 0x51, 0x50, 0x06, 0x00, 0xac, 0x03]

        command =[0x02, 0x01, 0x0B, 0x00 , 0x57 , 0x50 , 0x03 , 0x00 , 0x01 , 0x0A , 0x00 , 0x00 , 0x00 , 0x02 , 0x02 , 0xC5 , 0x03]

        # Send the command
        conn.sendall(bytes(command))
        print("send to client:", bytes(command))

        # Receive response from client
        response = conn.recv(1024)  # Adjust buffer size if needed
        print(f"Received response: {response}")