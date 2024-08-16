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
                    print("Getting in")

                    data = conn.recv(1024)
                    print("Data available")

                    if not data:
                        print("No data available")
                        break
                        
                    # Parse frame
                    address, command_class, command_code, data = parse_frame(data)

                    # Process frame here

                    # Echo the received frame
                    conn.sendall(data)
                print("Getting out")


if __name__ == "__main__":
    start_server('192.168.0.201', 8234)