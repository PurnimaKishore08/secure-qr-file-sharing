from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from hashlib import sha256

def pad(data):
    return data + b"\0" * (AES.block_size - len(data) % AES.block_size)

def encrypt_file(file_path, password):
    key = sha256(password.encode()).digest()
    with open(file_path, 'rb') as f:
        data = f.read()
    data = pad(data)
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted = iv + cipher.encrypt(data)

    output_path = "encrypted_file.bin"
    with open(output_path, "wb") as ef:
        ef.write(encrypted)

    return output_path, key.hex()

def decrypt_file(file_path, password, key_hex):
    key = sha256(password.encode()).digest()
    if key.hex() != key_hex:
        return None

    with open(file_path, 'rb') as f:
        data = f.read()
    iv = data[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(data[AES.block_size:])
    decrypted = decrypted.rstrip(b"\0")

    output_path = "decrypted_output"
    with open(output_path, "wb") as df:
        df.write(decrypted)

    return output_path
