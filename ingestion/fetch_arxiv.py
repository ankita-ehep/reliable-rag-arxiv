import feedparser
import requests
from pathlib import Path
from tqdm import tqdm
import json

BASE_URL = "http://export.arxiv.org/api/query?"

def fetch_cs_ai(max_results=50):
    query = (
        "search_query=cat:cs.AI"
        "&sortBy=submittedDate"
        "&sortOrder=descending"
        f"&max_results={max_results}"
    )
    feed = feedparser.parse(BASE_URL + query)
    return feed.entries

def download_pdf(arxiv_id, out_dir):
    url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
    pdf_path = out_dir / f"{arxiv_id}.pdf"

    if not pdf_path.exists():
        r = requests.get(url)
        pdf_path.write_bytes(r.content)

def run_pipeline(max_results=30):
    pdf_dir = Path("data/raw/pdfs")
    meta_dir = Path("data/raw/metadata")

    entries = fetch_cs_ai(max_results)
    metadata = []

    for e in tqdm(entries):
        arxiv_id = e.id.split("/")[-1]
        download_pdf(arxiv_id, pdf_dir)

        metadata.append({
            "paper_id": arxiv_id,
            "title": e.title,
            "authors": [a.name for a in e.authors],
            "published": e.published,
            "summary": e.summary,
            "category": "cs.AI"
        })

    with open(meta_dir / "cs_ai_metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)

if __name__ == "__main__":
    run_pipeline()
