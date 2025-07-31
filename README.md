# 🔐 Secure File Sharing using QR Code and AES Encryption

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://www.python.org/)  
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A modern and secure file-sharing desktop app that allows users to **encrypt files using AES**, **generate a QR code for password sharing**, and enable others to **decrypt the file by scanning the QR code** or entering the password manually.  

Built using **Python**, **Tkinter**, **PyCryptodome**, **qrcode**, and **OpenCV** – designed for privacy-first offline sharing.

---

## ✨ Features

- 🔒 AES-256 file encryption in CBC mode  
- 📄 Upload & encrypt any file (PDF, Word, Images, etc.)  
- 📷 QR code generation for secure key sharing  
- 📸 QR scanner using webcam to read encrypted password  
- 💻 Simple and beautiful desktop interface using Tkinter  
- 🔓 Decrypt by scanning or entering password manually  
- 📁 Files saved in `uploads/` folder after encryption/decryption  

---

## 🔗 Live Demo: [secure-qr-file-sharing.onrender.com](https://secure-qr-file-sharing.onrender.com/)

---

## 🔁 Workflow

1. User selects a file and enters a password
2. File is encrypted using AES-256
3. Password is encoded into a QR code
4. Encrypted file and QR code are shared
5. Receiver either:
   - Scans QR code using webcam, OR
   - Manually enters password
6. File is decrypted and saved in `uploads/`

## 🛠️ Installation
Clone the repository:

bash

git clone https://github.com/PurnimaKishore08/secure-qr-file-sharing.git
cd secure-qr-file-sharing
Create virtual environment (optional but recommended):

bash

python -m venv venv
venv\Scripts\activate  # On Windows

## Install dependencies:

bash

pip install -r requirements.txt
🚀 How to Use
Run the main app:

bash

python app.py
Choose from:

Encrypt File – Upload any file and enter a password to generate an encrypted version + QR.

Decrypt File – Upload the encrypted file and scan the QR code or enter password manually.

All files are saved to the uploads/ folder.

## 🧰 Tech Stack
Python 3.10+

Tkinter – GUI

PyCryptodome – AES Encryption

qrcode – QR Code generation

OpenCV – QR Code scanning via webcam

 ## 📁 Folder Structure
bash
Copy
Edit
secure-qr-file-sharing/
│
├── app.py                # Main UI logic
├── encryption.py         # AES encryption & decryption logic
├── qr_utils.py           # QR code generation and scanning
├── utils.py              # Helper functions
├── scan_and_decrypt.py   # QR scanning window
├── requirements.txt
├── uploads/              # All saved files (input/output)
└── README.md
