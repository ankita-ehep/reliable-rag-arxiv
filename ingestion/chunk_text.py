from pathlib import Path
import json
import tiktoken

TEXT_DIR = Path("data/processed/text")
OUT_DIR = Path("data/processed/chunks")
OUT_DIR.mkdir(parents=True, exist_ok=True)

ENCODING = tiktoken.get_encoding("cl100k_base")

CHUNK_SIZE = 600
OVERLAP = 100

def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=OVERLAP):
    tokens = ENCODING.encode(text)
    chunks = []

    start = 0
    chunk_id = 0

    while start < len(tokens):
        end = start + chunk_size
        chunk_tokens = tokens[start:end]
        chunk_text = ENCODING.decode(chunk_tokens)

        chunks.append((chunk_id, chunk_text))
        chunk_id += 1
        start += chunk_size - overlap

    return chunks

def process_all_files():
    all_chunks = []

    txt_files = list(TEXT_DIR.glob("*.txt"))
    print(f"Chunking {len(txt_files)} text files")

    for txt in txt_files:
        paper_id = txt.stem
        text = txt.read_text(encoding="utf-8")

        chunks = chunk_text(text)

        for cid, chunk in chunks:
            all_chunks.append({
                "paper_id": paper_id,
                "chunk_id": cid,
                "source": "arxiv",
                "category": "cs.AI",
                "text": chunk
            })

    out_path = OUT_DIR / "cs_ai_chunks.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2)

    print(f"Saved {len(all_chunks)} chunks")

if __name__ == "__main__":
    process_all_files()
