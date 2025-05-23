# grammar_checker.py

import os
import re
import fitz
import base64
import tempfile
from io import BytesIO
import streamlit as st
from dotenv import load_dotenv
from google.generativeai import GenerativeModel
import google.generativeai as genai


class GrammarChecker:
    def __init__(self):
        load_dotenv()
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = GenerativeModel("gemini-1.5-flash")

    def get_grammar_suggestions(self, text: str) -> str:
        prompt = f"""You are an expert English editor and proofreader.
                Carefully review the following resume text for any **clear grammatical mistakes, definite spelling errors, or obviously incorrect word usage**.

                Do **not** make style or rephrasing suggestions.
                Do **not** suggest changes unless the mistake is clearly wrong.
                Do **not** be overly cautious — only point out **actual, unambiguous errors**.

                For each real issue you find, respond using this **exact format** on a **new line**, and keep both the mistake and correction inside **double quotation marks**:
                "mistake" + -> + "correction"

                Only use this format — do not include explanations or anything else.

                Here is the resume:
                {text}
"""
        response = self.model.generate_content(prompt)
        return response.text.strip()

    def extract_mistakes(self, gemini_output: str) -> list:
        lines = gemini_output.strip().split("\n")
        mistakes = []
        for line in lines:
            if '->' in line:
                parts = line.strip().split("->")
                if len(parts) == 2:
                    mistake = parts[0].strip().strip('"')
                    mistakes.append(mistake)
        return mistakes

    def highlight_pdf_mistakes(self, uploaded_file, mistakes: list) -> str:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.read())
            temp_path = tmp_file.name

        doc = fitz.open(temp_path)
        for page in doc:
            for mistake in mistakes:
                for inst in page.search_for(mistake):
                    highlight = page.add_highlight_annot(inst)
                    highlight.set_info(title="Grammar Issue", content=f"{mistake}")
                    highlight.update()

        highlighted_path = os.path.join(tempfile.gettempdir(), "highlighted_resume.pdf")
        doc.save(highlighted_path, garbage=4, deflate=True, clean=True)
        doc.close()
        return highlighted_path

    def display_pdf(self, file_path: str):
        with open(file_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode("utf-8")
        st.markdown(
            f"""<iframe src="data:application/pdf;base64,{base64_pdf}" 
                 width="100%" height="800px" type="application/pdf"></iframe>""",
            unsafe_allow_html=True,
        )
