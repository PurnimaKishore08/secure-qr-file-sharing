import qrcode
import cv2

def generate_qr(data_string, filename='qr.png'):
    img = qrcode.make(data_string)
    img.save(filename)
    return filename

def scan_qr(image_path):
    detector = cv2.QRCodeDetector()
    img = cv2.imread(image_path)
    data, _, _ = detector.detectAndDecode(img)
    return data
