import streamlit as st
import easyocr
from PIL import Image
import requests

# ---------------- PAGE SETUP ----------------
st.set_page_config(page_title="Image → Hindi Translator", page_icon="🖼️")
st.title("🖼️ Image to Hindi Translator")
st.write("Upload an image containing **English text**")

# ---------------- OCR READER ----------------
reader = easyocr.Reader(['en'], gpu=False)

# ---------------- TRANSLATION FUNCTION ----------------
def translate_to_hindi(text):
    url = "https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-en-hi"
    payload = {"inputs": text}
    response = requests.post(url, json=payload)
    try:
        return response.json()[0]["translation_text"]
    except:
        return "Translation failed"

# ---------------- IMAGE INPUT ----------------
uploaded_file = st.file_uploader("Upload image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    if st.button("Translate Image"):
        with st.spinner("Reading text from image..."):
            result = reader.readtext(image)
            extracted_text = " ".join([r[1] for r in result])

        st.subheader("📄 Extracted English Text")
        st.write(extracted_text)

        with st.spinner("Translating to Hindi..."):
            hindi_text = translate_to_hindi(extracted_text)

        st.subheader("🇮🇳 Hindi Translation")
        st.success(hindi_text)
