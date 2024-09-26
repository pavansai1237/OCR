import streamlit as st
from PIL import Image
import easyocr
import numpy as np
import re
import json

# Initialize EasyOCR reader
reader = easyocr.Reader(['en', 'hi'])  # Specify the languages

def extract_text(image):
    try:
        image = np.array(image)  # Convert PIL Image to numpy array
        results = reader.readtext(image)  # Perform OCR
        extracted_text = ' '.join([result[1] for result in results])  # Concatenate text
        return extracted_text
    except Exception as e:
        st.error(f"Error during text extraction: {e}")
        return ""

def highlight_text(text, keyword):
    if not text or not keyword:
        return text
    pattern = re.compile(re.escape(keyword), re.IGNORECASE)
    highlighted_text = re.sub(pattern, lambda m: f"<span style='color: red; font-weight: bold;'>{m.group(0)}</span>", text)
    return highlighted_text

def main():
    st.title("Text Scanner and Generator")

    # Initialize session state variables
    if 'extracted_text' not in st.session_state:
        st.session_state.extracted_text = ""
    if 'keyword' not in st.session_state:
        st.session_state.keyword = ""

    uploaded_image = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

    if uploaded_image is not None:
        try:
            image = Image.open(uploaded_image)  # Open the uploaded image
            st.image(image, caption='Uploaded Image', use_column_width=True)

            # Extract text and store in session state
            st.session_state.extracted_text = extract_text(image)  
            st.text_area("Extracted Text", st.session_state.extracted_text, height=200)

            st.session_state.keyword = st.text_input("Enter a keyword", st.session_state.keyword)

            if st.button("Search"):
                highlighted_text = highlight_text(st.session_state.extracted_text, st.session_state.keyword)
                st.markdown(highlighted_text, unsafe_allow_html=True)

            # Prepare text for download
            if st.session_state.extracted_text:
                json_data = json.dumps({"extracted_text": st.session_state.extracted_text}, ensure_ascii=False)
                st.download_button(
                    label="Download Text as JSON",
                    data=json_data,
                    file_name='extracted_text.json',
                    mime='application/json'
                )
        except Exception as e:
            st.error(f"An error occurred while processing the image: {e}")

if __name__ == "__main__":
    main()
