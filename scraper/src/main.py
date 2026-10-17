"""
The Polite Scraper - Books to Scrape (FlyRank Backend Track - W5-A9)
Stage 1: Fetch and cache HTML
"""
import os
import sys
import requests
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
CACHE_DIR = BASE_DIR / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

USER_AGENT = "FlyRankInternship-A9/1.0 (+https://github.com/BennedictQuanTon/todo-crud-api)"
PAGE_1_URL = "https://books.toscrape.com/catalogue/page-1.html"
TIMEOUT_SECONDS = 5.0

def fetch_page(url: str, cache_path: Path, timeout: float = TIMEOUT_SECONDS) -> tuple[str, bool]:
    """
    Polite fetcher with local disk caching:
    - Checks cache first.
    - If missing, sends request with custom User-Agent and timeout.
    - Verifies HTTP 200 before storing to cache.
    """
    if cache_path.exists():
        content = cache_path.read_text(encoding="utf-8")
        print(f"[CACHE HIT] {url} (size: {len(content):,} bytes, file: {cache_path.name})")
        return content, True

    headers = {"User-Agent": USER_AGENT}
    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        if response.status_code != 200:
            raise RuntimeError(f"Failed to fetch {url}: HTTP {response.status_code}")
        
        html = response.text
        cache_path.write_text(html, encoding="utf-8")
        print(f"[FETCH] {url} (status: 200, size: {len(html):,} bytes -> saved to {cache_path.name})")
        return html, False
    except requests.RequestException as e:
        raise RuntimeError(f"Network error fetching {url}: {e}")

def main():
    print("--- Stage 1: Fetch and cache HTML ---")
    cache_file = CACHE_DIR / "catalogue-page-1.html"
    html, hit = fetch_page(PAGE_1_URL, cache_file)
    print(f"Result: {'Cache Hit' if hit else 'Fresh Fetch'}, Length: {len(html):,} characters.")

if __name__ == "__main__":
    main()
