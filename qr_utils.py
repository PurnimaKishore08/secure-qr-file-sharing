# qr_utils.py
import qrcode
import cv2
import tempfile
import os
from PIL import Image

def generate_qr(data):
    img = qrcode.make(data)
    temp_path = os.path.join(tempfile.gettempdir(), "qr_code.png")
    img.save(temp_path)
    return temp_path

def decode_qr_from_image(image_file):
    img = Image.open(image_file)
    img_cv = cv2.cvtColor(cv2.imread(image_file.name), cv2.COLOR_BGR2GRAY)
    detector = cv2.QRCodeDetector()
    data, _, _ = detector.detectAndDecode(img_cv)
    return data if data else None
