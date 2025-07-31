from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2

def pad(data):
    pad_len = 16 - len(data) % 16
    return data + bytes([pad_len]) * pad_len

def unpad(data):
    return data[:-data[-1]]

def encrypt_data(data, password):
    salt = get_random_bytes(16)
    key = PBKDF2(password, salt, dkLen=32, count=100000)
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(pad(data))
    return salt + iv + encrypted, key.hex()

def decrypt_data(enc_data, password, key_hex):
    salt = enc_data[:16]
    iv = enc_data[16:32]
    ct = enc_data[32:]
    key = bytes.fromhex(key_hex)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ct))
