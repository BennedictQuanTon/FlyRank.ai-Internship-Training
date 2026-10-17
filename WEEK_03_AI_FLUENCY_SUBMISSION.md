# Week 3 Assignment: Map It & Give It a Face (Consistency, Not Talent)
**Track:** General AI Fluency | **Program:** FlyRank AI Internship  
**Candidate:** Bennedict Quan Ton  
**Project Track:** Backend Track (Containerized APIs & Relational Systems)  
**Deliverable URL / Repo:** `https://github.com/BennedictQuanTon/todo-crud-api`

---

## Part 1: The Through-Line (One-Line Claim & Content Map)

### 1.1 One-Line Claim Generation & Selection

#### 10 AI-Generated Claim Explorations:
1. *I build full-stack web applications with modern AI integrations.* (Too broad, vague)
2. *Backend developer passionate about scalable code and clean APIs.* (Generic, sounds like every resume)
3. *FastAPI and PostgreSQL specialist shipping high-speed microservices.* (A bit buzzword-heavy)
4. *I turn complex server architectures into simple, containerized Docker applications.* (Better, but lacks durability angle)
5. *Junior software engineer with experience across memory, SQLite, and Postgres.* (Sounds too junior/academic)
6. *I build disciplined, containerized backend APIs and database systems that survive restarts and scale predictably.* (Strong, concrete)
7. *Designing clean API contracts and rock-solid relational database migrations.* (Good, but focuses on process rather than value)
8. *Engineering backend systems where storage is an implementation detail and reliability is guaranteed.* (Intriguing, technical)
9. *Production-ready REST APIs backed by Docker, PostgreSQL, and rigorous test suites.* (Punchy, but dry)
10. *I bridge clean software design and containerized infrastructure so backends work identically on every machine.* (Strong developer survival theme)

#### Selected & Sharpened One-Line Claim:
> **"I build disciplined, containerized backend APIs and persistent database systems that run identically on every machine."**

* **Why this claim wins:** It directly addresses the core engineering truth demonstrated across our assignments: moving from memory to SQLite to containerized PostgreSQL while preserving 100% of the API contract, backing it up with Docker Compose reliability and automated tests. It is single, confident, and memorable.

---

### 1.2 Content Map & Page Architecture

**Core Goal / Primary Action (from Week 1):**  
> *"Invite me to a technical backend conversation or code review interview."*

Every page section ladders directly to this single action with clear, named CTAs.

```
┌────────────────────────────────────────────────────────────────────────┐
│ 1. Hero Section (The Hook)                                             │
│    • Headline: Selected One-Line Claim                                 │
│    • Subhead: Real shipped proof summary (Docker + FastAPI + Postgres) │
│    • Primary CTA: [Review My Code on GitHub] | Secondary: [Contact Me] │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
┌───────────────────────────────────▼────────────────────────────────────┐
│ 2. Lead Proof / Featured Case Study (Strongest Piece)                   │
│    • Title: Containerized REST Stack with Zero-Setup Orchestration     │
│    • The Problem: Moving storage without breaking external client APIs │
│    • The Architecture: FastAPI + PostgreSQL 16 + Docker Compose        │
│    • Proof Artifacts: TablePlus DB capture + 16/16 Pytest pass suite   │
│    • Section CTA: [Inspect Docker & DB Architecture]                   │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
┌───────────────────────────────────▼────────────────────────────────────┐
│ 3. Engineering Philosophy & Core Stack (The Framing)                   │
│    • Theme: "Storage is an Implementation Detail"                      │
│    • Evolution: RAM (A1) ➔ SQLite (A2) ➔ Containerized Postgres (A3)   │
│    • Key Disciplines: Parameterized queries (SQLi safety), transactions│
│    • Stack Tokens: Python 3.11, FastAPI, PostgreSQL, Docker, Pytest    │
│    • Section CTA: [View Git Stage-by-Stage History]                    │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
┌───────────────────────────────────▼────────────────────────────────────┐
│ 4. Closing Action / Conversion (The Ask)                               │
│    • Direct invitation for technical internships / junior roles        │
│    • Contact channels: Email, LinkedIn, GitHub                         │
│    • Primary Action CTA: [Schedule a Technical Chat]                   │
└────────────────────────────────────────────────────────────────────────┘
```

### 1.3 "Still Need to Gather" Checklist (Unblocking Build Week)

| Item | Proof Needed | Source / Current Status | Blocked? |
| :--- | :--- | :--- | :---: |
| **Database Screenshot** | TablePlus / psql capture showing `tasks` table with 3 rows on port 5432 | Completed (`postgres_db.jpg` in repo) | No ✅ |
| **Test Verification** | Terminal capture of `pytest -v` showing 16/16 tests passing | Completed (0.50s pass on local daemon) | No ✅ |
| **Compose Roundtrip** | Short 10s terminal recording or GIF of `docker compose down` then `up` | Command output logged; GIF to capture in Week 4 | Minor ⏳ |
| **GitHub Commit History** | Verified clean commit sequence (`≥ 6 stage commits`) | 9 staged commits verified in git log | No ✅ |
| **Professional Headshot** | High-resolution real photo with neutral background | Need to select photo file for hero | No ✅ |

---

## Part 2: Decide Once (Identity Kit & Style Note)

### 2.1 Typography
* **Heading Font:** **`Plus Jakarta Sans`** (Google Fonts) — Crisp, contemporary geometric sans-serif that conveys structural precision without feeling quirky.
  * Weights: Bold (`700`) for H1/Hero, Semi-Bold (`600`) for H2/H3.
* **Body Font:** **`Inter`** (Google Fonts) — The industry-standard neutral workhorse. Highly legible at 14px–16px on screens, excellent numerical tabular figures for benchmarks and code snippets.
  * Weights: Regular (`400`) for body paragraphs, Medium (`500`) for UI labels/buttons.

### 2.2 Color Palette

A restrained 4-color palette designed around the **Portfolio Rule**: *The design is the quiet frame, never the painting.*

| Color Role | Name | Hex Code | Contrast Ratio | Usage |
| :--- | :--- | :---: | :---: | :--- |
| **Background (Light)** | Crisp Warm White | `#F8FAFC` | Base | Page canvas and breathing room |
| **Card / Surface** | Pure White | `#FFFFFF` | Base | Content boxes framing code & screenshots |
| **Text (Near-Black)** | Slate Deep Navy | `#0F172A` | **15.8:1** (AAA) | Headings, body text, high-readability copy |
| **Muted Text / Border** | Slate Muted | `#64748B` | **4.9:1** (AA) | Metadata, timestamps, divider borders (`#E2E8F0`) |
| **Single Accent** | Emerald Terminal | `#059669` | **4.6:1** (AA on white) | Active links, primary CTA buttons, success badges |

* **Contrast & Accessibility Audit:** Text `#0F172A` on `#F8FAFC` achieves a contrast ratio of **15.8:1** (far exceeding WCAG AAA requirements). Accent `#059669` provides a clean terminal-inspired signal without clashing or shouting.

### 2.3 Logo & Favicon
* **Favicon Concept:** A minimalist terminal bracket monogram:
  ```html
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
    <rect width="32" height="32" rx="6" fill="#0F172A"/>
    <path d="M9 11L14 16L9 21" stroke="#059669" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M16 21H23" stroke="#F8FAFC" stroke-width="2.5" stroke-linecap="round"/>
  </svg>
  ```
  *(Represents prompt execution, terminal discipline, and backend craft).*

### 2.4 Two-Line Style Note (For AI Workspace Reuse)
```markdown
STYLE GUIDE: Plus Jakarta Sans (Headings, 600/700) + Inter (Body, 400/500).
PALETTE: Text #0F172A on #F8FAFC bg, Surface #FFFFFF, Borders #E2E8F0, Accent #059669.
MOOD: Utilitarian, calm, and structured. Generous whitespace (24px/32px grid). The frame stays quiet so real database captures, terminal outputs, and code diffs remain the most vivid elements on the page.
```

---

## Part 3: Kill Your Darlings (Curated Image Selection & Rejection Note)

### 3.1 Curated Image Set (Matching Content Map)

1. **Profile Identity:** Real, clear portrait photo (no AI avatar stand-in, genuine human accountability).
2. **Featured Proof 1 (Hero Case Study):** High-resolution cropped screenshot of **TablePlus** connected to PostgreSQL container (`localhost:5432`) showing the `tasks` schema and seeded records.
3. **Featured Proof 2 (Engineering Rigor):** Crisp dark-themed terminal capture of `pytest -v` confirming all 16 test cases passing in 0.50s.
4. **Infrastructure Architecture:** Clean SVG system diagram showing the Docker network bridge between the `api` service and the `db` service with the `taskdata` volume.

### 3.2 The Rejection Note (Kill Your Darlings: Judgment in Action)

> **Generated Image Explored & Rejected:**  
> We generated several conceptual hero graphics: a 3D isometric floating server cluster with glowing purple fiber-optic cables, translucent glass cubes, and futuristic particle clouds.
> 
> **Why it was ruthlessly rejected:**  
> It was textbook **"AI slop"** — visually noisy, generic, and artificial. It conveyed zero technical truth about what was actually engineered. A flashy 3D graphic steals focus from the candidate's actual work and raises immediate suspicion among senior backend engineers. 
> 
> Replacing the speculative graphic with an authentic, cropped TablePlus database query output and an honest terminal test log immediately establishes credibility: *this backend was actually built, containerized, and tested on real infrastructure.*
