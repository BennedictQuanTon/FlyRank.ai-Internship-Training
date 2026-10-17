"""
The Polite Scraper - Books to Scrape (FlyRank Backend Track - W5-A9)
Stage 4: Clean, schema-validate (Pydantic), and store normalized records (idempotent)
"""
import os
import sys
import time
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel, Field, field_validator, ValidationError
from typing import List, Dict, Any, Optional, Tuple

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
CACHE_DIR = BASE_DIR / "cache"
OUTPUT_DIR = BASE_DIR / "output"
CACHE_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

USER_AGENT = "FlyRankInternship-A9/1.0 (+https://github.com/BennedictQuanTon/todo-crud-api)"
START_URL = "https://books.toscrape.com/catalogue/page-1.html"
TIMEOUT_SECONDS = 5.0
POLITE_DELAY_SECONDS = 0.5
MAX_CATALOGUE_PAGES = 3

class BookRecord(BaseModel):
    """
    Schema definition for a validated, normalized book record.
    """
    title: str = Field(..., min_length=1, description="Book title")
    product_url: str = Field(..., description="Canonical absolute product URL")
    price_text: str = Field(..., description="Raw price string including currency symbol")
    price_gbp: float = Field(..., ge=0.0, description="Normalized numeric price in GBP")
    availability_text: str = Field(..., description="Raw stock availability string")
    rating_text: Optional[str] = Field(None, description="Star rating word: One, Two, Three, Four, Five")
    description: Optional[str] = Field(None, description="Book description, or null if missing")
    source_page: str = Field(..., description="Provenance: catalogue page URL where discovered")
    fetched_at: str = Field(..., description="Provenance: ISO-8601 UTC timestamp")

    @field_validator("product_url", "source_page")
    def validate_https_url(cls, value: str) -> str:
        if not value.startswith("https://"):
            raise ValueError(f"URL must start with https://, got: {value}")
        return value

def normalize_price(price_text: str) -> float:
    """
    Normalizes '£51.77' into float 51.77.
    """
    # Remove currency symbols and non-numeric chars except period
    cleaned = re.sub(r"[^\d.]", "", price_text)
    if not cleaned:
        raise ValueError(f"Cannot parse price from '{price_text}'")
    return float(cleaned)

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
    Crawls exactly max_pages of the catalogue following pagination.
    """
    discovered: List[Tuple[str, str]] = []
    current_url = start_url
    pages_crawled = 0

    while current_url and pages_crawled < max_pages:
        pages_crawled += 1
        cache_file = CACHE_DIR / f"catalogue-page-{pages_crawled}.html"
        
        html, is_cache_hit = fetch_page(current_url, cache_file)
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
    Fetches (or loads from cache) the detail page and extracts the raw fields.
    """
    slug = product_url.strip("/").split("/")[-2] if "/" in product_url else "unknown"
    cache_file = CACHE_DIR / f"book-{slug}.html"
    
    html, is_cache_hit = fetch_page(product_url, cache_file)
    if not is_cache_hit:
        time.sleep(POLITE_DELAY_SECONDS)

    soup = BeautifulSoup(html, "html.parser")
    main_section = soup.select_one(".product_main")
    
    title_tag = main_section.select_one("h1") if main_section else None
    title = title_tag.get_text(strip=True) if title_tag else ""
    
    price_tag = main_section.select_one(".price_color") if main_section else None
    price_text = price_tag.get_text(strip=True) if price_tag else ""
    
    avail_tag = main_section.select_one(".availability") if main_section else None
    availability_text = avail_tag.get_text(strip=True) if avail_tag else ""
    
    rating_text = None
    if main_section:
        star_tag = main_section.select_one(".star-rating")
        if star_tag:
            classes = star_tag.get("class", [])
            rating_candidates = [c for c in classes if c != "star-rating"]
            if rating_candidates:
                rating_text = rating_candidates[0]
                
    desc_header = soup.select_one("#product_description")
    description = None
    if desc_header:
        p_desc = desc_header.find_next_sibling("p")
        if p_desc:
            description = p_desc.get_text(strip=True)

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

def process_and_store_books():
    """
    Executes the crawl, normalization, schema validation, and storage.
    Ensures idempotency (running twice produces the same 60 records).
    """
    book_entries = discover_catalogue_books()
    
    # Store by canonical product_url to prevent duplicates
    valid_records_map: Dict[str, Dict[str, Any]] = {}
    error_records: List[Dict[str, Any]] = []

    for book_url, source_page in book_entries:
        raw = extract_book_raw_record(book_url, source_page)
        try:
            price_gbp = normalize_price(raw["price_text"])
            validated_item = BookRecord(
                title=raw["title"],
                product_url=raw["product_url"],
                price_text=raw["price_text"],
                price_gbp=price_gbp,
                availability_text=raw["availability_text"],
                rating_text=raw["rating_text"],
                description=raw["description"],
                source_page=raw["source_page"],
                fetched_at=raw["fetched_at"]
            )
            # Idempotent map insert keyed by canonical URL
            valid_records_map[validated_item.product_url] = validated_item.model_dump()
        except (ValueError, ValidationError) as exc:
            error_records.append({
                "record": raw,
                "error": str(exc)
            })

    # Write output/books.json
    books_file = OUTPUT_DIR / "books.json"
    ordered_books = list(valid_records_map.values())
    books_file.write_text(json.dumps(ordered_books, indent=2, ensure_ascii=False), encoding="utf-8")

    # Write output/errors.json if any
    errors_file = OUTPUT_DIR / "errors.json"
    errors_file.write_text(json.dumps(error_records, indent=2, ensure_ascii=False), encoding="utf-8")

    return ordered_books, error_records

def main():
    print("--- Stage 4: Validate normalized records ---")
    books, errors = process_and_store_books()
    print(f"Validated and stored {len(books)} records in output/books.json")
    print(f"Validation errors set aside: {len(errors)} records in output/errors.json")
    
    # Verify checkpoint conditions
    assert len(books) == 60, f"Expected 60 records, got {len(books)}"
    assert all(isinstance(b["price_gbp"], (int, float)) for b in books), "Every price_gbp must be a number"
    assert all(b["product_url"].startswith("https://") for b in books), "Every URL must start with https://"
    print("\nCheckpoint passed: books.json has exactly 60 records, price_gbp is numeric, URLs start with https://.")

if __name__ == "__main__":
    main()
