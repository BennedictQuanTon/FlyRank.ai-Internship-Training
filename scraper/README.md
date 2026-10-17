# The Polite Scraper (FlyRank Backend Track - W5-A9)

A production-grade, polite web scraping pipeline that extracts 60 books across the first three catalogue pages of **Books to Scrape**, normalizes raw textual currency and availability data into strictly-typed records, validates every entity against a Pydantic schema, survives network anomalies or broken pages without crashing, and generates an honest audit report.

---

## 🎯 1. Target Classification & Robots Audit

* **Target Site:** Books to Scrape ([https://books.toscrape.com](https://books.toscrape.com))
* **Target Classification:** **Practice Sandbox**. The homepage explicitly identifies the site as a dedicated educational sandbox built specifically for developers to practice web scraping without legal risks or server harm.
* **Scope of Collection:** Exactly the first 3 catalogue pages (`page-1.html`, `page-2.html`, `page-3.html`), discovering and extracting exactly 60 unique book detail pages.
* **Robots.txt Audit:**
  * Request URL: `https://books.toscrape.com/robots.txt`
  * HTTP Status: `404 Not Found` (no robots file found).
  * Finding: Under RFC 9309, a missing robots.txt indicates no automated crawler restrictions are declared by the host. Given its educational sandbox purpose, respectful crawling is fully permitted.
* **Ethical Commitment:**
  > *"I will not reuse this code on another site without checking its rules and terms first."*

---

## 🚀 2. Quick Start (One Command)

From a fresh clone, run the pipeline with zero external service dependencies:

```bash
cd scraper
pip install -r requirements.txt
python src/main.py
```

To run the unit test suite verifying parser invariants:
```bash
pytest tests/test_parser.py -v
```

To verify fault tolerance with a deliberately broken test URL:
```bash
python src/main.py --test-broken
```

---

## 📋 3. Record Schema & Output Structure

Every record is validated with **Pydantic v2** before entering storage. Raw strings and clean values live side-by-side:

```python
class BookRecord(BaseModel):
    title: str = Field(..., min_length=1)
    product_url: str = Field(...)                    # Canonical absolute URL
    price_text: str                                  # e.g. "£51.77"
    price_gbp: float = Field(..., ge=0.0)           # e.g. 51.77
    availability_text: str                           # e.g. "In stock (22 available)"
    rating_text: Optional[str] = None               # e.g. "Three"
    description: Optional[str] = None               # null if missing (never invented)
    source_page: str                                 # Provenance: catalogue page URL
    fetched_at: str                                  # Provenance: ISO-8601 UTC timestamp
```

* Valid records are stored in: [`output/books.json`](output/books.json) (exactly 60 unique records, strictly idempotent).
* Failing or malformed records land in: [`output/errors.json`](output/errors.json).

Sample output record:
```json
{
  "title": "A Light in the Attic",
  "product_url": "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html",
  "price_text": "£51.77",
  "price_gbp": 51.77,
  "availability_text": "In stock (22 available)",
  "rating_text": "Three",
  "description": "It's hard to imagine a world without A Light in the Attic...",
  "source_page": "https://books.toscrape.com/catalogue/page-1.html",
  "fetched_at": "2026-10-17T07:11:27Z"
}
```

---

## 🛡️ 4. Politeness Rules & Resilience

1. **Identifying User-Agent:** Every HTTP request sends an honest, identifiable header:
   `User-Agent: FlyRankInternship-A9/1.0 (+https://github.com/BennedictQuanTon/todo-crud-api)`
2. **Polite Rate Limiting:** Enforces a minimum **500 ms delay** (`time.sleep(0.5)`) between live requests to Books to Scrape.
3. **Strict Timeout:** Enforces a maximum **5.0-second timeout** on every network request; calls never hang indefinitely.
4. **Local Disk Cache:** Saves responses in `cache/` (git-ignored). Repeated development runs read 100% from cache in $<0.3\text{s}$ with zero outbound requests to the server.
5. **Selective Retry Logic:**
   * `404 Not Found` / `403 Forbidden`: Never retried (asking again will not create missing pages or bypass bans).
   * `5xx Server Error` / `Timeout`: Retries once after a 1.0s backoff pause.
6. **Fault Isolation:** Each book detail page is processed in an isolated try-catch boundary; 59 good records survive 1 bad one.

---

## 📊 5. Real Run Report (`output/run-report.json`)

```json
{
  "start_time": "2026-10-17T07:13:04Z",
  "end_time": "2026-10-17T07:13:04Z",
  "duration_seconds": 0.176,
  "catalogue_pages": 3,
  "pages_fetched": 0,
  "cache_hits": 63,
  "valid_records": 60,
  "invalid_records": 0,
  "failed_pages": 0,
  "failed_details": []
}
```

*Fault Survival Test Report (`python src/main.py --test-broken`):*
```json
{
  "start_time": "2026-10-17T07:12:43Z",
  "end_time": "2026-10-17T07:12:44Z",
  "duration_seconds": 1.226,
  "catalogue_pages": 3,
  "pages_fetched": 0,
  "cache_hits": 63,
  "valid_records": 60,
  "invalid_records": 0,
  "failed_pages": 1,
  "failed_details": [
    {
      "url": "https://books.toscrape.com/catalogue/deliberately-broken-page-404_9999/index.html",
      "reason": "HTTP 404 (Not Found)"
    }
  ]
}
```

---

## 💡 6. Why No Browser Was Needed

> **Architecture Decision:** This assignment needed no headless browser because Books to Scrape is statically server-rendered; all 60 book records, prices, and descriptions are already present in the raw HTML payload returned by the server. Launching a headless browser (such as Playwright or Puppeteer) would have consumed 10x-20x more RAM and CPU cycles with zero extraction benefit.

---

## ⚠️ 7. Honest Limitation

* **Limitation:** The scraper assumes traditional server-side rendering (SSR). If the target site migrates to a client-side Single Page Application (SPA) architecture rendered exclusively via React/Vue without server-rendered markup, `requests` + `BeautifulSoup` would receive an empty shell (`<div id="root"></div>`), requiring transition to browser automation or reverse-engineering internal JSON API endpoints.

---

## ⚖️ 8. Ethics & Responsible Scraping Note

1. **API First:** Always use an official REST/GraphQL API when provided by the platform.
2. **Never Bypass Access Controls:** Never attempt to circumvent authentication gates, paywalls, CAPTCHAs, or IP bans.
3. **Minimize Footprint:** Collect only the exact fields required for the business problem; respect bandwidth by aggressively caching during development.

---

## 🤖 9. Bonus Stage: The AI Rematch (AI vs Me)

### 1. Specification Prompt Provided to the AI
> *"Build a Python web scraping pipeline using requests and BeautifulSoup for Books to Scrape (https://books.toscrape.com).*
> *Requirements:*
> *1. Crawl exactly the first 3 catalogue pages following pagination.*
> *2. Extract all 60 book detail pages collecting title, canonical product URL, raw price text, numeric price in GBP, availability, rating, and description.*
> *3. Cache all HTML pages locally so repeated runs do not hit the live site.*
> *4. Enforce polite crawling with custom User-Agent, 5s timeout, and 500ms delay between live requests.*
> *5. Validate records against a Pydantic schema; set aside invalid records in errors.json.*
> *6. Store clean records in output/books.json with strict idempotency (rerun never creates duplicates).*
> *7. Isolate page failures so broken URLs do not crash the crawl, and write an honest output/run-report.json with run metrics."*

The raw AI-generated version is quarantined in [`ai-version/main.py`](ai-version/main.py).

### 2. Checkpoint Comparison

| Verification Checkpoint | Hand-Built Pipeline | AI-Generated Version |
| :--- | :--- | :--- |
| **Discovers 60 unique URLs** | ✅ Follows dynamic `li.next a` to 3 pages (60 books) | ⚠️ Hardcoded `range(1, 4)` page loop |
| **URL Normalization** | ✅ `urllib.parse.urljoin` handles relative paths | ❌ Crude `.replace('../', '')` string manipulation |
| **Encoding & Currency** | ✅ Explicit `utf-8` decoding (`£51.77`) | ❌ Default ASCII decoding results in mojibake `Â£` |
| **Missing Description** | ✅ Gracefully returns `null` | ❌ Crashes with `AttributeError: NoneType` |
| **Local Disk Cache** | ✅ `cache/` checked first; 63 hits in $<0.3\text{s}$ | ❌ No caching; repeats 63 HTTP requests on every run |
| **Idempotent Storage** | ✅ Exactly 60 records on 1st run and reruns | ❌ Blind array append; creates duplicates on reruns |
| **Fault Tolerance & Report** | ✅ Survives fake 404; logs to `run-report.json` | ❌ Bare try-catch; no execution metrics reported |

### 3. Concrete Differences & Architectural Analysis (`git diff --no-index`)

1. **What did the AI do better — and do you understand that code?**
   * The AI used concise list comprehensions and compact soup selectors. It is fast to skim through in under 50 lines. However, that brevity came at the expense of defensive engineering.
2. **What did it get wrong or silently skip?**
   * **URL Joining:** Gluing strings manually (`BASE_URL + rel_link.replace('../', '')`) is fragile and breaks if directory depth changes. `urljoin` is the web standard.
   * **Encoding Neglect:** The AI did not set `response.encoding = 'utf-8'`, causing the British Pound symbol to corrupt into `Â£51.77`.
   * **Schema & Missing Values:** The AI did not use Pydantic. On books with no description, `find_next_sibling('p')` raised an unhandled `AttributeError`, discarding records entirely instead of storing `null`.
   * **Zero Provenance & Idempotency:** The AI omitted `source_page` and `fetched_at` timestamps, and lacked keyed deduplication to ensure reruns produce exactly 60 records.
3. **What did your prompt forget to say?**
   * The prompt forgot to specify character encoding (`utf-8`), the exact structure of cache filenames, and the specific schema for `run-report.json`. The AI silently skipped caching and run reporting altogether.

### 4. Rematch & Prompt Refinement
* **Refined Prompt:** *"Use urllib.parse.urljoin for all relative links. Explicitly decode responses as utf-8. Handle missing descriptions safely with None. Cache every HTML response using URL slugs. Key output records by canonical URL to guarantee idempotency."*
* **Outcome:** With these precise constraints, the regenerated AI scraper eliminated character corruption, handled missing descriptions safely, and respected local disk caching.

