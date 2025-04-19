import streamlit as st
import re
import random
import string
import requests

# ---------------------------------------
# Load Lottie Animation
# ---------------------------------------
def load_lottie_url(url: str):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()
    except:
        return None

# ---------------------------------------
# Check Password Strength Function
# ---------------------------------------
def check_password_strength(password):
    score = 0
    feedback = []

    if len(password) >= 8:
        score += 1
    else:
        feedback.append("At least 8 characters.")

    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("Mix uppercase and lowercase letters.")

    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("Include at least one number.")

    if re.search(r"[!@#$%^&*]", password):
        score += 1
    else:
        feedback.append("Add a special character (!@#$%^&*).")

    # Common Password Blacklist
    common_passwords = ["password", "123456", "password123", "qwerty", "letmein"]
    if password.lower() in common_passwords:
        feedback.append("Too common. Try something unique.")

    return score, feedback

# ---------------------------------------
# Generate Strong Password Function
# ---------------------------------------
def generate_strong_password(length=12):
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(chars) for _ in range(length))

# ---------------------------------------
# UI Setup
# ---------------------------------------
st.set_page_config(page_title="Password Strength Checker", layout="centered")
st.title("🔐 Password Strength Checker")

# Lottie Animation
try:
    from streamlit_lottie import st_lottie
    lottie_animation = load_lottie_url("https://assets10.lottiefiles.com/packages/lf20_jcikwtux.json")
    if lottie_animation:
        st_lottie(lottie_animation, height=200)
except:
    st.warning("Install `streamlit-lottie` to enable animations.")

# ---------------------------------------
# Layout
# ---------------------------------------
col1, col2 = st.columns([4, 1], vertical_alignment="bottom")

with col1:
    password_input = st.text_input("Enter a password to check:", type="password", key="password_input")
with col2:
    if st.button("🔍 Analyze"):
        st.session_state.run_check = True
    else:
        st.session_state.run_check = False

# ---------------------------------------
# Password Strength Check
# ---------------------------------------
if st.session_state.get("run_check") and password_input:
    score, suggestions = check_password_strength(password_input)
    st.markdown(f"### 🔢 Score: {score}/4")

    if score == 4:
        st.success("✅ Strong password!")
    elif score == 3:
        st.warning("⚠️ Moderate password. Could be stronger.")
    else:
        st.error("❌ Weak password. Needs improvement.")

    if suggestions:
        st.markdown("### 💡 Suggestions:")
        for tip in suggestions:
            st.markdown(f"- {tip}")

# ---------------------------------------
# Password Generator Section
# ---------------------------------------
st.divider()
st.markdown("### 🔐 Generate a Strong Password")

gen_col1, gen_col2 = st.columns([3, 1], vertical_alignment="bottom")
with gen_col1:
    if "generated_password" not in st.session_state:
        st.session_state.generated_password = ""

    if st.button("⚡ Generate Password"):
        st.session_state.generated_password = generate_strong_password()

    if st.session_state.generated_password:
        st.code(st.session_state.generated_password, language="")

with gen_col2:
    if st.session_state.generated_password:
        st.download_button(
            label="📋 Copy Password",
            data=st.session_state.generated_password,
            file_name="secure_password.txt",
            mime="text/plain"
        )
