##invoice extractor


import streamlit as st
import os
from PIL import Image
import google.generativeai  as genai

##configuring API key
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

##function to load gemini model and get response
def get_gemini_response(input, image, prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")

    response = model.generate_content(
        [input, image,prompt], 
    )
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()

        #Return image_part
        image_part = {
            "mime_type": uploaded_file.type,
            "data": bytes_data
        }
        return image_part
    else:
        raise FileNotFoundError("No file uploaded")


##streamlit set up
st.set_page_config(page_title="Invoice Extractor")

st.header("Gemini Application")

input = st.text_input("Input Prompt", key="input")

uploaded_file = st.file_uploader("choose an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

submit = st.button("tell me about the invoice")

input_prompt = """
You are an expert in understanding invoices. 
You will receive input images as invoices, and you will have to answer questions based on input image
"""

##if submit button is clicked
if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompt, image_data, input)

    st.subheader("the response is")
    st.write(response)
