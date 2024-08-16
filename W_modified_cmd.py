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

# Utility function to unescape data
def unescape_data(data):
    unescaped = bytearray()
    i = 0
    while i < len(data):
        if data[i] == 0x1b:
            if data[i+1] == 0xe7:
                unescaped.append(0x02)
            elif data[i+1] == 0xe8:
                unescaped.append(0x03)
            elif data[i+1] == 0x00:
                unescaped.append(0x1b)
            i += 2
        else:
            unescaped.append(data[i])
            i += 1
    return bytes(unescaped)

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

# Utility function to parse a frame
def parse_frame(frame):
    start = frame[0]
    address = frame[1]
    length = struct.unpack('<H', frame[2:4])[0]
    command_class = frame[4]
    command_code = frame[5]
    data = frame[6:-2]
    checksum = frame[-2]
    end = frame[-1]

    # Verify checksum
    calculated_checksum = calculate_crc8(frame[1:-2])
    if calculated_checksum != checksum:
        raise ValueError("Invalid checksum")

    return address, command_class, command_code, data

# Function to build a response frame
def build_response(address, response_message):
    start = 0x02
    end = 0x03
    frame = bytearray()
    frame.append(start)
    frame.append(address)
    
    # Encode response message
    response_data = response_message.encode('utf-8')
    frame_length = 1 + 1 + len(response_data)  # Address + Data + Checksum
    frame.extend(struct.pack('<H', frame_length))
    
    # Command Class: 0x00 for universal response
    command_class = 0x00
    frame.append(command_class)
    
    # Data
    frame.extend(response_data)
    
    # Checksum
    checksum = calculate_crc8(frame[1:])  # Exclude start byte
    frame.append(checksum)
    
    # End byte
    frame.append(end)
    
    return bytes(frame)

def start_server(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(1)
        print(f"Server listening on {host}:{port}")

        while True:
            conn, addr = server_socket.accept()
            with conn:
                print(f"Connected by {addr}")
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    
                    try:
                        # Parse frame
                        address, command_class, command_code, payload = parse_frame(data)
                        
                        # Determine response based on command code
                        if command_code == 0x01:
                            response_message = "Getting data"
                        elif command_code == 0x02:
                            response_message = "Status OK"
                        else:
                            response_message = "Unknown command"
                        
                        # Build and send response frame
                        response_frame = build_response(address, response_message)
                        conn.sendall(response_frame)
                    
                    except ValueError as e:
                        print(f"Error: {e}")
                        # Send an error response
                        response_status = 0x00  # Checking error
                        response_frame = build_response(0xFF, "Error")
                        conn.sendall(response_frame)

if __name__ == "__main__":
    start_server('192.168.0.201', 8234)
