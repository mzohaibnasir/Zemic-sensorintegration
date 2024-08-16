import socket

# Server settings
server_ip = '192.168.0.201'  # IP to listen on
server_port = 8234  # Port to listen on

"""
    command format : Hex
    response format : List(int)
"""

def byteStreamToHex(byte_stream):
    # Convert byte stream to hex string
    hex_string = byte_stream.hex().upper()
    # Format the hex string with spaces between bytes
    formatted_hex_string = ' '.join(hex_string[i:i+2] for i in range(0, len(hex_string), 2))
    return formatted_hex_string

def HexToByteStream(hex_str):
    # Remove any spaces from the hex string
    hex_str = hex_str.replace(' ', '')
    # Convert hex string to byte stream
    byte_stream = bytes.fromhex(hex_str)
    return byte_stream

def byteStreamToInt(byte_stream):
    return list(byte_stream)

# Create and bind the server socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((server_ip, server_port))
    server_socket.listen()

    print(f"Server listening on {server_ip}:{server_port}")

    # Accept a connection
    conn, addr = server_socket.accept()
    with conn:
        print(f"Connected by {addr}")

        get = "02 01 04 00 51 50 06 00 AC 03"  # Command to send
    
        byte_stream = HexToByteStream(get)
        print("byte_stream: ", byte_stream)

        # Send the command
        conn.sendall(byte_stream)
        print(f"Command sent: INT: {byteStreamToInt(byte_stream)}")
        print(f"Command sent: HEX: {byteStreamToHex(byte_stream)}")

        # Receive response from client
        response = conn.recv(1024)  # Adjust buffer size if needed
        print(f"Response: INT: {byteStreamToInt(response)}")
        print(f"Response: HEX: {byteStreamToHex(response)}")
# b'\x02\x01\x04\x00QP\x06\x00\xac\x03'


# print("\n\n\n\n bye", byteStreamToHex(b'\x02\x01\x04\x00QP\x06\x00\xac\x03'))