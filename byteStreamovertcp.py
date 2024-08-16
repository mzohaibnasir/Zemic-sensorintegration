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
        command = bytes([
            0x02, 0x31, 0x0d, 0x00, 0x51, 0x50, 0x02, 0xc0,
            0xa8, 0x01, 0x1b, 0xe8, 0x50, 0x1b, 0x00, 0xc0,
            0xa8, 0x01, 0x1b, 0xe7, 0x23, 0x03
            ])  # Example command

        # Send the command
        conn.sendall(command)
        print("Command sent.")

        # Receive response from client
        response = conn.recv(1024)  # Adjust buffer size if needed
        print(f"Received response: {response}")