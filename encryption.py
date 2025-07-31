# encryption.py
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import os
import base64

UPLOAD_DIR = "uploads"

def encrypt_file(file, password):
    key = password.encode('utf-8').ljust(32, b'0')[:32]  # Ensure 32 bytes for AES-256
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)

    data = file.read()
    ct_bytes = cipher.encrypt(pad(data, AES.block_size))

    filename = os.path.join(UPLOAD_DIR, "encrypted_" + file.name)
    with open(filename, 'wb') as f:
        f.write(iv + ct_bytes)

    return filename, password

def decrypt_file(file, password):
    key = password.encode('utf-8').ljust(32, b'0')[:32]
    data = file.read()
    iv = data[:16]
    ct = data[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)

    filename = os.path.join(UPLOAD_DIR, "decrypted_" + file.name)
    with open(filename, 'wb') as f:
        f.write(pt)

    return filename

