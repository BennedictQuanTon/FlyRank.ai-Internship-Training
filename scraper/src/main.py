"""
The Polite Scraper - Books to Scrape (FlyRank Backend Track - W5-A9)
Stage 3: Extract raw book details with provenance and caching
"""
import os
import sys
import time
import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any, Optional, Tuple

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
        return content, True

    headers = {"User-Agent": USER_AGENT}
    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        if response.status_code != 200:
            raise RuntimeError(f"Failed to fetch {url}: HTTP {response.status_code}")
        
        response.encoding = "utf-8"
        html = response.text
        cache_path.write_text(html, encoding="utf-8")
        return html, False
    except requests.RequestException as e:
        raise RuntimeError(f"Network error fetching {url}: {e}")

def discover_catalogue_books(start_url: str = START_URL, max_pages: int = MAX_CATALOGUE_PAGES) -> List[Tuple[str, str]]:
    """
    Crawls max_pages of the catalogue.
    Returns list of tuples: (book_absolute_url, source_catalogue_page_url)
    """
    discovered: List[Tuple[str, str]] = []
    current_url = start_url
    pages_crawled = 0

    while current_url and pages_crawled < max_pages:
        pages_crawled += 1
        cache_file = CACHE_DIR / f"catalogue-page-{pages_crawled}.html"
        
        html, is_cache_hit = fetch_page(current_url, cache_file)
        print(f"[{'CACHE HIT' if is_cache_hit else 'FETCH'}] Catalogue page {pages_crawled}: {current_url}")
        if not is_cache_hit:
            time.sleep(POLITE_DELAY_SECONDS)

        soup = BeautifulSoup(html, "html.parser")
        
        pods = soup.select("article.product_pod")
        for pod in pods:
            a_tag = pod.select_one("h3 a")
            if a_tag and a_tag.get("href"):
                abs_url = urljoin(current_url, a_tag["href"])
                discovered.append((abs_url, current_url))

        next_tag = soup.select_one("li.next a")
        if next_tag and next_tag.get("href") and pages_crawled < max_pages:
            current_url = urljoin(current_url, next_tag["href"])
        else:
            current_url = None

    # Deduplicate by product_url while preserving order
    seen = set()
    unique: List[Tuple[str, str]] = []
    for item in discovered:
        if item[0] not in seen:
            seen.add(item[0])
            unique.append(item)
    return unique

def extract_book_raw_record(product_url: str, source_page: str) -> Dict[str, Any]:
    """
    Fetches (or loads from cache) the detail page and extracts the 8 raw fields.
    """
    # Safe cache filename based on URL slug or hash
    slug = product_url.strip("/").split("/")[-2] if "/" in product_url else "unknown"
    cache_file = CACHE_DIR / f"book-{slug}.html"
    
    html, is_cache_hit = fetch_page(product_url, cache_file)
    if not is_cache_hit:
        time.sleep(POLITE_DELAY_SECONDS)

    soup = BeautifulSoup(html, "html.parser")
    main_section = soup.select_one(".product_main")
    
    # Title
    title_tag = main_section.select_one("h1") if main_section else None
    title = title_tag.get_text(strip=True) if title_tag else ""
    
    # Price text
    price_tag = main_section.select_one(".price_color") if main_section else None
    price_text = price_tag.get_text(strip=True) if price_tag else ""
    
    # Availability text
    avail_tag = main_section.select_one(".availability") if main_section else None
    availability_text = avail_tag.get_text(strip=True) if avail_tag else ""
    
    # Rating text
    rating_text = None
    if main_section:
        star_tag = main_section.select_one(".star-rating")
        if star_tag:
            classes = star_tag.get("class", [])
            rating_candidates = [c for c in classes if c != "star-rating"]
            if rating_candidates:
                rating_text = rating_candidates[0]
                
    # Description (can be null if missing)
    desc_header = soup.select_one("#product_description")
    description = None
    if desc_header:
        p_desc = desc_header.find_next_sibling("p")
        if p_desc:
            description = p_desc.get_text(strip=True)

    # Provenance timestamp
    fetched_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    return {
        "title": title,
        "product_url": product_url,
        "price_text": price_text,
        "availability_text": availability_text,
        "rating_text": rating_text,
        "description": description,
        "source_page": source_page,
        "fetched_at": fetched_at
    }

def main():
    print("--- Stage 3: Extract book details ---")
    book_entries = discover_catalogue_books()
    print(f"Discovered {len(book_entries)} unique book URLs to extract.")
    
    raw_records: List[Dict[str, Any]] = []
    for i, (book_url, source_page) in enumerate(book_entries, start=1):
        record = extract_book_raw_record(book_url, source_page)
        raw_records.append(record)
        if i % 20 == 0 or i == len(book_entries):
            print(f"Extracted {i}/{len(book_entries)} books...")

    print(f"\ndetail_pages={len(raw_records)}")
    if raw_records:
        print("\nSample complete raw record:")
        print(json.dumps(raw_records[0], indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
