import streamlit as st
import pdfplumber
from ollama import chat
from ollama import ChatResponse

st.title("Summarize CV")
st.write("Upload the CV and get a summary of the last 2 years of activities.")

uploaded_file = st.file_uploader("Choose a file", type="pdf")
if uploaded_file is not None:
    # Shows pdf
    st.pdf(uploaded_file)

    # Extract text from pdf
    with pdfplumber.open(uploaded_file) as pdf:
        full_text = ""

        for page in pdf.pages:
            words = page.extract_text(x_tolerance=0.5)
            full_text += words + "\n\n"
        
        response: ChatResponse = chat(model='gemma3:4b', messages=[
          {
            'role': 'user',
            'content': f'{full_text}, summarize the last 2 years of activities in a few bullet points',
          },
        ])

    # Display extracted text
    st.text_area("Extracted Text", full_text, height=500)
    st.text_area("Extracted Text", response.message.content, height=500)
