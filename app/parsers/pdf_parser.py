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
        # Removed re.sub that was flattening text into a single line
        return text.strip()
