def pkcs7_pad(message, block_size):
    """
    Pads the message to be a multiple of block_size using PKCS#7 standard.
    """
    if isinstance(message, str):
        message = message.encode()

    # Calculate how many bytes we are short
    # Example: len=16, block=20 -> target_len=20, padding_needed=4
    padding_len = block_size - (len(message) % block_size)
    
    # SPECIAL CASE: If padding_len is 0 (already a multiple), 
    # we must add a full block of padding. 
    # (Usually handled automatically by the math above if modulo returns 0, 
    # but strictly speaking 16%16 is 0, so we want 16-0=16).
    if padding_len == 0:
        padding_len = block_size

    # Create the padding bytes
    # chr(4) * 4 becomes '\x04\x04\x04\x04'
    padding = bytes([padding_len] * padding_len)
    
    return message + padding

# --- Test Case ---
text = "YELLOW SUBMARINE"
padded = pkcs7_pad(text, 20)

print(f"Original: {text}")
print(f"Padded:   {padded}")
# To visualize the invisible bytes clearly:
print(f"Debug:    {padded.hex()}")