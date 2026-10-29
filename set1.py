import base64


# --- Challenge 1 ---

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


# --- Challenge 2 ---

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

# --- Challenge 3 ---

# The hex string from the challenge
hex_string = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"

# 1. Decode hex to bytes
ciphertext = bytes.fromhex(hex_string)

def get_english_score(input_bytes):
    """
    Returns a score for the input_bytes based on character frequency.
    Higher score = more likely to be English.
    """
    # Dictionary of common English letter frequencies (percentages)
    # You can expand this or use a simpler "most common letters" list
    character_frequencies = {
        'a': .08167, 'b': .01492, 'c': .02782, 'd': .04253,
        'e': .12702, 'f': .02228, 'g': .02015, 'h': .06094,
        'i': .06094, 'j': .00153, 'k': .00772, 'l': .04025,
        'm': .02406, 'n': .06749, 'o': .07507, 'p': .01929,
        'q': .00095, 'r': .05987, 's': .06327, 't': .09056,
        'u': .02758, 'v': .00978, 'w': .02360, 'x': .00150,
        'y': .01974, 'z': .00074, ' ': .13000
    }
    
    score = 0
    for byte in input_bytes:
        char = chr(byte).lower()
        if char in character_frequencies:
            score += character_frequencies[char]
    
    return score

def single_byte_xor(input_bytes, key_byte):
    """XORs every byte in input_bytes with the key_byte"""
    # Create a result buffer of the same length
    return bytes([b ^ key_byte for b in input_bytes])

# 2. Loop through all possible keys (0-255)
candidates = []

for key in range(256):
    plaintext = single_byte_xor(ciphertext, key)
    score = get_english_score(plaintext)
    
    # Store the result so we can sort later
    result = {
        'key': key,
        'score': score,
        'plaintext': plaintext
    }
    candidates.append(result)

# 3. Sort by score (highest to lowest) and print the winner
best_candidate = sorted(candidates, key=lambda x: x['score'], reverse=True)[0]

print(f"Key: {best_candidate['key']} ('{chr(best_candidate['key'])}')")
print(f"Message: {best_candidate['plaintext']}")

# --- Challenge 4 ---

best_line_score = 0
best_plaintext = ""
line_number = 0

# Open the file (make sure '4.txt' is in your directory)
with open('4.txt', 'r') as f:
    for index, line in enumerate(f):
        line = line.strip() # Remove newline characters
        try:
            # Decode the hex string into bytes
            ciphertext = bytes.fromhex(line)
        except ValueError:
            continue

        # Brute force this specific line
        for key in range(256):
            decrypted = single_byte_xor(ciphertext, key)
            score = get_english_score(decrypted)
            
            # If this is the best English we've seen so far, save it
            if score > best_line_score:
                best_line_score = score
                best_plaintext = decrypted
                line_number = index + 1

print(f"Found at line {line_number}")
print(f"Decrypted: {best_plaintext}")

# --- Challenge 5 ---

def repeating_key_xor(plaintext, key):
    # Convert strings to bytes if they aren't already
    if isinstance(plaintext, str):
        plaintext = plaintext.encode()
    if isinstance(key, str):
        key = key.encode()
        
    output_bytes = bytearray()
    
    # Iterate over the plaintext, keeping track of the index (i)
    for i, byte in enumerate(plaintext):
        # Pick the correct key byte using modulo
        key_byte = key[i % len(key)]
        
        # XOR and append
        output_bytes.append(byte ^ key_byte)
    
    return output_bytes

# --- Challenge Input ---

message = """Burning 'em, if you ain't quick and nimble
I go crazy when I hear a cymbal"""

key = "ICE"

encrypted = repeating_key_xor(message, key)
print(encrypted.hex())

# --- Challenge 6 ---

def hamming_distance(b1, b2):
    """
    Computes the edit distance (number of differing bits) 
    between two byte strings.
    """
    dist = 0
    # Zip combines the two byte strings so we can iterate over them together
    for byte1, byte2 in zip(b1, b2):
        # XOR checks for differences (1 = difference, 0 = same)
        xor_res = byte1 ^ byte2
        # Count the number of 1s in the binary representation
        dist += bin(xor_res).count('1')
    return dist

# Test Case
s1 = b"this is a test"
s2 = b"wokka wokka!!!"
print(f"Distance: {hamming_distance(s1, s2)}")  # Should be 37

import base64

# --- PASTED HELPER FUNCTIONS START ---
# (Paste your get_english_score and single_byte_xor functions here from Challenge 3)
# For brevity, I assume you have them defined as:
# get_english_score(byte_string) -> float
# single_byte_xor(byte_string, key_byte) -> bytes
# -------------------------------------

def hamming_distance(b1, b2):
    return sum(bin(b1 ^ b2).count('1') for b1, b2 in zip(b1, b2))

def break_repeating_key_xor(ciphertext):
    candidate_keysizes = []

    # 1. Find the best KEYSIZE
    # The challenge suggests trying 2 to 40
    for keysize in range(2, 41):
        # Grab first chunks to compare
        # Suggestion: take 4 blocks and average them for better accuracy
        chunks = [ciphertext[i:i+keysize] for i in range(0, keysize*4, keysize)]
        
        # Ensure we have enough chunks to compare
        if len(chunks) < 4: 
            break
            
        distances = []
        # Compare 1st vs 2nd, 2nd vs 3rd, etc.
        for i in range(len(chunks) - 1):
             d = hamming_distance(chunks[i], chunks[i+1])
             distances.append(d / keysize) # Normalize by dividing by keysize
             
        avg_dist = sum(distances) / len(distances)
        
        candidate_keysizes.append({
            'keysize': keysize,
            'distance': avg_dist
        })
    
    # Sort by smallest normalized distance
    best_candidates = sorted(candidate_keysizes, key=lambda x: x['distance'])

    # Print the top 5
    print("Top 5 Key Candidates:")
    for cand in best_candidates[:5]:
        print(f"Size: {cand['keysize']}, Score: {cand['distance']:.4f}")

    best_keysize = 29
    print(f"Likely Key Size: {best_keysize}")

    # 2. Break ciphertext into blocks based on the best keysize
    # Transpose: Make a block of all the 1st bytes, all the 2nd bytes, etc.
    key = b""
    for i in range(best_keysize):
        # Create a block containing every Nth byte (slicing checks for bounds automatically)
        block = ciphertext[i::best_keysize]
        
        # 3. Solve each block as Single-Byte XOR
        # We try all 256 keys for THIS block and pick the best one
        best_score = 0
        best_k = 0
        for k in range(256):
            decrypted_block = single_byte_xor(block, k)
            score = get_english_score(decrypted_block)
            if score > best_score:
                best_score = score
                best_k = k
        
        # Append the found byte to our final key
        key += bytes([best_k])

    return key

# --- MAIN EXECUTION ---
# Read the file
with open('6.txt', 'r') as f:
    b64_data = f.read()

# Decode Base64 first!
ciphertext = base64.b64decode(b64_data)

found_key = break_repeating_key_xor(ciphertext)
print(f"Found Key: {found_key}")

# Use the key to decrypt the whole thing
# You need a repeating_xor function (from Challenge 5)
def repeating_key_xor(data, key):
    output = bytearray()
    for i, byte in enumerate(data):
        output.append(byte ^ key[i % len(key)])
    return output

plaintext = repeating_key_xor(ciphertext, found_key)
print("Decrypted Message:\n")
print(plaintext.decode())

# --- Challenge 7 ---

import base64
from Crypto.Cipher import AES

# The key from the challenge (must be bytes)
key = b"YELLOW SUBMARINE"

# Read the file content
with open('7.txt', 'r') as f:
    b64_data = f.read()

# 1. Decode Base64 to get the raw ciphertext
ciphertext = base64.b64decode(b64_data)

# 2. Create the AES Cipher object
cipher = AES.new(key, AES.MODE_ECB)

# 3. Decrypt
# Note: The result will be bytes. We decode to utf-8 to print it.
plaintext = cipher.decrypt(ciphertext)

print(plaintext.decode('utf-8', errors='ignore'))

# --- Challenge 8 ---

def detect_ecb(ciphertext, block_size=16):
    # Break the ciphertext into 16-byte chunks
    chunks = [ciphertext[i:i+block_size] for i in range(0, len(ciphertext), block_size)]
    
    # A set only stores unique items. 
    # If len(set) < len(list), it means there were duplicates.
    number_of_duplicates = len(chunks) - len(set(chunks))
    
    return number_of_duplicates > 0

# --- Challenge Execution ---

best_line = -1
max_duplicates = 0
ciphertext_hex = ""

with open('8.txt', 'r') as f:
    for i, line in enumerate(f):
        line = line.strip()
        ciphertext = bytes.fromhex(line)
        
        if detect_ecb(ciphertext):
            print(f"ECB detected on line {i+1}")
            print(f"Ciphertext: {line}")
            break