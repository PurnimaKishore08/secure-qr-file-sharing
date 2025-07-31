import qrcode
from pyzbar.pyzbar import decode
from PIL import Image

def generate_qr(data, filename="qr_code.png"):
    img = qrcode.make(data)
    img.save(filename)
    return filename

def decode_qr_from_image(image_path):
    img = Image.open(image_path)
    decoded = decode(img)
    if decoded:
        return decoded[0].data.decode("utf-8")
    return None
