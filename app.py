# app.py
import streamlit as st
from utils import encrypt_file, generate_qr_code, decrypt_file_from_qr

st.set_page_config(page_title="Secure QR File Sharing", layout="centered")
st.title("🔐 Secure File Sharing with QR & AES Encryption")

menu = st.sidebar.selectbox("Choose", ["🔐 Encrypt & Generate QR", "🔓 Decrypt from QR"])

if menu == "🔐 Encrypt & Generate QR":
    uploaded_file = st.file_uploader("Upload File", type=None)
    key = st.text_input("Enter 16-byte Secret Key (AES)", type="password")
    if st.button("Encrypt & Generate QR"):
        if uploaded_file and len(key) == 16:
            file_data = uploaded_file.read()
            encrypted_data = encrypt_file(file_data, key.encode())
            qr_img = generate_qr_code(encrypted_data)
            st.image(qr_img, caption="Scan or Save This QR", use_column_width=True)
        else:
            st.error("Upload file and use 16-byte key.")

elif menu == "🔓 Decrypt from QR":
    qr_image = st.file_uploader("Upload QR Code Image", type=["png", "jpg", "jpeg"])
    key = st.text_input("Enter 16-byte Secret Key (AES)", type="password")
    if st.button("Decrypt & Download File"):
        if qr_image and len(key) == 16:
            try:
                file_bytes = decrypt_file_from_qr(qr_image, key.encode())
                st.success("✅ File Decrypted Successfully!")
                st.download_button("📥 Download File", data=file_bytes, file_name="decrypted_file", mime="application/octet-stream")
            except Exception as e:
                st.error(f"❌ Failed to decrypt: {str(e)}")
        else:
            st.error("Upload QR and enter a valid 16-byte key.")
