import cv2
import qrcode

def read_qr_from_image(image_path: str):
    img = cv2.imread(image_path)
    detector = cv2.QRCodeDetector()
    data, bbox, _ = detector.detectAndDecode(img)
    return data if data else None
