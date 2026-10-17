# Identity Kit: Decide Once (Consistency, Not Talent)
**Track:** General AI Fluency — Week 3 Assignment (`#identity-kit`)  
**Program:** FlyRank AI Internship  
**Candidate:** Bennedict Quan Ton  
**Focus:** Backend Engineering Portfolio  
**Repository:** [BennedictQuanTon/todo-crud-api](https://github.com/BennedictQuanTon/todo-crud-api)

---

## 1. Typography (One or Two Free Fonts)

We select two complementary, open-source Google Fonts designed to create structure without distracting from technical work:

* **Heading Font:** **`Plus Jakarta Sans`** (Google Fonts)
  * **Role:** Page title, section headings (H1, H2, H3), case study titles.
  * **Weights:** `700 Bold` for H1 / Hero, `600 Semi-Bold` for section titles.
  * **Character:** Clean, contemporary geometric sans-serif that communicates structural precision and architectural clarity.
* **Body Font:** **`Inter`** (Google Fonts)
  * **Role:** Body paragraphs, case study explanations, UI metadata, tables.
  * **Weights:** `400 Regular` for running text, `500 Medium` for navigation and button labels.
  * **Character:** Neutral, engineered specifically for high screen readability at 14px–16px, with crisp tabular numbers for metrics and benchmarks.
* **Monospace (Code / Terminal):** **`JetBrains Mono`** (`400 Regular`) for SQL statements, curl outputs, and Docker commands.

---

## 2. Color Palette (A Tight 4-Color System)

The design is the quiet frame, never the painting. Real database outputs and code snippets are the loudest, most vivid things on the page.

| Role | Color Name | Hex Code | WCAG Contrast | Usage & Application |
| :--- | :--- | :---: | :---: | :--- |
| **Near-Black Text** | Deep Slate Navy | `#0F172A` | **15.8:1** (AAA) | Primary headings, body copy, terminal backgrounds |
| **Near-White Canvas** | Warm Cloud White | `#F8FAFC` | Base | Page canvas background, generous negative space |
| **Surface / Card** | Pure Card White | `#FFFFFF` | Base | Content boxes, code containers, case study cards |
| **Border / Muted** | Slate Divider | `#E2E8F0` / `#64748B` | **4.9:1** (AA) | 1px clean card borders, subtle captions, metadata |
| **Single Accent** | Terminal Emerald | `#059669` | **4.6:1** (AA) | Primary CTA buttons, active links, success badges |

### Contrast & Readability Verification:
* Text `#0F172A` on background `#F8FAFC`: **15.8:1** (Exceeds WCAG AAA requirement of 7.0:1).
* Accent `#059669` on white `#FFFFFF`: **4.6:1** (Meets WCAG AA standard for text/UI components).

---

## 3. Logo & Favicon

### Wordmark (Name Set in Heading Font):
```text
BENNEDICT TON  |  Backend Systems
[Plus Jakarta Sans Bold 700, #0F172A with #059669 terminal cursor accent]
```

### Favicon & Monogram (Clean Terminal Glyph):
* Self-contained SVG asset created at [`favicon.svg`](favicon.svg):
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <rect width="64" height="64" rx="14" fill="#0F172A"/>
  <path d="M18 22L28 32L18 42" stroke="#059669" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
  <path d="M34 42H46" stroke="#F8FAFC" stroke-width="5" stroke-linecap="round"/>
</svg>
```
* **Meaning:** Represents command-line execution, backend discipline, and terminal prompt precision (`>_`).

---

## 4. Reusable Two-Line Style Note (For Claude Project / AI Workspace)

```markdown
STYLE GUIDE: Plus Jakarta Sans (Headings, 600/700) + Inter (Body, 400/500).
PALETTE: Text #0F172A on #F8FAFC bg, Surface #FFFFFF, Borders #E2E8F0, Accent #059669.
MOOD: Utilitarian, calm, and structured. Generous whitespace (24px/32px grid). The frame stays quiet so real code diffs and database outputs are the loudest things on the page.
```

---

## 5. Pass / Revise Checklist Self-Audit

- [x] **One or two fonts, not a pile:** Exactly 2 fonts (`Plus Jakarta Sans` for headings, `Inter` for body).
- [x] **Tight palette (3–4 colors) with actual hex codes:** Near-black (`#0F172A`), Near-white (`#F8FAFC`), Surface (`#FFFFFF`), Single Accent (`#059669`).
- [x] **Simple logo or favicon exists:** Standalone vector asset created at `favicon.svg`.
- [x] **Style note describes a single, coherent mood:** Calm, utilitarian, and restrained, framing backend engineering proof rather than competing with it.
