import feedparser
import requests
from pathlib import Path

BASE_URL = "http://export.arxiv.org/api/query?"

def fetch_arxiv_cs_ai(max_results=50):
    query = f"search_query=cat:cs.AI&sortBy=submittedDate&sortOrder=descending&max_results={max_results}"
    feed = feedparser.parse(BASE_URL + query)
    return feed.entries

def download_pdf(arxiv_id, out_dir="data/raw"):
    url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    pdf_path = out_dir / f"{arxiv_id}.pdf"
    if not pdf_path.exists():
        r = requests.get(url)
        pdf_path.write_bytes(r.content)

if __name__ == "__main__":
    entries = fetch_arxiv_cs_ai()
    for e in entries:
        arxiv_id = e.id.split("/")[-1]
        download_pdf(arxiv_id)
