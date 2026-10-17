"""
The Polite Scraper - Books to Scrape (FlyRank Backend Track - W5-A9)
Stage 5: Fault tolerance (survive failures), retry rules, and run reporting
"""
import os
import sys
import time
import json
import re
import argparse
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

FAKE_BROKEN_URL = "https://books.toscrape.com/catalogue/deliberately-broken-page-404_9999/index.html"

# Run stats tracker
class RunStats:
    def __init__(self):
        self.start_time = datetime.now(timezone.utc)
        self.end_time = None
        self.catalogue_pages = 0
        self.pages_fetched = 0
        self.cache_hits = 0
        self.valid_records = 0
        self.invalid_records = 0
        self.failed_pages = 0
        self.failures: List[Dict[str, str]] = []

    def finish(self) -> Dict[str, Any]:
        self.end_time = datetime.now(timezone.utc)
        duration = (self.end_time - self.start_time).total_seconds()
        return {
            "start_time": self.start_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "end_time": self.end_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "duration_seconds": round(duration, 3),
            "catalogue_pages": self.catalogue_pages,
            "pages_fetched": self.pages_fetched,
            "cache_hits": self.cache_hits,
            "valid_records": self.valid_records,
            "invalid_records": self.invalid_records,
            "failed_pages": self.failed_pages,
            "failed_details": self.failures
        }

class BookRecord(BaseModel):
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
    cleaned = re.sub(r"[^\d.]", "", price_text)
    if not cleaned:
        raise ValueError(f"Cannot parse price from '{price_text}'")
    return float(cleaned)

def fetch_page_with_retry(url: str, cache_path: Path, stats: RunStats, timeout: float = TIMEOUT_SECONDS) -> Tuple[str, bool]:
    """
    Polite fetcher with disk cache and professional retry logic:
    - 404 / 403: Never retry (do not hammer unresolvable or forbidden endpoints).
    - Timeout / 5xx: Wait 1s and retry ONCE.
    """
    if cache_path.exists():
        content = cache_path.read_text(encoding="utf-8")
        stats.cache_hits += 1
        return content, True

    headers = {"User-Agent": USER_AGENT}
    max_attempts = 2

    for attempt in range(1, max_attempts + 1):
        try:
            response = requests.get(url, headers=headers, timeout=timeout)
            
            # Explicit non-retryable 4xx handling
            if response.status_code in (404, 403):
                raise RuntimeError(f"HTTP {response.status_code} ({'Not Found' if response.status_code == 404 else 'Forbidden'})")
            
            if response.status_code != 200:
                # 5xx or unexpected status
                if attempt < max_attempts:
                    print(f"[RETRY] {url} returned HTTP {response.status_code}. Retrying in 1s (attempt {attempt}/{max_attempts})...")
                    time.sleep(1.0)
                    continue
                raise RuntimeError(f"HTTP {response.status_code}")

            response.encoding = "utf-8"
            html = response.text
            cache_path.write_text(html, encoding="utf-8")
            stats.pages_fetched += 1
            return html, False

        except (requests.Timeout, requests.ConnectionError) as e:
            if attempt < max_attempts:
                print(f"[RETRY] Network timeout/error on {url}. Retrying in 1s (attempt {attempt}/{max_attempts})...")
                time.sleep(1.0)
                continue
            raise RuntimeError(f"Network failure after {max_attempts} attempts: {e}")

    raise RuntimeError(f"Failed to fetch {url} after {max_attempts} attempts")

def discover_catalogue_books(stats: RunStats, start_url: str = START_URL, max_pages: int = MAX_CATALOGUE_PAGES) -> List[Tuple[str, str]]:
    discovered: List[Tuple[str, str]] = []
    current_url = start_url
    pages_crawled = 0

    while current_url and pages_crawled < max_pages:
        pages_crawled += 1
        cache_file = CACHE_DIR / f"catalogue-page-{pages_crawled}.html"
        
        html, is_cache_hit = fetch_page_with_retry(current_url, cache_file, stats)
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

    stats.catalogue_pages = pages_crawled
    seen = set()
    unique: List[Tuple[str, str]] = []
    for item in discovered:
        if item[0] not in seen:
            seen.add(item[0])
            unique.append(item)
    return unique

def extract_book_raw_record(product_url: str, source_page: str, stats: RunStats) -> Dict[str, Any]:
    slug = product_url.strip("/").split("/")[-2] if "/" in product_url else "unknown"
    cache_file = CACHE_DIR / f"book-{slug}.html"
    
    html, is_cache_hit = fetch_page_with_retry(product_url, cache_file, stats)
    if not is_cache_hit:
        time.sleep(POLITE_DELAY_SECONDS)

    soup = BeautifulSoup(html, "html.parser")
    main_section = soup.select_one(".product_main")
    if not main_section:
        raise ValueError(f"Malformed book detail page: '.product_main' not found in {product_url}")
    
    title_tag = main_section.select_one("h1")
    title = title_tag.get_text(strip=True) if title_tag else ""
    
    price_tag = main_section.select_one(".price_color")
    price_text = price_tag.get_text(strip=True) if price_tag else ""
    
    avail_tag = main_section.select_one(".availability")
    availability_text = avail_tag.get_text(strip=True) if avail_tag else ""
    
    rating_text = None
    star_tag = main_section.select_one(".star-rating")
    if star_tag:
        classes = star_tag.get("class", [])
        candidates = [c for c in classes if c != "star-rating"]
        if candidates:
            rating_text = candidates[0]
            
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

def run_pipeline(inject_broken_url: bool = False) -> Dict[str, Any]:
    stats = RunStats()
    book_entries = discover_catalogue_books(stats)

    # Optional demonstration of fault survival
    if inject_broken_url:
        print(f"[TEST] Injecting 1 deliberately broken test URL: {FAKE_BROKEN_URL}")
        # Insert broken URL in the middle of valid URLs
        book_entries.insert(5, (FAKE_BROKEN_URL, "https://books.toscrape.com/catalogue/page-1.html"))

    valid_records_map: Dict[str, Dict[str, Any]] = {}
    error_records: List[Dict[str, Any]] = []

    for book_url, source_page in book_entries:
        try:
            raw = extract_book_raw_record(book_url, source_page, stats)
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
            valid_records_map[validated_item.product_url] = validated_item.model_dump()
            stats.valid_records += 1
        except Exception as exc:
            # Fault isolation: One broken page must not kill the run!
            stats.failed_pages += 1
            stats.failures.append({"url": book_url, "reason": str(exc)})
            print(f"[SKIPPED BROKEN PAGE] {book_url} -> {exc}")

    # Write output/books.json
    books_file = OUTPUT_DIR / "books.json"
    ordered_books = list(valid_records_map.values())
    books_file.write_text(json.dumps(ordered_books, indent=2, ensure_ascii=False), encoding="utf-8")

    # Write output/errors.json
    errors_file = OUTPUT_DIR / "errors.json"
    errors_file.write_text(json.dumps(error_records, indent=2, ensure_ascii=False), encoding="utf-8")

    # Write output/run-report.json
    report_data = stats.finish()
    report_file = OUTPUT_DIR / "run-report.json"
    report_file.write_text(json.dumps(report_data, indent=2, ensure_ascii=False), encoding="utf-8")

    return report_data

def main():
    parser = argparse.ArgumentParser(description="The Polite Scraper")
    parser.add_argument("--test-broken", action="store_true", help="Inject 1 deliberately broken URL to test fault tolerance")
    args = parser.parse_args()

    # If run in default or test mode
    inject_broken = args.test_broken or ("--test-broken" in sys.argv)
    
    print("--- Stage 5: Survive failures and report the run ---")
    report = run_pipeline(inject_broken_url=inject_broken)
    
    books_file = OUTPUT_DIR / "books.json"
    books = json.loads(books_file.read_text(encoding="utf-8"))
    
    print(f"\nRun Complete in {report['duration_seconds']}s:")
    print(f"- Catalogue pages: {report['catalogue_pages']}")
    print(f"- Cache hits: {report['cache_hits']}")
    print(f"- Pages fetched: {report['pages_fetched']}")
    print(f"- Valid books in books.json: {len(books)}")
    print(f"- Failed pages: {report['failed_pages']}")
    print(f"- Full report written to: {OUTPUT_DIR / 'run-report.json'}")

if __name__ == "__main__":
    main()
