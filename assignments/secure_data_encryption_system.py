import streamlit as st
import hashlib
from cryptography.fernet import Fernet

# Setup encryption key
if "key" not in st.session_state:
    st.session_state.key = Fernet.generate_key()
    st.session_state.cipher = Fernet(st.session_state.key)

# Initialize session variables
if "stored_data" not in st.session_state:
    st.session_state.stored_data = {}  # {"data_id": {"encrypted_text": "xyz", "passkey": "hashed"}}
if "failed_attempts" not in st.session_state:
    st.session_state.failed_attempts = 0

# Hash passkey
def hash_passkey(passkey):
    return hashlib.sha256(passkey.encode()).hexdigest()

# Encrypt data
def encrypt_data(text):
    return st.session_state.cipher.encrypt(text.encode()).decode()

# Decrypt data
def decrypt_data(encrypted_text, passkey):
    hashed_passkey = hash_passkey(passkey)

    for entry in st.session_state.stored_data.values():
        if entry["encrypted_text"] == encrypted_text and entry["passkey"] == hashed_passkey:
            st.session_state.failed_attempts = 0
            return st.session_state.cipher.decrypt(encrypted_text.encode()).decode()
    
    st.session_state.failed_attempts += 1
    return None

# UI
st.title("🔒 Secure Data Encryption System")

menu = ["Home", "Store Data", "Retrieve Data", "Login"]
choice = st.sidebar.selectbox("Navigation", menu)

if choice == "Home":
    st.subheader("🏠 Welcome to Secure Storage")
    st.markdown("""
    - Store confidential data securely.
    - Use a secret passkey to protect & retrieve your data.
    - After 3 wrong attempts, reauthorization is required.
    """)

elif choice == "Store Data":
    st.subheader("📂 Store New Data")

    data_id = st.text_input("Enter Data Identifier (e.g. Note1, UserX)", key="store_id")
    user_data = st.text_area("Enter your text")
    passkey = st.text_input("Set a Passkey", type="password")

    if st.button("🔐 Encrypt & Save"):
        if data_id and user_data and passkey:
            encrypted = encrypt_data(user_data)
            st.session_state.stored_data[data_id] = {
                "encrypted_text": encrypted,
                "passkey": hash_passkey(passkey)
            }
            st.success("✅ Data encrypted and stored successfully!")
            st.code(encrypted, language="text")
        else:
            st.error("⚠️ Please fill all fields.")

elif choice == "Retrieve Data":
    st.subheader("🔎 Retrieve Your Data")

    if st.session_state.failed_attempts >= 3:
        st.warning("🔒 Too many failed attempts! Redirecting to Login Page.")
        st.rerun() 

    encrypted_input = st.text_area("Paste Encrypted Text")
    passkey_input = st.text_input("Enter Passkey", type="password")

    if st.button("🔓 Decrypt"):
        if encrypted_input and passkey_input:
            decrypted = decrypt_data(encrypted_input, passkey_input)
            if decrypted:
                st.success("✅ Data successfully decrypted!")
                st.code(decrypted, language="text")
            else:
                st.error(f"❌ Incorrect passkey! Attempts left: {3 - st.session_state.failed_attempts}")
        else:
            st.error("⚠️ Please enter both fields.")

# elif choice == "Login":
    # st.subheader("🔑 Reauthorization")

    # login_pass = st.text_input("Enter Master Password", type="password")
    # if st.button("🔓 Login"):
    #     if login_pass == "admin123":
    #         st.session_state.failed_attempts = 0
    #         st.success("✅ Reauthorized successfully!")
    #         st.rerun()
    #     else:
    #         st.error("❌ Incorrect master password.")

elif choice == "Login":
    st.subheader("🔑 Reauthorization")

    # Check if just reauthorized
    if st.session_state.get("reauth_success", False):
        st.success("✅ Reauthorized successfully!")
        st.session_state.reauth_success = False  # Reset flag after showing
    else:
        login_pass = st.text_input("Enter Master Password", type="password")
        if st.button("🔓 Login"):
            if login_pass == "admin123":
                st.session_state.failed_attempts = 0
                st.session_state.reauth_success = True  # Set success flag
                st.rerun()
            else:
                st.error("❌ Incorrect master password.")
