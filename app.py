## invoice extractor

from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

# Load .env and configure API key
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Function to get response from Gemini
def get_gemini_response(input, image, prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([input, image, prompt])
    return response.text

# Handle uploaded image
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_part = {
            "mime_type": uploaded_file.type,
            "data": bytes_data
        }
        return image_part
    else:
        raise FileNotFoundError("No file uploaded")

# ---------- STYLING ----------
st.markdown("""
    <style>
        body {
            background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
        }
        .main {
            background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
            color: white;
            font-family: 'Segoe UI', sans-serif;
        }
        .block-container {
            padding: 2rem 2rem;
            border-radius: 12px;
            background-color: rgba(255, 255, 255, 0.05);
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.4);
        }
        input, textarea {
            background-color: #ffffff10 !important;
            color: white !important;
            border: 1px solid #ffffff50 !important;
        }
        button[kind="primary"] {
            background-color: #0074D9 !important;
            color: white !important;
            font-weight: bold !important;
            border: none !important;
        }
        /* Updated label font size */
        label.css-1cpxqw2, label.css-1c7p6b4 {
            font-size: 60px !important;
            font-weight: 1200;
            color: #FFFFFF !important;
        }
    </style>
""", unsafe_allow_html=True)

# ---------- STREAMLIT UI ----------
st.set_page_config(page_title="Invoice Extractor")

st.title("📄 Invoice Extractor")

input = st.text_input("💬 Input Prompt", key="input")

uploaded_file = st.file_uploader("📎 Choose an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="🖼 Uploaded Image", use_container_width=True)

submit = st.button("🔍 Tell me about the invoice")

# Gemini input prompt
input_prompt = """
You are an expert in understanding invoices. 
You will receive input images as invoices, and you will have to answer questions based on input image.
"""

if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompt, image_data, input)

    st.subheader("📝 The response is")
    st.write(response)
