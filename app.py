import streamlit as st
from encryption import encrypt_file, decrypt_file
from qr_utils import generate_qr, decode_qr_from_image
import os
from datetime import datetime

st.set_page_config(page_title="🔐 Secure QR File Sharing", layout="centered")

st.title("🔐 Secure File Sharing via QR Code & AES")
st.markdown("Upload a file, encrypt it with a password, and share it securely using a QR code.")

menu = ["🔒 Encrypt & Generate QR", "🔓 Decrypt File", "📤 Scan QR to Extract Password"]
choice = st.sidebar.selectbox("Navigation", menu)

UPLOAD_DIR = "uploaded"
ENCRYPTED_DIR = "encrypted"
DECRYPTED_DIR = "decrypted"
QR_DIR = "qr_codes"
for d in [UPLOAD_DIR, ENCRYPTED_DIR, DECRYPTED_DIR, QR_DIR]:
    os.makedirs(d, exist_ok=True)

if choice == "🔒 Encrypt & Generate QR":
    st.subheader("Step 1: Upload File and Enter Password")
    uploaded_file = st.file_uploader("Choose file to encrypt")
    password = st.text_input("Enter strong password", type="password")

    if uploaded_file and password:
        filename = uploaded_file.name
        file_path = os.path.join(UPLOAD_DIR, filename)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())

        encrypted_file_path = os.path.join(ENCRYPTED_DIR, f"enc_{filename}")
        encrypt_file(file_path, encrypted_file_path, password)
        st.success("File encrypted successfully.")

        qr_path = os.path.join(QR_DIR, f"{filename}_qr.png")
        generate_qr(password, qr_path)
        st.image(qr_path, caption="Share this QR securely")

        with open(encrypted_file_path, "rb") as f:
            st.download_button("⬇️ Download Encrypted File", f, file_name=f"enc_{filename}")

        with open(qr_path, "rb") as f:
            st.download_button("⬇️ Download QR Code", f, file_name=f"{filename}_qr.png")

elif choice == "🔓 Decrypt File":
    st.subheader("Step 2: Upload Encrypted File and Password")
    encrypted_file = st.file_uploader("Upload encrypted file")
    password = st.text_input("Enter password for decryption", type="password")

    if encrypted_file and password:
        enc_filename = encrypted_file.name
        enc_path = os.path.join(ENCRYPTED_DIR, enc_filename)
        with open(enc_path, "wb") as f:
            f.write(encrypted_file.read())

        output_filename = enc_filename.replace("enc_", "dec_")
        output_path = os.path.join(DECRYPTED_DIR, output_filename)

        try:
            decrypt_file(enc_path, output_path, password)
            st.success("Decryption successful.")

            with open(output_path, "rb") as f:
                st.download_button("⬇️ Download Decrypted File", f, file_name=output_filename)
        except Exception as e:
            st.error("Decryption failed. Invalid password or corrupted file.")

elif choice == "📤 Scan QR to Extract Password":
    st.subheader("Upload QR Code to Extract Password")
    qr_image = st.file_uploader("Upload QR code image (PNG, JPG)", type=["png", "jpg", "jpeg"])

    if qr_image:
        with open("temp_qr.png", "wb") as f:
            f.write(qr_image.read())

        result = decode_qr_from_image("temp_qr.png")
        if result:
            st.success(f"Password in QR: `{result}`")
        else:
            st.error("Could not read QR code. Try a clearer image.")
