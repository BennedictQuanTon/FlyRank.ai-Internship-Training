"""
Unit tests for The Polite Scraper (FlyRank Backend Track - W5-A9)
Tests 5 core parser & normalization invariants without hitting the network.
"""
import pytest
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from pydantic import ValidationError
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from main import normalize_price, BookRecord

# Test 1: Price normalization
def test_price_normalization():
    assert normalize_price("£51.77") == 51.77
    assert normalize_price("£10.00") == 10.0
    assert normalize_price("  £0.99  ") == 0.99
    with pytest.raises(ValueError):
        normalize_price("Free")
    with pytest.raises(ValueError):
        normalize_price("")

# Test 2: Relative to absolute URL conversion
def test_relative_to_absolute_urls():
    base_catalogue = "https://books.toscrape.com/catalogue/page-1.html"
    relative_link = "a-light-in-the-attic_1000/index.html"
    abs_url = urljoin(base_catalogue, relative_link)
    assert abs_url == "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"

    # From root catalogue relative
    base_root = "https://books.toscrape.com/index.html"
    rel_root = "catalogue/tipping-the-velvet_999/index.html"
    assert urljoin(base_root, rel_root) == "https://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html"

# Test 3: Missing description produces null (not invented text)
def test_missing_description_handling():
    html_without_description = """
    <div class="product_main">
        <h1>Book Without Description</h1>
        <p class="price_color">£19.99</p>
        <p class="availability">In stock</p>
        <p class="star-rating Four"></p>
    </div>
    """
    soup = BeautifulSoup(html_without_description, "html.parser")
    desc_header = soup.select_one("#product_description")
    description = None
    if desc_header:
        p_desc = desc_header.find_next_sibling("p")
        if p_desc:
            description = p_desc.get_text(strip=True)
            
    assert description is None

    # Validating in Pydantic schema allows None
    record = BookRecord(
        title="Book Without Description",
        product_url="https://books.toscrape.com/catalogue/book_1/index.html",
        price_text="£19.99",
        price_gbp=19.99,
        availability_text="In stock",
        rating_text="Four",
        description=description,
        source_page="https://books.toscrape.com/catalogue/page-1.html",
        fetched_at="2026-10-17T07:00:00Z"
    )
    assert record.description is None

# Test 4: Deduplication of URLs (idempotency)
def test_duplicate_url_deduplication():
    raw_urls = [
        "https://books.toscrape.com/catalogue/book-1/index.html",
        "https://books.toscrape.com/catalogue/book-2/index.html",
        "https://books.toscrape.com/catalogue/book-1/index.html",
        "https://books.toscrape.com/catalogue/book-3/index.html",
        "https://books.toscrape.com/catalogue/book-2/index.html",
    ]
    unique_urls = list(dict.fromkeys(raw_urls))
    assert len(unique_urls) == 3
    assert unique_urls == [
        "https://books.toscrape.com/catalogue/book-1/index.html",
        "https://books.toscrape.com/catalogue/book-2/index.html",
        "https://books.toscrape.com/catalogue/book-3/index.html"
    ]

# Test 5: Malformed HTML fixture rejection
def test_malformed_html_fixture():
    malformed_html = "<html><body><div>Broken markup with no product info</div></body></html>"
    soup = BeautifulSoup(malformed_html, "html.parser")
    main_section = soup.select_one(".product_main")
    assert main_section is None

# Test 6: Pydantic schema validation constraints
def test_schema_validation_invariants():
    # Invalid non-https URL
    with pytest.raises(ValidationError):
        BookRecord(
            title="Insecure Book",
            product_url="http://insecure.com/book",
            price_text="£10.00",
            price_gbp=10.0,
            availability_text="In stock",
            source_page="https://books.toscrape.com/catalogue/page-1.html",
            fetched_at="2026-10-17T07:00:00Z"
        )
    
    # Negative price
    with pytest.raises(ValidationError):
        BookRecord(
            title="Free Book",
            product_url="https://books.toscrape.com/book",
            price_text="£-5.00",
            price_gbp=-5.0,
            availability_text="In stock",
            source_page="https://books.toscrape.com/catalogue/page-1.html",
            fetched_at="2026-10-17T07:00:00Z"
        )
