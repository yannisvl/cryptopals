import base64

# Function to convert hex to base64
def hex_to_base64(hex_str):
    # Convert hex to bytes
    byte_data = bytes.fromhex(hex_str)
    # Encode bytes to base64
    base64_data = base64.b64encode(byte_data)
    # Convert base64 bytes to string
    return base64_data.decode('utf-8')

# Example usage
hex_string = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d" 
base64_string = hex_to_base64(hex_string)
print("Base64 Encoded String:", base64_string)


def xor_hex(hex1, hex2):
    # Convert hex strings to integers
    int1 = int(hex1, 16)
    int2 = int(hex2, 16)
    # XOR the integers
    xor_result = int1 ^ int2
    # Convert the result back to hex and remove the '0x' prefix
    return hex(xor_result)[2:]

# Example usage
hex1 = "1c0111001f010100061a024b53535009181c"
hex2 = "686974207468652062756c6c277320657965"
result = xor_hex(hex1, hex2)
print("XOR Result:", result)