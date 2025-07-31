# utils.py
import base64
import cv2
import numpy as np
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import qrcode

# Encrypt file
def encrypt_file(file_data, key):
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(file_data)
    return cipher.nonce + tag + ciphertext

# Generate QR code from encrypted file
def generate_qr_code(encrypted_data):
    encoded_data = base64.b64encode(encrypted_data).decode()
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M)
    qr.add_data(encoded_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img

# Decode QR using OpenCV and decrypt
def decrypt_file_from_qr(uploaded_image, key):
    file_bytes = np.asarray(bytearray(uploaded_image.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    detector = cv2.QRCodeDetector()
    data, _, _ = detector.detectAndDecode(img)

    if not data:
        raise ValueError("No QR code found or unreadable.")

    encrypted_data = base64.b64decode(data)
    nonce = encrypted_data[:16]
    tag = encrypted_data[16:32]
    ciphertext = encrypted_data[32:]
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    return cipher.decrypt_and_verify(ciphertext, tag)
