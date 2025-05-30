import re
import streamlit as st
from PyPDF2 import PdfReader

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    pdf_reader = PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Extract Name (Assume it's the first non-empty line)
def extract_name(text):
    lines = text.strip().split('\n')
    for line in lines:
        if line.strip():
            return line.strip()
    return None

# Extract email and phone using regex
def extract_contact_info(text):
    email = re.search(r'[\w\.-]+@[\w\.-]+', text)
    phone = re.search(r'(?:(?:\+91)|(?:0))?\d{10}', text)
    return email.group() if email else None, phone.group() if phone else None

# Extract skills (assuming "SKILLS" section present)
def extract_skills(text):
    skills_match = re.search(r'SKILLS\s*(.*?)\s*(EDUCATION|CERTIFICATIONS|PROJECT|HOBBIES)', text, re.S | re.I)
    if skills_match:
        skills_text = skills_match.group(1).strip()
        return [skill.strip() for skill in re.split(r',|\n', skills_text) if skill.strip()]
    return []

# Extract certifications
def extract_certifications(text):
    cert_match = re.search(r'CERTIFICATIONS\s*(.*?)\s*(PROJECT|EXPERIENCE|HOBBIES)', text, re.S | re.I)
    if cert_match:
        return cert_match.group(1).strip()
    return ""

# Extract education
def extract_education(text):
    edu_match = re.search(r'EDUCATION\s*(.*?)\s*(CERTIFICATIONS|PROJECT|HOBBIES)', text, re.S | re.I)
    if edu_match:
        return edu_match.group(1).strip()
    return ""

# Streamlit UI
st.title("ATS Resume Parser")

uploaded_file = st.file_uploader("Upload a Resume PDF", type="pdf")

if uploaded_file:
    text = extract_text_from_pdf(uploaded_file)
    
    st.subheader("Extracted Information")
    st.write("**Name:**", extract_name(text))
    email, phone = extract_contact_info(text)
    st.write("**Email:**", email)
    st.write("**Phone:**", phone)
    st.write("**Skills:**", extract_skills(text))
    st.write("**Certifications:**", extract_certifications(text))
    st.write("**Education:**", extract_education(text))



