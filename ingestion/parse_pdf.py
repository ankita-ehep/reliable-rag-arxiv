import fitz  # PyMuPDF
from pathlib import Path

def extract_text(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def remove_references(text):
    for token in ["References", "REFERENCES"]:
        if token in text:
            return text.split(token)[0]
    return text

if __name__ == "__main__":
    pdfs = Path("data/raw").glob("*.pdf")
    Path("data/processed").mkdir(parents=True, exist_ok=True)

    for pdf in pdfs:
        text = extract_text(pdf)
        text = remove_references(text)
        out = Path("data/processed") / f"{pdf.stem}.txt"
        out.write_text(text)
