import magic

def extract_file(carrier_data, start_position, length):
    
    #  Initialize an empty string to store the binary representation of the length
    binary_length = ""

    # Extract the binary representation of the length from the carrier data
    for i in range(32):  # Assuming length is represented by 32 bits
        binary_length += str(carrier_data[start_position + i])

    # Convert the binary length to an integer
    message_length = int(binary_length, 2)
    
     # Extract the message using the extracted length
    carrier_bytes =  bytes(carrier_data)
    cbinary = ''.join(format(byte, '08b') for byte in carrier_bytes)
    cbinarylist = list(cbinary)
    start_position = start_position * 8 * 1024
    
    extracted_message = []
    len_array = [length, length + 4, length + 8]
    k = 0
    for i in range(start_position + 32, len(cbinarylist)):
        if len(extracted_message) > message_length:
            break
        extracted_message.append(cbinarylist[i])
        if k == 3:
            k = 0 # reset to 0 to keep looping through len_array 
        i += len_array[k]
        k += 1

    new_cbinary = ''.join(extracted_message)
    bytes_list = bits_to_bytes(new_cbinary)
    return bytes_list


def bits_to_bytes(bits):
    # Pad the bit string to ensure its length is a multiple of 8
    bits += '0' * (8 - len(bits) % 8) if len(bits) % 8 != 0 else ''

    # Convert the bit string to bytes
    byte_list = [int(bits[i:i+8], 2) for i in range(0, len(bits), 8)]

    # Convert integers to bytes
    byte_string = bytes(byte_list)

    return byte_string
        

def determine_file_type(binary_data):
    # Use python-magic to determine the file type
    mime = magic.Magic(mime=True)
    file_type = mime.from_buffer(binary_data)
    return file_type