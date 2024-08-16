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
            0x02,  # start
            0x31,  # adressiD 
            0x51, # address class
            0x50, # command code
            0x01, 0x00, # parametrs
            0xc0, 0xa8, 0x01, 0x1b, 0xe7, 0x23,  # check
            0x03 # end
            ])  # Example command
        
        # hex_command = [2, 1, F, 0, 57, 50, 9, 31, 39, 31, 32, 30, 39, 31, 38, 35, 38, 30, 30, 2C, 3 ]

        hex_string = "02 01 0F 00 57 50 09 31 39 31 32 30 39 31 38 35 38 30 30 2C 03"



        byte_stream = bytes.fromhex(hex_string) 
        print(f"byte_stream: {byte_stream}")

        # byte_array = bytes(hex_command)


        # print(f"hex_command: {hex_command}")
        # print(f"byte_array: {byte_array}")

        # Send the command
        conn.sendall(command)
        print(f"Command sent.: {command}")

        # Receive response from client
        response = conn.recv(1024)  # Adjust buffer size if needed
        print(f"Received response: {response}")
























































        """
        To break down the byte stream `02 01 0F 00 57 50 09 31 39 31 32 30 39 31 38 35 38 30 30 2C 03` into its communication protocol components, we can typically identify the following parts:

1. **Start of Message (SOM)**: `02`
   - Indicates the beginning of the message.

2. **Command Type (or Message Type)**: `01`
   - Represents the specific command or action being requested. In this case, `01` might indicate a command for setting or retrieving information, depending on the protocol's definition.

3. **Length or Parameter Identifier**: `0F`
   - Indicates the length of the following data or a specific parameter related to the command. Here, `0F` (15 in decimal) might denote the length of the data section that follows.

4. **Reserved or Padding Byte**: `00`
   - This byte is often reserved for alignment, future extensions, or padding. It does not carry specific data for this command.

5. **Data Section**:
   - **`57 50`**: These bytes could represent a specific identifier or parameter related to the command. For example, `57` and `50` might represent `W` and `P` in ASCII, which could be part of the data payload or configuration parameters.
   - **`09`**: This byte could indicate a specific field or parameter. In this context, it might represent a delimiter or a length of a specific section within the data.
   - **`31 39 31 32 30 39 31 38 35 38 30 30 2C`**: These bytes represent the ASCII string `191209185800,` which appears to be a date-time stamp or another textual piece of information.
   
6. **End of Message (EOM)**: `03`
   - Indicates the end of the message.

### Breakdown:

- **Start of Message (SOM)**: `02`
- **Command Type**: `01`
- **Length/Parameter**: `0F`
- **Reserved/Padding**: `00`
- **Data Section**:
  - `57 50`: Possibly an identifier or specific data (ASCII: `WP`)
  - `09`: Specific field or delimiter
  - `31 39 31 32 30 39 31 38 35 38 30 30 2C`: ASCII string `191209185800,`
- **End of Message (EOM)**: `03`

In summary, the byte stream encodes a command with a specific type, includes a length indicator, and contains a data section with identifiers and information, ending with an end-of-message marker. The exact meaning of each byte depends on the specific communication protocol being used.

"""