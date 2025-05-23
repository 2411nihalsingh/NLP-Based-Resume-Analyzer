# utils/text_utils.py

import fitz  # PyMuPDF
import tempfile
import re

class TextExtractor:
    def __init__(self, uploaded_file):
        self.raw_text = self._extract_text(uploaded_file)
        self.processed_text = self._preprocess_text(self.raw_text)

    def _extract_text(self, uploaded_file) -> str:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.read())
            temp_path = tmp_file.name

        doc = fitz.open(temp_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text

    def _preprocess_text(self, text: str) -> str:
        text = text.encode("ascii", "ignore").decode()
        text = re.sub(r"[^\w\s.,;:!?@&%()+/\-']", " ", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    def get_processed_text(self) -> str:
        return self.processed_text
