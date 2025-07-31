import streamlit as st

# ---------------------- STYLING ----------------------
st.set_page_config(page_title="Secure QR File Encryptor", layout="centered")

custom_css = """
<style>
/* Input & Password Field */
input, textarea, .stTextInput input {
    color: white !important;
    background-color: #1e1e1e !important;
    border: 1px solid #555 !important;
    border-radius: 8px !important;
    padding: 0.5em;
}

input::placeholder {
    color: #cccccc !important;
}
</style>

"""

st.markdown(custom_css, unsafe_allow_html=True)

import streamlit as st
import os
from encryption import encrypt_data, decrypt_data
from qr_utils import generate_qr, scan_qr

st.set_page_config(page_title="Secure File QR App", layout="centered")
st.title("🔐 Secure File Sharing via QR Code")

mode = st.sidebar.radio("Select Mode", ["Encrypt & Generate QR", "Scan QR & Decrypt"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

if mode == "Encrypt & Generate QR":
    uploaded_file = st.file_uploader("Upload a file to encrypt", type=None)
    password = st.text_input("Enter a password to encrypt", type="password")

    if uploaded_file and password:
        data = uploaded_file.read()
        encrypted_data, key_hex = encrypt_data(data, password)
        file_path = os.path.join(UPLOAD_DIR, uploaded_file.name + ".enc")

        with open(file_path, "wb") as f:
            f.write(encrypted_data)

        payload = f"{file_path}||{key_hex}"
        qr_path = generate_qr(payload)

        st.success("File encrypted successfully!")
        st.image(qr_path, caption="Scan this QR to decrypt", width=300)
        st.download_button("Download Encrypted File", encrypted_data, file_name=uploaded_file.name + ".enc")

elif mode == "Scan QR & Decrypt":
    qr_image = st.file_uploader("Upload QR image (from sender)", type=["png", "jpg", "jpeg"])
    password = st.text_input("Enter password to decrypt", type="password")

    if qr_image and password:
        with open("scanned_qr.png", "wb") as f:
            f.write(qr_image.read())

        payload = scan_qr("scanned_qr.png")
        if not payload:
            st.error("QR code not recognized.")
        else:
            try:
                file_path, key_hex = payload.split("||")
                with open(file_path.strip(), "rb") as f:
                    encrypted_data = f.read()
                decrypted_data = decrypt_data(encrypted_data, password, key_hex)
                st.success("✅ File decrypted successfully!")
                st.download_button("Download Decrypted File", decrypted_data, file_name="decrypted_file")
            except Exception as e:
                st.error(f"Decryption failed: {e}")
