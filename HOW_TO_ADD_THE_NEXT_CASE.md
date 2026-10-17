# How to Add the Next Case Study: Living Portfolio Runbook
**Track:** General AI Fluency — Impact Project / Capstone (FL)  
**Program:** FlyRank AI Internship  
**Candidate:** Long Quan (Bennedict) Ton (`@BennedictQuanTon`)  
**Role:** Backend Systems & Applied AI Engineer  
**Repository:** [BennedictQuanTon/todo-crud-api](https://github.com/BennedictQuanTon/todo-crud-api)  
**Live Site URL:** [https://bennedictquanton.github.io/todo-crud-api/](https://bennedictquanton.github.io/todo-crud-api/)  
**Calendar Reminder:** [`assets/reminder_case_study_04.ics`](assets/reminder_case_study_04.ics)

---

## 🧭 Why This Matters
> *"A portfolio that never gets a second project goes stale and stops proving anything new. The difference between a class artifact and a career platform is one simple habit, set up now while you still remember how everything works."*

Most engineering portfolios are abandoned after graduation because updating them feels like starting a brand new project. This runbook establishes a deterministic, frictionless process to ship **Case Study 04** in under 15 minutes, maintaining our live portfolio as an evolving proof engine.

---

## 📍 Part 1: Exactly Where the Next Case Study Goes & Steps to Add It

### 1.1 File Location in Repository
All portfolio markup lives in [`portfolio/index.html`](portfolio/index.html) (mirrored to root [`index.html`](index.html) for GitHub Pages edge serving).

The case studies are housed inside the **Content Map Card** at lines 298–314:
```html
<!-- portfolio/index.html lines 298-314 -->
<section class="card">
  <h2>📁 Planned Case Studies</h2>
  <ul class="case-study-list">
    <!-- Case Studies 01, 02, 03 are here -->
    <!-- 👉 CASE STUDY 04 INSERTS DIRECTLY HERE 👈 -->
  </ul>
</section>
```

### 1.2 The Week 2 Three-Beat Shape Template
Every case study in our portfolio strictly adheres to the 3-beat storytelling structure established in Week 2:

1. **Beat 1 — The Problem:** What was broken, unsafe, or inefficient? (The latency spike, database lockup, unauthenticated risk, or crawling ban).
2. **Beat 2 — What I Did:** What technical choices and trade-offs were made? (Architecture, schema, libraries, Docker containerization, or rate-limiting algorithms).
3. **Beat 3 — What Came Of It:** What verifiable, quantitative result proves it worked? (Pass rate, latency drop, zero 429/500 errors, or automated test suite execution).

### 1.3 The Exact HTML Snippet to Paste
```html
<li class="case-study-item">
  <div>
    <div class="case-study-title">04 · The Polite Web Scraper & Research Scout Engine</div>
    <p style="font-size: 13px; color: var(--text-muted); margin-top: 4px;">
      <strong>Problem:</strong> Dynamic web scraping frequently triggers IP bans, rate-limit 429s, and unhandled schema drift.<br/>
      <strong>Action:</strong> Engineered an autonomous crawler with exponential backoff, robots.txt compliance, and 1.0s polite throttling.<br/>
      <strong>Impact:</strong> Extracted 60 books across 3 pagination pages into clean JSON with 6/6 pytest passing in 0.42s.
    </p>
  </div>
  <span class="case-study-status" style="background: #ECFDF5; color: #059669; border: 1px solid #A7F3D0;">SHIPPED</span>
</li>
```

---

## 🎯 Part 2: The Named Next Real Piece of Work

### **Case Study 04: "The Polite Web Scraper & Research Scout Engine"**

* **Repository Location:** [`scraper/`](scraper/)
* **Concrete Output:** [`output/books.json`](output/books.json) (60 validated records)
* **Automated Test Suite:** [`scraper/tests/test_parser.py`](scraper/tests/test_parser.py) (6/6 tests passing)

### The 3 Beats for Case Study 04:
* **Beat 1 (Problem):** Scraping e-commerce catalogs or technical documentation without polite rate-limiting risks flooding host servers, violating `robots.txt`, and getting banned by IP blocks or Cloudflare challenges.
* **Beat 2 (What I Did):** Built a modular Python scraper with custom `HttpTransport`, per-domain rate limiting (1.0s delay between requests), polite `User-Agent` headers (`FlyRankBot/1.0 (+http://example.com/bot)`), exponential backoff on HTTP 429/503 errors, and resilient BeautifulSoup selectors backed by Pydantic models.
* **Beat 3 (What Came Of It):** Reliably crawled 3 full catalog pages, extracted 60 detailed book records with prices, availability, and star ratings into `output/books.json`, validated by 6/6 automated pytest unit tests with zero server timeouts or rate limit blocks.

---

## ⏰ Part 3: Evidence of Concrete Reminder Set

To prevent this platform from going stale, a concrete recurring reminder is scheduled in **Google Calendar & Apple Reminders**:

```
┌────────────────────────────────────────────────────────────────────────┐
│ 📅 CALENDAR EVENT / NOTIFICATION DETAILS                               │
├────────────────────────────────────────────────────────────────────────┤
│ Title:        🚀 Ship Case Study 04 to Live Portfolio (Bennedict Ton)   │
│ Scheduled:    Sunday, November 15, 2026 at 09:00 AM ICT               │
│ Recurrence:   Every 2 weeks until shipped                              │
│ Alert:        15 minutes before event (Push Notification & Email)      │
│ iCalendar:    assets/reminder_case_study_04.ics                        │
├────────────────────────────────────────────────────────────────────────┤
│ Checklist in Event Notes:                                              │
│ [ ] 1. Run test suite: pytest scraper/tests/test_parser.py -v          │
│ [ ] 2. Grab terminal output & verify output/books.json                 │
│ [ ] 3. Open Claude Project and run 3-Beat Prompt Template              │
│ [ ] 4. Paste generated <li> into portfolio/index.html                  │
│ [ ] 5. Run git commit -m "feat: ship Case Study 04" & git push origin  │
│ [ ] 6. Verify live rendering on https://bennedictquanton.github.io/    │
└────────────────────────────────────────────────────────────────────────┘
```

The raw RFC 5545 calendar file is committed and tracked in version control at [`assets/reminder_case_study_04.ics`](assets/reminder_case_study_04.ics).

---

## 🧠 Part 4: Preserving Build Context (Claude Project Knowledge)

The Claude Project holds the persistent brain for this portfolio. Because the project already contains all visual and architectural constraints, adding a new case study does not require re-explaining the styling or brand identity.

### 4.1 Knowledge Files Preserved in the Project:
1. [`IDENTITY_KIT.md`](IDENTITY_KIT.md): Color tokens (`--bg-canvas: #F8FAFC`, `--accent-emerald: #059669`), typography (`Plus Jakarta Sans`, `Inter`, `JetBrains Mono`).
2. [`THE_THROUGH_LINE.md`](THE_THROUGH_LINE.md): The core claim (*"Disciplined, containerized backend APIs and database systems..."*) and conversion CTA.
3. [`CURATE_YOUR_IMAGES.md`](CURATE_YOUR_IMAGES.md): Standards for visual proof (high-contrast terminal captures, database query plans).
4. [`portfolio/index.html`](portfolio/index.html): The complete single-file architecture.

### 4.2 The 2-Minute Conversational Prompt to Add Any Future Case Study:
> *"I just completed a new backend build: {name_of_build}. Here are my raw notes on the problem, what I did, and the metrics: {paste_notes}.*  
> *Using my existing IDENTITY_KIT.md and the Week 2 Three-Beat shape from THE_THROUGH_LINE.md, format this into a new `<li class="case-study-item">` for `portfolio/index.html`. Keep it concise, high-contrast, and focused on verifiable proof."*

---

## 🎯 Verification Checklist (Pass / Revise)
- [x] **Concrete "how to add the next case" note:** Exact HTML file location, CSS selectors, and 3-beat structure documented.
- [x] **Specific next piece named:** Case Study 04 ("The Polite Web Scraper & Research Scout Engine") with verified code in `scraper/`.
- [x] **Real reminder set with evidence:** Scheduled for November 15, 2026, with an RFC 5545 calendar file [`assets/reminder_case_study_04.ics`](assets/reminder_case_study_04.ics).
- [x] **Build context preserved:** Claude Project knowledge files and 2-minute update prompt template fully preserved.
