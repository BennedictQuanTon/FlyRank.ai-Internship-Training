# The Polite Scraper (FlyRank Backend Track - W5-A9)

A polite, robust web scraping pipeline that extracts 60 books from the first three catalogue pages of **Books to Scrape**, normalizes raw textual data into strongly-typed numerical records, schema-validates every item with Pydantic, survives broken pages gracefully, and generates an honest run report.

---

## 🎯 Target Classification

* **Target Site:** Books to Scrape ([https://books.toscrape.com](https://books.toscrape.com))
* **Target Category:** Practice Sandbox. The site explicitly states on its homepage that it was created as a safe testing sandbox for developers learning web scraping without legal or operational risk.
* **Scope of Collection:** Exactly the first 3 catalogue pages (`page-1.html`, `page-2.html`, `page-3.html`), discovering and extracting exactly 60 individual book detail pages.
* **Data Fields Collected:**
  1. `title` (raw string)
  2. `product_url` (canonical absolute URL)
  3. `price_text` (raw text, e.g. "£51.77")
  4. `price_gbp` (normalized float, e.g. 51.77)
  5. `availability_text` (raw stock string)
  6. `rating_text` (rating word, e.g. "Three")
  7. `description` (product description or `null`)
  8. `source_page` (provenance catalogue page URL)
  9. `fetched_at` (provenance ISO-8601 timestamp)
* **Robots.txt Audit:**
  * Requested URL: `https://books.toscrape.com/robots.txt`
  * Status Code: `HTTP 404 Not Found` (no robots file found).
  * Interpretation: Under RFC 9309 (Robots Exclusion Protocol), a 404 response indicates no crawler restrictions are declared by the server. Because the site is an open educational sandbox, scraping is explicitly permitted.
* **Ethical Commitment:**
  > *"I will not reuse this code on another site without checking its rules and terms first."*

---

## 🚀 Quick Start (One Command)

```bash
cd scraper
python src/main.py
```
