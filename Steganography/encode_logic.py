
def get_binary_data(cfile):
    with open(cfile, "rb") as file:
        binary_data = file.read()       
    return binary_data


def embed_message(carrier_data, message_data, starting_bit, length):
    # get length of message file to store in carrier file (for extraction purpose)
    message_data_len = bin(len(message_data))[2:]
    
    # Pad the binary length with leading zeros to ensure it's 32 bits long
    padded_length = message_data_len.zfill(32)
    
    # Embed the padded binary length into the carrier data
    for i, bit in enumerate(padded_length):
        carrier_data[starting_bit + i] = int(bit)
    carrier_bytes =  bytes(carrier_data)
    
    cbinary = ''.join(format(byte, '08b') for byte in carrier_bytes)
    mbinary = ''.join(format(byte, '08b') for byte in message_data)
    
    cbinarylist = list(cbinary)
    mbinarylist = list(mbinary)

    index = 0
    starting_bit = starting_bit * 1024 * 8 # to convert to bits from kilobytes
    
    # start embedding 
    lenth_array = [length, length + 4, length + 8] # enhancement to change L during process
    k=0 
    for i in range(starting_bit + 32, len(cbinarylist)): # 32 bits has stored message length, hence skipping it.
        if index < len(mbinarylist):
            # Modify the Lth bit in the carrier with the corresponding bit from the message
            cbinarylist[i] = mbinarylist[index]
            if k == 3:
                k = 0 # to loop throught length array, to make the replacement length dynamic
            i += lenth_array[k] # read length value from list 
            k += 1 # move to next index of lenth_array
            index += 1
        else:
            break
      
    if index < len(mbinarylist):
        return False        
    new_cbinary = ''.join(cbinarylist)
    byte_string = bits_to_bytes(new_cbinary)
    return byte_string


def bits_to_bytes(bits):
    # Pad the bit string to ensure its length is a multiple of 8
    bits += '0' * (8 - len(bits) % 8) if len(bits) % 8 != 0 else ''

    # Convert the bit string to bytes
    byte_list = [int(bits[i:i+8], 2) for i in range(0, len(bits), 8)]

    # Convert integers to bytes
    byte_string = bytes(byte_list)

    return byte_string







    










    