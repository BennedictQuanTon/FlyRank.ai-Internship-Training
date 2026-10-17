# Week 6 · Explain It Like You Built It (`#explain-it-like-you-built-it`)
**Track:** General AI Fluency — Week 6 Assignment  
**Program:** FlyRank AI Internship  
**Candidate:** Long Quan (Bennedict) Ton (`@BennedictQuanTon`)  
**Role:** Backend Systems & Applied AI Engineer  
**Repository:** [BennedictQuanTon/todo-crud-api](https://github.com/BennedictQuanTon/todo-crud-api)  
**Deliverable File:** [`EXPLAIN_IT_LIKE_YOU_BUILT_IT.md`](EXPLAIN_IT_LIKE_YOU_BUILT_IT.md)  
**Live Site URL:** [https://bennedictquanton.github.io/todo-crud-api/](https://bennedictquanton.github.io/todo-crud-api/)

---

## 🧭 Submission Summary for Reviewers

### 1. The Chosen Part of the Build
- **Target File:** [`portfolio/index.html`](portfolio/index.html#L148-L154) (and [`index.html`](index.html#L148-L154))
- **Concrete Code Snippet:**
  ```css
  .specs-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 16px;
  }
  ```
- **Context:** Responsive layout of the system architecture specifications and case studies without any `@media` query breakpoints.

### 2. The Plain-Words Explanation (As Taught to a Non-Technical Friend)
> "Imagine an expandable wooden dining table where you place plates for guests. You set one simple house rule: *'Every plate needs at least 200cm of elbow room, but no plate should ever feel crowded.'*
> 
> On a tiny phone screen (a café table for one), only one plate fits, so that guest gets the entire table surface comfortably. On a huge desktop monitor (a grand banquet table), the table automatically counts: *'I have 800cm of space—that fits three 200cm plates with room to spare.'* Then, instead of leaving empty ghost gaps on the right side, the plates expand like accordions so they balance evenly and fill the entire beautiful spread.
> 
> That whole intelligent behavior is governed by one line of CSS: `grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));`. It tells the browser to fit as many cards as safely possible (at least 200px each), and stretch them equally whenever there's leftover room."

### 3. Human in the Loop Proof (Tutor Quiz Validation)
- **Edge Case 1 (350px Viewport):** Calculated available width (318px). Since 2 cards require 416px, the browser computes exactly 1 column, and `1fr` expands it to 318px.
- **Edge Case 2 (`auto-fit` vs `auto-fill`):** Understood that `auto-fit` collapses empty ghost tracks and distributes leftover space to actual content, whereas `auto-fill` preserves empty phantom tracks.

---

## 📋 Copy-Paste Information for FlyRank Portal

### 🔗 Deliverable links:
```text
https://github.com/BennedictQuanTon/todo-crud-api/blob/main/EXPLAIN_IT_LIKE_YOU_BUILT_IT.md
https://bennedictquanton.github.io/todo-crud-api/
https://github.com/BennedictQuanTon/todo-crud-api
```

### 📝 Notes:
```text
Week 6 Deliverable: Explain It Like You Built It (#explain-it-like-you-built-it).

1. Real piece of build chosen:
Selected the CSS Grid fluid layout in portfolio/index.html (lines 148-154):
`grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));`
which powers the responsive case studies and tech spec cards without a single media query.

2. Tutor Mode & Learning Process:
Conducted a dedicated AI tutor session breaking down repeat(), auto-fit vs auto-fill, and minmax(200px, 1fr). Completed a 2-question quiz verifying edge-case calculations (350px mobile screen column budget and empty track collapse on 1200px displays).

3. Plain-words explanation:
Authored an intuitive explanation using the "expandable dining table" analogy, explaining how elbow room constraints and accordion stretching eliminate rigid breakpoint hacks.

Complete documentation, tutor transcript, and verification checklist committed to:
https://github.com/BennedictQuanTon/todo-crud-api/blob/main/EXPLAIN_IT_LIKE_YOU_BUILT_IT.md
```
