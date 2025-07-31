import streamlit as st
from encryption import encrypt_file, decrypt_file
from qr_utils import generate_qr
import os

st.set_page_config(page_title="Secure File Sharing via QR", layout="centered")
st.title("🔐 Secure File Sharing via QR Code")

menu = ["Encrypt & Generate QR", "Decrypt File"]
choice = st.sidebar.selectbox("Select Action", menu)

if choice == "Encrypt & Generate QR":
    uploaded_file = st.file_uploader("📤 Upload a file to encrypt", type=["txt", "pdf", "png", "jpg", "jpeg"])
    password = st.text_input("🔑 Enter a password", type="password")

    if uploaded_file and password:
        with open(uploaded_file.name, "wb") as f:
            f.write(uploaded_file.read())
        encrypted_file_path, key = encrypt_file(uploaded_file.name, password)

        if encrypted_file_path:
            qr_image = generate_qr(key)
            st.success("✅ File encrypted and QR code generated!")
            st.image(qr_image, caption="Scan this QR to get the decryption key")
            with open(encrypted_file_path, "rb") as ef:
                st.download_button("⬇️ Download Encrypted File", ef, file_name="encrypted_file.bin")
            os.remove(uploaded_file.name)

elif choice == "Decrypt File":
    encrypted_file = st.file_uploader("📥 Upload the encrypted file", type=["bin"])
    password = st.text_input("🔑 Enter the password used during encryption", type="password")
    key_input = st.text_input("🧩 Paste the key from the QR code")

    if encrypted_file and password and key_input:
        with open("received_encrypted.bin", "wb") as ef:
            ef.write(encrypted_file.read())

        decrypted_path = decrypt_file("received_encrypted.bin", password, key_input)

        if decrypted_path:
            with open(decrypted_path, "rb") as df:
                st.download_button("⬇️ Download Decrypted File", df, file_name="decrypted_output")
            st.success("✅ File decrypted successfully!")
            os.remove(decrypted_path)
            os.remove("received_encrypted.bin")
        else:
            st.error("❌ Decryption failed. Check your key or password.")
