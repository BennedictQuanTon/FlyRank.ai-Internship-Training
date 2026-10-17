"""
AI-Generated Scraper Version (Quarantined in ai-version/ for Stage Bonus comparison)
"""
import requests
from bs4 import BeautifulSoup
import json
import time

BASE_URL = "https://books.toscrape.com/catalogue/"
HEADERS = {"User-Agent": "AI-Scraper/1.0"}

def scrape_books():
    books = []
    # AI Flaw 1: Hardcoding pagination loop instead of following catalogue's dynamic next link
    for page in range(1, 4):
        url = f"{BASE_URL}page-{page}.html"
        r = requests.get(url, headers=HEADERS, timeout=10)
        # AI Flaw 2: Not setting r.encoding='utf-8', resulting in mojibake Â£
        soup = BeautifulSoup(r.text, 'html.parser')
        
        for article in soup.find_all('article', class_='product_pod'):
            rel_link = article.find('h3').find('a')['href']
            # AI Flaw 3: Crude string replacement instead of urllib.parse.urljoin
            book_url = BASE_URL + rel_link.replace('../', '')
            
            # Fetch book detail
            try:
                detail_res = requests.get(book_url, headers=HEADERS, timeout=10)
                detail_soup = BeautifulSoup(detail_res.text, 'html.parser')
                
                title = detail_soup.find('h1').text
                price_text = detail_soup.find('p', class_='price_color').text
                # AI Flaw 4: Naive float conversion that crashes on non-numeric symbols
                price_gbp = float(price_text.replace('£', ''))
                
                # AI Flaw 5: Unsafe description extraction that raises AttributeError if product_description is missing
                desc_tag = detail_soup.find('div', id='product_description')
                description = desc_tag.find_next_sibling('p').text if desc_tag else None
                
                books.append({
                    "title": title,
                    "product_url": book_url,
                    "price_text": price_text,
                    "price_gbp": price_gbp,
                    "description": description
                })
                time.sleep(0.5)
            except Exception as e:
                # Blindly skips without structured error reporting
                print(f"Failed {book_url}: {e}")

    # AI Flaw 6: Appends without canonical deduplication (not idempotent)
    with open("ai_books.json", "w") as f:
        json.dump(books, f)

if __name__ == "__main__":
    scrape_books()
