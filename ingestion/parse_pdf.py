import fitz  # PyMuPDF
from pathlib import Path
import re

RAW_PDF_DIR = Path("data/raw/pdfs")
OUT_TEXT_DIR = Path("data/processed/text")

OUT_TEXT_DIR.mkdir(parents=True, exist_ok=True)

def extract_text(pdf_path):
    """Extract raw text from PDF"""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def remove_references(text):
    """Remove references/bibliography section"""
    patterns = [
        r"\nreferences\n",
        r"\nbibliography\n"
    ]
    for p in patterns:
        match = re.search(p, text, flags=re.IGNORECASE)
        if match:
            return text[:match.start()]
    return text

def clean_text(text):
    """Normalize whitespace"""
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def process_all_pdfs():
    pdfs = list(RAW_PDF_DIR.glob("*.pdf"))
    print(f"Found {len(pdfs)} PDFs")

    for pdf in pdfs:
        raw_text = extract_text(pdf)
        raw_text = remove_references(raw_text)
        cleaned = clean_text(raw_text)

        out_file = OUT_TEXT_DIR / f"{pdf.stem}.txt"
        out_file.write_text(cleaned, encoding="utf-8")

    print("PDF parsing completed")

if __name__ == "__main__":
    process_all_pdfs()
