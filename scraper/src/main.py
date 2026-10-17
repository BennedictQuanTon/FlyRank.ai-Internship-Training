"""
The Polite Scraper - Books to Scrape (FlyRank Backend Track - W5-A9)
Stage 2: Discover three catalogue pages and 60 book URLs
"""
import os
import sys
import time
import requests
from pathlib import Path
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from typing import List, Tuple

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
CACHE_DIR = BASE_DIR / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

USER_AGENT = "FlyRankInternship-A9/1.0 (+https://github.com/BennedictQuanTon/todo-crud-api)"
START_URL = "https://books.toscrape.com/catalogue/page-1.html"
TIMEOUT_SECONDS = 5.0
POLITE_DELAY_SECONDS = 0.5
MAX_CATALOGUE_PAGES = 3

def fetch_page(url: str, cache_path: Path, timeout: float = TIMEOUT_SECONDS) -> Tuple[str, bool]:
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

def discover_catalogue_books(start_url: str = START_URL, max_pages: int = MAX_CATALOGUE_PAGES) -> Tuple[List[str], int, int]:
    """
    Crawls exactly max_pages of the catalogue following the site's own 'next' pagination.
    Extracts and converts relative book URLs to absolute URLs.
    """
    discovered_urls: List[str] = []
    current_url = start_url
    pages_crawled = 0

    while current_url and pages_crawled < max_pages:
        pages_crawled += 1
        cache_file = CACHE_DIR / f"catalogue-page-{pages_crawled}.html"
        
        html, is_cache_hit = fetch_page(current_url, cache_file)
        if not is_cache_hit:
            time.sleep(POLITE_DELAY_SECONDS)

        soup = BeautifulSoup(html, "html.parser")
        
        # Extract book links from product pods
        pods = soup.select("article.product_pod")
        for pod in pods:
            a_tag = pod.select_one("h3 a")
            if a_tag and a_tag.get("href"):
                abs_url = urljoin(current_url, a_tag["href"])
                discovered_urls.append(abs_url)

        # Look for the pagination 'next' link
        next_tag = soup.select_one("li.next a")
        if next_tag and next_tag.get("href") and pages_crawled < max_pages:
            current_url = urljoin(current_url, next_tag["href"])
        else:
            current_url = None

    unique_urls = list(dict.fromkeys(discovered_urls))
    return unique_urls, pages_crawled, len(discovered_urls)

def main():
    print("--- Stage 2: Discover three catalogue pages ---")
    unique_urls, pages, discovered_count = discover_catalogue_books()
    print(f"catalogue_pages={pages}, discovered={discovered_count}, unique_urls={len(unique_urls)}")
    if unique_urls:
        print(f"Sample book 1: {unique_urls[0]}")
        print(f"Sample book {len(unique_urls)}: {unique_urls[-1]}")

if __name__ == "__main__":
    main()
