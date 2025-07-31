import streamlit as st
from utils import encrypt_file, generate_qr_code, decrypt_file_from_qr
import os

st.set_page_config(page_title="Secure QR File Sharing", layout="centered")
st.title("🔐 Secure File Sharing with QR Code + AES Encryption")

st.markdown("---")

# Encrypt and generate QR
st.header("📤 Upload & Encrypt File")
uploaded_file = st.file_uploader("Upload a file", type=["txt", "pdf", "png", "jpg", "jpeg", "csv", "docx"])

if uploaded_file:
    key = st.text_input("Enter a secret key for encryption 🔑", type="password")
    if st.button("Encrypt & Generate QR"):
        if not key:
            st.warning("Please enter a secret key.")
        else:
            file_path = os.path.join("uploads", uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            encrypted_path, qr_path = encrypt_file(file_path, key)
            st.success("File encrypted successfully!")
            st.image(qr_path, caption="Scan this QR to decrypt", use_column_width=True)

st.markdown("---")

# Decrypt from QR
st.header("📥 Decrypt File from QR Code")
qr_uploaded = st.file_uploader("Upload QR Code Image", type=["png", "jpg", "jpeg"], key="decrypt")

if qr_uploaded:
    dec_key = st.text_input("Enter the secret key used during encryption 🔑", type="password", key="dec")
    if st.button("Decrypt File"):
        if not dec_key:
            st.warning("Please enter the decryption key.")
        else:
            with open("qr_temp.png", "wb") as f:
                f.write(qr_uploaded.getbuffer())
            output = decrypt_file_from_qr("qr_temp.png", dec_key)
            if output:
                st.success("File decrypted successfully!")
                with open(output, "rb") as file:
                    btn = st.download_button(
                        label="📥 Download Decrypted File",
                        data=file,
                        file_name=os.path.basename(output),
                        mime="application/octet-stream"
                    )
            else:
                st.error("Decryption failed. Invalid QR or wrong key.")
