# beautiful_unit_converter.py

import streamlit as st

# Unit conversion dictionary (relative to metre)
length_units = {
    "Millimetre": 0.001,
    "Centimetre": 0.01,
    "Metre": 1,
    "Kilometre": 1000,
    "Inch": 0.0254,
    "Foot": 0.3048,
    "Yard": 0.9144,
    "Mile": 1609.34
}

# Page config
st.set_page_config(page_title="Beautiful Unit Converter", layout="centered")

# 💅 Style injection
st.markdown("""
    <style>
        .title {
            color: #4F8BF9;
            font-weight: bold;
            font-size: 36px;
            text-align: center;
            margin-top: 30px;
        }
        .result-box {
            font-size: 24px;
            font-weight: bold;
            color: #4CAF50;
            text-align: center;
            margin-top: 1rem;
        }
        .formula-box {
            background-color: #fff3cd;
            border-left: 6px solid #ffc107;
            padding: 1rem;
            margin-top: 2rem;
            border-radius: 8px;
            font-size: 15px;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<div class='title'>🔁 Google-Style Unit Converter</div>", unsafe_allow_html=True)

# 💳 Card container using st.container() + CSS styling
with st.container():

    # Input field
    input_value = st.number_input("Enter Value", min_value=0.0, format="%.4f", value=1.0)

    # Unit selectors
    col1, col2 = st.columns(2)
    with col1:
        from_unit = st.selectbox("From", list(length_units.keys()), index=2)
    with col2:
        to_unit = st.selectbox("To", list(length_units.keys()), index=1)

    # Conversion calculation
    result = input_value * length_units[from_unit] / length_units[to_unit]
    st.markdown(f"<div class='result-box'>= {result:.4f}</div>", unsafe_allow_html=True)

    # Formula explanation
    st.markdown(f"""
        <div class="formula-box">
            <strong>Formula:</strong> Multiply the value in <i>{from_unit}</i> by <code>{length_units[from_unit]}</code>, 
            then divide by <code>{length_units[to_unit]}</code>.
        </div>
    """, unsafe_allow_html=True)

