# The Through-Line: Map Content & CTAs
**Track:** General AI Fluency — Week 3 Assignment (`#the-through-line`)  
**Program:** FlyRank AI Internship  
**Candidate:** Long Quan Ton (Bennedict) — `tonlongquanvn@gmail.com`  
**Track Focus:** Backend Systems Engineering  
**Repository:** [BennedictQuanTon/todo-crud-api](https://github.com/BennedictQuanTon/todo-crud-api)

---

## 1. The One-Line Claim

### 1.1 Ten AI-Generated Claim Explorations:
1. *I build full-stack web applications and scalable APIs with Python.* (Too broad, generic)
2. *Passionate software engineer building high-performance microservices.* (Vague resume filler)
3. *FastAPI and PostgreSQL specialist shipping database-backed backends.* (Buzzwordy)
4. *I turn complex architectures into containerized Docker applications.* (Lacks durability proof)
5. *Junior developer with experience across in-memory, SQLite, and Postgres.* (Sounds too junior)
6. *I build disciplined, containerized backend APIs and database systems that survive restarts and scale predictably.* (Strong, concrete)
7. *Designing clean API contracts and rock-solid relational database migrations.* (Focuses on process rather than value)
8. *Engineering backend systems where storage is an implementation detail and reliability is guaranteed.* (Technical, intriguing)
9. *Production-ready REST APIs backed by Docker, PostgreSQL, and rigorous test suites.* (A bit dry)
10. *I bridge clean software design and containerized infrastructure so backends work identically on every machine.* (Strong developer survival theme)

### 1.2 Selected & Sharpened One-Line Claim:
> **"I build disciplined, containerized backend APIs and persistent database systems that run identically on every machine."**

* **Why this claim wins:** It is a single, memorable sentence that directly encapsulates the progression demonstrated in our assignments: starting from an in-memory list, migrating to SQLite, and advancing to a containerized PostgreSQL stack with Docker Compose—all while preserving 100% of the API contract and backing it with automated tests.

---

## 2. The Content Map (Site Architecture, Cases & CTAs)

### Primary Goal / The One Action (from Chapter 1):
> **"Invite me to a technical backend conversation or code review interview."**

Every page, section, and case study below ladders directly up to this single conversion goal.

```
┌────────────────────────────────────────────────────────────────────────┐
│ PAGE 1: HOME / PORTFOLIO OVERVIEW                                      │
├────────────────────────────────────────────────────────────────────────┤
│ Section 1: Hero & Value Proposition                                    │
│   • Claim: "I build disciplined, containerized backend APIs..."        │
│   • Proof Pill: 1-Command Docker Compose | PostgreSQL | FastAPI        │
│   • Named CTA: [Review My Code on GitHub]                              │
├────────────────────────────────────────────────────────────────────────┤
│ Section 2: Lead Proof — Containerized REST Stack (Strongest Piece)    │
│   • Case Placement: Assignment A3 (PostgreSQL in Docker Compose)       │
│   • The Problem: Moving storage without breaking client API contracts │
│   • The Solution: FastAPI + PostgreSQL 16 + Healthcheck + Named Volume │
│   • Live Proof: Real TablePlus capture (localhost:5432)                │
│   • Named CTA: [Inspect Docker & DB Architecture]                      │
├────────────────────────────────────────────────────────────────────────┤
│ Section 3: Supporting Proof — Storage Evolution & Test Rigor          │
│   • Case Placement: Assignment A1 & A2 (Memory ➔ SQLite ➔ Postgres)    │
│   • Core Thesis: "Storage is just an implementation detail"           │
│   • Proof: 16/16 Pytest suite passing across all storage swaps in 0.50s│
│   • Named CTA: [Explore 9-Stage Git Commit History]                    │
├────────────────────────────────────────────────────────────────────────┤
│ Section 4: Engineering Discipline & Core Stack                         │
│   • Philosophy: Parameterized queries (SQLi safety), transactions     │
│   • Stack: Python 3.11, FastAPI, PostgreSQL, Docker, Pytest, psycopg   │
│   • Named CTA: [View Technical Architecture Note]                      │
├────────────────────────────────────────────────────────────────────────┤
│ Section 5: Closing Conversion (The Direct Ask)                         │
│   • Message: Open for backend software engineering intern/junior roles │
│   • Primary Action CTA: [Schedule a Technical Chat / Email Me]         │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 3. "Still Need to Gather" Honest Checklist

This honest inventory ensures that the upcoming build week (Week 4 & 5) is completely unblocked.

| Proof Artifact | Description / Technical Need | Current Status | Unblocked? |
| :--- | :--- | :---: | :---: |
| **Database Verification Capture** | High-res TablePlus screenshot showing `tasks` table with live rows on port 5432 | Completed & committed (`postgres_db.jpg`) | Yes ✅ |
| **Automated Test Log** | Terminal capture of `pytest -v` confirming 16/16 test passes in 0.50s | Verified live on local PostgreSQL container | Yes ✅ |
| **Commit Trajectory Evidence** | Git log showing clean, disciplined stage commits ($\ge 6$ required) | 9 sequential commits verified in git history | Yes ✅ |
| **Live Docker Walkthrough GIF** | 10-second screen capture demonstrating `docker compose down` then `up` with data persistence | Logs verified; recording tool ready for build week | Yes ✅ |
| **Professional Headshot** | High-resolution portrait photograph with natural lighting | Ready to link in static asset folder | Yes ✅ |
| **Internship Testimonial / Review** | Mid-term feedback quote from FlyRank mentor / peer reviewer | Scheduled for Week 6 | In Progress ⏳ |

---

## 4. Pass / Revise Criteria Self-Audit

- [x] **A single, memorable claim, not a paragraph:** Precisely 1 sentence, focused on containerized reliability and persistence.
- [x] **Every page has ordered sections and a named call to action; strongest work leads:** Flow starts with Hero, immediately leads into our strongest piece (A3 Docker Stack), followed by test rigor, and ends with closing conversion.
- [x] **The calls to action ladder up to the one action from Chapter 1:** Every button (`[Review Code]`, `[Inspect DB]`, `[Schedule Chat]`) drives the visitor toward initiating a technical conversation.
- [x] **The gather-list is honest so build week isn't blocked:** Explicitly identifies what is already captured and what remains for the build phase.
