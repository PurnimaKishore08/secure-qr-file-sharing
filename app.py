# app.py
import streamlit as st
from encryption import encrypt_file, decrypt_file
from qr_utils import generate_qr, decode_qr_from_image
import os
import base64

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

st.set_page_config(page_title="Secure QR File Sharing", layout="centered")
st.title("🔐 Secure File Sharing using QR & AES Encryption")

menu = ["Encrypt File", "Decrypt File"]
choice = st.sidebar.selectbox("Select Action", menu)

if choice == "Encrypt File":
    st.subheader("🔒 Encrypt File")

    uploaded_file = st.file_uploader("Upload any file", type=None)
    password = st.text_input("Enter Password", type="password")

    if uploaded_file and password:
        output_path, key = encrypt_file(uploaded_file, password)
        st.success("File encrypted successfully!")

        # Save and show QR
        qr_path = generate_qr(key)
        st.image(qr_path, caption="🔑 QR Code with Encryption Key")

        with open(output_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
            href = f'<a href="data:application/octet-stream;base64,{b64}" download="{os.path.basename(output_path)}">⬇️ Download Encrypted File</a>'
            st.markdown(href, unsafe_allow_html=True)

elif choice == "Decrypt File":
    st.subheader("🔓 Decrypt File")

    encrypted_file = st.file_uploader("Upload Encrypted File", type=None)
    qr_image = st.file_uploader("Upload QR Code Image (with key)", type=["png", "jpg", "jpeg"])

    if encrypted_file and qr_image:
        password = decode_qr_from_image(qr_image)

        if password:
            output_path = decrypt_file(encrypted_file, password)
            st.success("File decrypted successfully!")

            with open(output_path, "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
                href = f'<a href="data:application/octet-stream;base64,{b64}" download="{os.path.basename(output_path)}">⬇️ Download Decrypted File</a>'
                st.markdown(href, unsafe_allow_html=True)
        else:
            st.error("Failed to decode QR code. Please try another image.")

