from re import X
import socket
import struct

# Utility function to calculate CRC8 checksum
def calculate_crc8(data):
    crc = 0
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x80:
                crc = (crc << 1) ^ 0x07
            else:
                crc <<= 1
    return crc & 0xFF

# Utility function to escape data
def escape_data(data):
    escaped = bytearray()
    for byte in data:
        if byte == 0x02:
            escaped.extend([0x1b, 0xe7])
        elif byte == 0x03:
            escaped.extend([0x1b, 0xe8])
        elif byte == 0x1b:
            escaped.extend([0x1b, 0x00])
        else:
            escaped.append(byte)
    return bytes(escaped)

# Utility function to build a frame
def build_frame(address, command_class, command_code, data):
    frame = bytearray()
    start = 0x02
    end = 0x03
    frame.append(start)
    
    # Address
    frame.append(address)
    
    # Frame Length
    length = 1 + 1 + 1 + len(data)  # Address + Command Class + Command Code + Data
    frame.extend(struct.pack('<H', length))
    
    # Command Class
    frame.append(command_class)
    
    # Command Code
    frame.append(command_code)
    
    # Data
    frame.extend(data)
    
    # Checksum
    checksum = calculate_crc8(frame[1:])  # Exclude start byte
    frame.append(checksum)
    
    # End byte
    frame.append(end)
    
    return bytes(frame)

# Function to send a command to the TCP client
def send_command(client_ip, client_port, server_ip, server_port, address, command_class, command_code, data):
    # Establish connection to the server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((server_ip, server_port))
        
        # Build and send frame
        frame = build_frame(address, command_class, command_code, data)
        s.sendall(frame)
        
        # Receive response
        response = s.recv(1024)  # Buffer size is 1024 bytes
        return response

# Example usage
if __name__ == "__main__":
    # Define parameters
    client_ip = '192.168.0.7'
    client_port = 80
    server_ip = '192.168.0.201'
    server_port = 8234
    address = 0x01  # Example address
    command_class = 0x01  # Example command class
    command_code = 0x01  # Example command code
    data = bytearray([0x01, 0x02, 0x03])  # Example data

    # Send command and receive response
    response = send_command(client_ip, client_port, server_ip, server_port, address, command_class, command_code, data)
    
    print("Received response:", response)
