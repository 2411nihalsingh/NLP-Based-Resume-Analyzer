import streamlit as st
import fitz  # PyMuPDF
from dotenv import load_dotenv
import os, re, tempfile
import google.generativeai as genai
from google.generativeai import GenerativeModel

# Load environment variables (API key)
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = GenerativeModel("gemini-1.5-flash")

# --- Streamlit UI ---
st.set_page_config(page_title="Resume Grammar Checker", layout="centered")
st.title("📄 Resume Grammar & Spelling Checker")
uploaded_file = st.file_uploader("Upload your resume (PDF)", type="pdf")

# --- Functions ---

def extract_text_from_pdf(uploaded_file) -> str:
    """Extract full text from uploaded PDF."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        temp_path = tmp_file.name

    doc = fitz.open(temp_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    doc.close()

    return full_text

def preprocess_resume_text(text: str) -> str:
    """Clean up resume text."""
    text = text.encode("ascii", "ignore").decode()
    text = re.sub(r"[^\w\s.,;:!?@&%()+'/\-']", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def chunk_text(text, max_words=100):
    """Yield text in chunks of N words."""
    words = text.split()
    for i in range(0, len(words), max_words):
        yield " ".join(words[i:i+max_words])

def get_grammar_suggestions_from_gemini(text: str) -> list:
    """Get grammar and spelling suggestions from Gemini in chunks."""
    final_suggestions = []

    prompt_intro = """
You are an expert English editor and proofreader.

Correct only actual **spelling mistakes, grammar errors, or incorrect word usage** in the text below.

Respond in this format for each issue:
"mistake" -> "correction"

Examples:
"recieved" -> "received"
"worked with team for deliver project" -> "worked with the team to deliver the project"

Text to review:
"""

    for chunk in chunk_text(text):
        prompt = prompt_intro + "\n" + chunk
        response = model.generate_content(prompt)
        suggestions = response.text.strip().split("\n")

        for line in suggestions:
            if "->" in line and len(line.strip()) > 5:
                final_suggestions.append(line.strip())

    return final_suggestions

# --- Main Logic ---
if uploaded_file:
    extracted_text = extract_text_from_pdf(uploaded_file)
    preprocessed_text = preprocess_resume_text(extracted_text)
    st.subheader("✅ Grammar & Spelling Suggestions")

    with st.spinner("Analyzing your resume..."):
        suggestions = get_grammar_suggestions_from_gemini(preprocessed_text)

    if suggestions:
        for suggestion in suggestions:
            st.markdown(f"🔸 {suggestion}")
    else:
        st.success("No significant grammar or spelling mistakes found! 🎉")