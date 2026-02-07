import fitz
import re

class PDFParser:
    @classmethod
    def extract_text(cls, path):
        doc = fitz.open(path)
        text = ""
        for page in doc:
            text += page.get_text() + "\n"
        doc.close()
        text = re.sub(r"\s+", " ", text)
        return text.strip()
