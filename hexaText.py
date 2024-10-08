import struct

# Byte string to be analyzed
byte_string = b'\x02\x81\x1b\xe7\x00A\x06\xca\x03\x02\x81\x1b\xe7\x00A\x06\xca\x03\x02\x81\x1b\xe7\x00A\x06\xca\x03\x02\x81\x1b\xe7\x00A\x06\xca\x03\x02\x81\x1b\xe7\x00A\x06\xca\x03\x02\x81\x1b\xe7\x00A\x06\xca\x03\x02\x81\x1b\xe7\x00A\x06\xca\x03\x02\x81\x1b\xe7\x00A\x06\xca\x03\x02\x81\x1b\xe7\x00A\x06\xca\x03\x02\x81\x1b\xe7\x00A\x06\xca\x03\x02\x81\x1b\xe7\x00A\x06\xca\x03\x02\x81\x1b\xe7\x00A\x06\xca\x03\x02\x81\x1b\xe7\x00A\x06\xca\x03\x02\x81\x1b\xe7\x00A\x06\xca\x03\x02\x81\x1b\xe7\x00A\x06\xca\x03\x02\x81\x1b\xe7\x00A\x06\xca\x03\x02\x81\x1b\xe7\x00A\x06\xca\x03\x02\x81\x1b\xe7\x00A\x06\xca\x03\x02\x81\x1b\xe7\x00A\x06\xca\x03\x02\x81\x1b\xe7\x00A\x06\xca\x03\x02\x81\x1b\xe7\x00A\x06\xca\x03\x02\x81\x1b\xe7\x00A\x06\xca\x03\x02\x81\x1b\xe7\x00A\x06\xca\x03\x02\x81\x1b\xe7\x00A\x06\xca\x03\x02\x81\x1b\xe7\x00A\x06\xca\x03\x02\x81\x1b\xe7\x00A\x06\xca\x03\x02\x81\x1b\xe7\x00A\x06\xca\x03\x02\x81\x1b\xe7\x00A\x06\xca\x03\x02\x81\x1b\xe7\x00A\x06\xca\x03\x02\x81\x1b\xe7\x00A\x06\xca\x03\x02\x81\x1b\xe7\x00A\x06\xca\x03\x02\x81\x1b\xe7\x00A\x06\xca\x03\x02\x81\x1b\xe7\x00A\x06\xca\x03'

# Example: Parse the byte string into chunks
# Adjust the format string based on your data structure
def parse_binary_data(data):
    # Example format string: '<B B H I' (Little-endian: 1 byte, 1 byte, 2 bytes, 4 bytes)
    # Adjust based on your data structure
    fmt = '<B B H I'
    size = struct.calcsize(fmt)
    
    # Extracting chunks
    for i in range(0, len(data), size):
        chunk = data[i:i+size]
        if len(chunk) < size:
            continue
        unpacked_data = struct.unpack(fmt, chunk)
        print(f'Chunk {i//size + 1}: {unpacked_data}')

# Call the function to parse and print the data
parse_binary_data(byte_string)
