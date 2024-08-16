import socket
import struct

def calculate_checksum(data):
    return sum(data) & 0xFF

def parse_frame(frame):
    start_byte = frame[0]
    id_byte = frame[1]
    frame_length = struct.unpack('<H', frame[2:4])[0]
    command_class = frame[4]
    command_code = frame[5]
    data_package = frame[6:-2]
    checksum = frame[-2]
    end_byte = frame[-1]

    # Validate frame
    if start_byte != 0x02 or end_byte != 0x03:
        raise ValueError("Invalid start or end byte")
    if len(frame) != frame_length + 4:  # Frame length includes Command Class, Command Code, Checksum, and End Byte
        raise ValueError("Frame length mismatch")
    if calculate_checksum(frame[1:-2]) != checksum:  # Exclude start byte and end byte for checksum calculation
        raise ValueError("Checksum mismatch")

    return command_class, command_code, data_package

def create_response(command_class, command_code, data):
    # Define response frame start and end bytes
    start_byte = 0x02
    end_byte = 0x03
    id_byte = 0x01  # Assuming device ID is 1

    # Build data package
    data_package = bytearray(data)

    # Calculate frame length
    frame_length = len(data_package) + 4  # 4 bytes for Command Class, Command Code, Checksum, and End Byte
    frame_length_bytes = struct.pack('<H', frame_length)

    # Create frame
    frame = bytearray()
    frame.append(start_byte)
    frame.append(id_byte)
    frame.extend(frame_length_bytes)
    frame.append(command_class)
    frame.append(command_code)
    frame.extend(data_package)

    # Calculate checksum
    checksum = calculate_checksum(frame[1:])  # Exclude start byte for checksum calculation
    frame.append(checksum)
    frame.append(end_byte)

    return frame

def server(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print("Server listening on", host, port)
        
        while True:
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)
                while True:
                    frame = conn.recv(1024)  # Adjust the buffer size if necessary
                    if not frame:
                        break

                    try:
                        command_class, command_code, data_package = parse_frame(frame)
                        print(f"Received - Command Class: {command_class}, Command Code: {command_code}, Data: {data_package}")
                        
                        # Create a response (echo the received command)
                        response = create_response(command_class, command_code, [0x00])  # Example response data
                        conn.sendall(response)
                    except ValueError as e:
                        print(f"Frame parsing error: {e}")

# Example usage
host = '0.0.0.0'  # Listen on all interfaces
port = 25032

server(host, port)
