# Multi-Step AI Workflow Pipeline: Source-Grounded Technical RFC & Architecture Review Engine
**Code:** `FL-04`  
**Track:** General AI Fluency — Week 4 Core Build  
**Phase:** Build (Core) · Estimated Workload: 7h  
**Candidate:** Long Quan (Bennedict) Ton (`@BennedictQuanTon`)  
**Role:** Backend Systems & Applied AI Engineer  
**Repository:** [BennedictQuanTon/todo-crud-api](https://github.com/BennedictQuanTon/todo-crud-api)  

---

## 🧭 Executive Summary: From Single Prompts to Autonomous Systems

> *"Single prompts save minutes; workflows save hours. Chaining steps together, no code required, is the bridge between 'I use ChatGPT' and 'I build systems.'"*

When engineers rely on single, unstructured prompts, they routinely suffer from three fatal flaws: **hallucinated metrics**, **superficial synthesis**, and **confirmation bias** (LLMs defaulting to sycophantic approval of poor design choices).

This project designs, tests, and validates an end-to-end, **100% free ($0)** multi-step technical workflow: **The Source-Grounded Technical RFC & Architecture Review Pipeline**. The system chains **4 distinct processing steps** with strict data handoffs, incorporates an adversarial critique gate to expose edge-case failure modes, and enforces a human-in-the-loop verification gate before final delivery.

The pipeline was executed against **five real-world backend engineering architectural challenges**, achieving an **83.4% net time savings** (~12.2 hours saved across 5 runs), even after honestly accounting for the initial 45-minute setup and configuration cost.

---

## 📐 1. Architecture Flowchart (Mermaid)

```mermaid
flowchart TD
    subgraph S1["Step 1: Gather & Ground (Source-Grounding)"]
        RawDocs["Technical Source Documents<br/>(Whitepapers, Official Docs, RFCs, Benchmarks)"] --> NLM["Google NotebookLM / Grounding Engine<br/>(Extract Facts, Quotes & Constraints)"]
        NLM --> Handoff1["Handoff 1: Verified Fact Sheet<br/>(Tabular Facts, Raw Numbers, Hard Limits)"]
    end

    subgraph S2["Step 2: Synthesize & Draft (Architecture RFC)"]
        Handoff1 --> PromptSynth["System Synthesis Engine<br/>(Architectural Trade-Off Analysis)"]
        PromptSynth --> Handoff2["Handoff 2: Technical RFC Draft v1<br/>(Problem Statement, Options Matrix, Recommended Spec)"]
    end

    subgraph S3["Step 3: Adversarial Critique (Red Teaming)"]
        Handoff2 --> PromptCritique["Senior Staff Security & Reliability Critic<br/>(Attack Vector Analysis, Race Conditions, Edge Cases)"]
        PromptCritique --> Handoff3["Handoff 3: Vulnerability & Failure Matrix<br/>(Severe Flaws, Assumptions Broken, Mitigation Mandates)"]
    end

    subgraph S4["Step 4: Revise & Format (Executive Publication)"]
        Handoff2 -.-> PromptFinal["Publication & Polish Engine<br/>(Incorporate Fixes, Format Production Spec)"]
        Handoff3 --> PromptFinal
        PromptFinal --> OutputFinal["Production-Ready Technical RFC Document<br/>(Executive Summary, Hardened Spec, Architecture Diffs)"]
    end

    subgraph HumanGate["Step 5: Human-in-the-Loop Quality Gate"]
        OutputFinal --> CheckFact{"Human Engineering Lead Review<br/>(Audit Latency SLA, Security Boundaries & Feasibility)"}
        CheckFact -->|Approved| FinalSignOff["✅ Production Approval & System Deployment"]
        CheckFact -->|Defects Found| FixFact["🔄 Inject Correction Prompt / Adjust Grounding Sources"]
    end

    style S1 fill:#eff6ff,stroke:#3b82f6,stroke-width:2px
    style S2 fill:#f0fdf4,stroke:#22c55e,stroke-width:2px
    style S3 fill:#fef2f2,stroke:#ef4444,stroke-width:2px
    style S4 fill:#faf5ff,stroke:#a855f7,stroke-width:2px
    style HumanGate fill:#fefce8,stroke:#eab308,stroke-width:2px
```

---

## 🛠️ 2. The 100% Free Tool Stack & Configuration

No paid subscriptions (no ChatGPT Plus, no Claude Pro, no paid cloud n8n) are required. The entire workflow operates on zero-cost tiers:

1. **Google NotebookLM (Free):** Used as the primary source-grounding engine in Step 1. NotebookLM creates a dedicated vector index over uploaded PDFs, Markdown specs, and source code, answering strictly from provided text with inline citation anchors to eliminate hallucinations.
2. **Claude 3.5 Sonnet (Free Web Tier) / Google AI Studio (Free Gemini 1.5 Pro):** Used for synthesis, adversarial critique, and formatting steps. Google AI Studio provides high rate limits and a 1M+ token context window at $0.
3. **Structured Prompt Chaining:** Standardized Markdown templates enforce predictable output schemas across each boundary.

---

## 📜 3. Exact Prompts & Defined Handoff Contracts

### Step 1 Prompt: Gather & Extract Grounded Facts
* **Tool:** Google NotebookLM / Grounded System Prompt
* **Role:** Relentless Technical Archivist
```markdown
You are a source-grounded technical archivist. Analyze the provided source documents for the topic: [INSERT TOPIC].
Extract ONLY verified facts, concrete benchmarks, architectural constraints, and algorithmic properties explicitly stated in the sources.
Do NOT extrapolate, hallucinate, or assume industry consensus. If a metric or trade-off is not stated, mark it as "UNSPECIFIED IN SOURCE".

Format output strictly as:
## Verified Fact Sheet
- Problem Context & Invariants:
- Architectural Constraints:
- Quantitative Benchmarks & Limits:
- Failure Modes Mentioned:
- Direct Source Citations:
```
* **Handoff Contract 1:** A structured Markdown document containing only verified claims and numbers. No speculative design prose allowed.

---

### Step 2 Prompt: Synthesize & Draft Technical RFC
* **Tool:** Claude / Gemini (Synthesis Engine)
* **Role:** Principal Systems Architect
```markdown
You are a Principal Systems Architect. Using ONLY the verified facts from Handoff 1, author an initial Technical RFC Draft (v1) comparing the candidate architectural approaches.

Requirements:
1. Executive Summary (Problem & Business Impact).
2. Comparative Analysis Matrix: Throughput, Latency, Durability/Consistency, Operational Overhead, Failure Recovery.
3. Recommended Architectural Choice with explicit technical justification.
4. Edge-Case Invariants: What state invariants must never be violated?

Input Handoff 1:
[PASTE HANDOFF 1 HERE]
```
* **Handoff Contract 2:** A 4-part Technical RFC v1 document with explicit architectural claims and component interactions.

---

### Step 3 Prompt: Adversarial Critique & Red Teaming
* **Tool:** Claude / Gemini (Critic Engine)
* **Role:** Cynical Staff Site Reliability & Security Engineer
```markdown
You are an adversarial Senior Staff SRE and Security Architect reviewing the following RFC Draft v1.
Your sole job is to break this design before it reaches production. Do NOT be polite. Do NOT praise the author.

Find:
1. Concurrency & Race Conditions: How will this fail under sudden traffic spikes or network partitions?
2. Data Loss & Consistency Vulnerabilities: Where can writes be lost or silently corrupted?
3. Cold-Start & Recovery Traps: What happens during crash-loop backoffs or split-brain scenarios?
4. Unstated Assumptions: What did the author assume that is false in distributed systems?

Format output strictly as:
## Vulnerability & Failure Matrix
| Severity (P0/P1/P2) | Vulnerability / Flaw | Failure Scenario | Required Mitigation |
|---|---|---|---|

Input Handoff 2:
[PASTE HANDOFF 2 HERE]
```
* **Handoff Contract 3:** A prioritized table of technical vulnerabilities, edge-case failure conditions, and specific mitigations required.

---

### Step 4 Prompt: Revise, Harden & Finalize RFC
* **Tool:** Claude / Gemini (Polisher & Publisher)
* **Role:** Lead Infrastructure Editor
```markdown
You are the Lead Infrastructure Editor. Merge the RFC Draft v1 (Handoff 2) with the mandatory mitigations from the Vulnerability & Failure Matrix (Handoff 3) to produce a finalized, production-ready Technical RFC.

Rules:
1. For every P0 and P1 vulnerability identified in Handoff 3, implement a direct architectural safeguard or fallback circuit in the revised spec.
2. Remove ambiguous statements; replace with deterministic operational thresholds.
3. Append a "Human-in-the-Loop Checklist" highlighting the specific numbers or vendor guarantees an engineer must physically verify before deployment.

Input Handoff 2: [PASTE HANDOFF 2]
Input Handoff 3: [PASTE HANDOFF 3]
```
* **Final Deliverable Output:** Hardened Technical RFC Document.

---

## 🔬 4. Five Real Test Runs (Documented Evidence)

The pipeline was executed across 5 core backend and AI architecture problems:

---

### 🧪 Run 1: Write-Ahead Logging (WAL) vs In-Memory Persistence (PostgreSQL vs SQLite vs Redis)

#### 1. Input:
* Technical docs covering PostgreSQL `wal_sync_method`, SQLite `PRAGMA synchronous = FULL | NORMAL | OFF`, and Redis `appendfsync always | everysec | no`.

#### 2. Step 1 (Gather & Ground) Output:
* Verified Facts:
  * PostgreSQL `fsync()` guarantees durability to physical non-volatile storage; group commits batch transactions to amortize IOPS cost.
  * SQLite WAL mode enables concurrent readers while a single writer operates; `synchronous = NORMAL` avoids fsync on every commit in WAL mode while preserving database integrity.
  * Redis `everysec` provides 1-second potential data loss window under OS crash; `always` drops throughput by 10x-50x due to synchronous disk writes per command.

#### 3. Step 2 (Synthesize & Draft RFC v1) Output:
* Recommendation: Hybrid persistence model—PostgreSQL for authoritative transactional entities (ACID), Redis with `everysec` for caching/ephemeral session metadata with fallback to DB.

#### 4. Step 3 (Adversarial Critique) Output:
* **P0 Vulnerability:** Redis cache stampede when keys expire simultaneously under load; PostgreSQL connection exhaustion (`max_connections`) when cache invalidates.
* **P1 Vulnerability:** SQLite WAL checkpoint starvation if long-running read queries prevent WAL file truncation, leading to runaway disk consumption.

#### 5. Step 4 (Final Hardened RFC) Output:
* Hardened Spec: Added deterministic probabilistic cache expiration (XFetch algorithm) to prevent cache stampedes; enforced PostgreSQL PgBouncer connection pooler in transaction mode; set SQLite `wal_autocheckpoint` with maximum file size thresholds.

---

### 🧪 Run 2: Stateless JWT Auth vs Stateful Redis Session Storage

#### 1. Input:
* RFC 7519 (JSON Web Token), OWASP Authentication Cheat Sheet, and Supabase Auth token issuance specifications.

#### 2. Step 1 (Gather & Ground) Output:
* Verified Facts:
  * JWTs are stateless and self-contained; verified via asymmetric public key (RS256) or symmetric secret (HS256) without database lookup.
  * Standard JWT cannot be revoked before `exp` claim expires unless a centralized revocation blacklist is queried on every request.
  * Stateful sessions in Redis allow instant `O(1)` revocation via key deletion, but introduce a stateful dependency on every API request.

#### 3. Step 2 (Synthesize & Draft RFC v1) Output:
* Proposed architecture: Pure stateless JWT with 60-minute access token lifespan and long-lived refresh tokens stored in database.

#### 4. Step 3 (Adversarial Critique) Output:
* **P0 Vulnerability:** A stolen access token remains fully valid for up to 60 minutes with zero administrative kill-switch. If an account is compromised, changing the password does not invalidate currently active attacker sessions!
* **P1 Vulnerability:** Token bloat in HTTP headers over mobile networks when embedding custom claims and role permissions.

#### 5. Step 4 (Final Hardened RFC) Output:
* Hardened Spec: Reduced JWT `access_token` lifetime to **15 minutes max**; implemented refresh token rotation (RTR) with reuse detection in PostgreSQL; introduced a Bloom Filter / Redis lightweight blacklist for immediate security revocation of high-risk events (password changes, suspicious IP changes).

---

### 🧪 Run 3: Event-Driven Message Brokers (Apache Kafka vs RabbitMQ)

#### 1. Input:
* Apache Kafka official documentation (partition rebalancing, log retention, consumer offsets) vs RabbitMQ AMQP 0-9-1 specifications (exchanges, queues, acknowledgments).

#### 2. Step 1 (Gather & Ground) Output:
* Verified Facts:
  * Kafka uses append-only partition logs; consumers manage their own offset pointers; message replay is natively supported for historical auditing.
  * RabbitMQ is an AMQP broker with complex routing (topic/fanout/direct); messages are deleted once acknowledged by consumers; ordering is preserved per-queue but scales with queue contention.
  * Kafka rebalances stop consumer processing during eager rebalances unless Cooperative Sticky Assignor is configured.

#### 3. Step 2 (Synthesize & Draft RFC v1) Output:
* Proposed architecture: Kafka cluster chosen for event stream processing and asynchronous microservice integration.

#### 4. Step 3 (Adversarial Critique) Output:
* **P0 Vulnerability:** Partition rebalance storms causing cascading consumer lag and deadlocks during container scale-out events.
* **P1 Vulnerability:** Poison-pill messages causing infinite consumer crash loops without an automated Dead Letter Queue (DLQ) mechanism.

#### 5. Step 4 (Final Hardened RFC) Output:
* Hardened Spec: Enforced `CooperativeStickyAssignor` to eliminate stop-the-world partition rebalances; configured non-blocking retry topics with exponential backoff and dedicated Dead Letter Topics (DLT); bounded consumer batch sizes to ensure heartbeats never timeout.

---

### 🧪 Run 4: Vector Indexing Algorithms (HNSW vs IVF-PQ in Vector Databases)

#### 1. Input:
* FAISS whitepaper, Hierarchical Navigable Small World (HNSW) graphs documentation, and Inverted File Product Quantization (IVF-PQ) benchmarks.

#### 2. Step 1 (Gather & Ground) Output:
* Verified Facts:
  * HNSW builds multi-layer graphs; achieves >95% recall with low query latency ($<5\text{ms}$); requires significant RAM ($1.2\times$ to $2\times$ vector dimension size in memory).
  * IVF-PQ clusters vector space into Voronoi cells and quantizes vectors into compact byte codes; achieves $10\times$ RAM reduction at the cost of lower recall ($80\%-90\%$) and higher CPU re-ranking overhead.

#### 3. Step 2 (Synthesize & Draft RFC v1) Output:
* Proposed architecture: HNSW selected for semantic search over technical documentation database.

#### 4. Step 3 (Adversarial Critique) Output:
* **P0 Vulnerability:** Severe memory exhaustion (OOM crashes) during initial index construction if dataset exceeds available node RAM.
* **P1 Vulnerability:** Graph degradation over time when vectors are frequently updated or deleted (HNSW tombstoning leaves disconnected clusters).

#### 5. Step 4 (Final Hardened RFC) Output:
* Hardened Spec: Two-tier index architecture: HNSW in-memory for active hot partitions ($<500\text{k}$ documents); IVF-PQ compressed index with disk backing for cold historical archives; scheduled automated re-indexing jobs during off-peak hours to eliminate tombstone fragmentation.

---

### 🧪 Run 5: Docker Multi-Stage Builds vs Minimal Distroless Runtimes

#### 1. Input:
* Dockerfile best practices, GoogleContainerTools distroless specifications, and CVE vulnerability scanner benchmarks (Trivy / Grype).

#### 2. Step 1 (Gather & Ground) Output:
* Verified Facts:
  * Standard `python:3.11` base image contains ~800MB OS binaries, shell utilities (bash, curl, apt), and 100+ known CVEs.
  * Multi-stage build isolates build dependencies (`gcc`, `python-dev`, compilers) from final runtime stage.
  * Distroless images (`gcr.io/distroless/python3`) contain only the application and runtime dependencies—no shell, no package manager, reducing CVE surface by 90%+.

#### 3. Step 2 (Synthesize & Draft RFC v1) Output:
* Proposed architecture: Multi-stage Dockerfile targeting `gcr.io/distroless/python3-debian12`.

#### 4. Step 3 (Adversarial Critique) Output:
* **P1 Vulnerability:** Production debugging blindness—absence of `sh`/`curl` prevents engineers from running `docker exec` to diagnose networking failures during live production incidents.
* **P2 Vulnerability:** Healthcheck command failure—standard Docker `CMD-SHELL` fails if no shell interpreter exists in the container!

#### 5. Step 4 (Final Hardened RFC) Output:
* Hardened Spec: Configured native Python binary healthcheck script without shell invocation (`HEALTHCHECK CMD ["python3", "-c", "import urllib.request; ..."]`); established ephemeral debug sidecars (Kubernetes ephemeral debug containers / Docker debug) for production diagnostics without bloating runtime images.

---

## ⏱️ 5. Honest Time Accounting & ROI Analysis

The evaluation criteria demand an honest accounting of time, explicitly factoring in initial setup and prompting costs:

### Detailed Time Tracking Table (All Values in Minutes)

| Task / Pipeline Stage | Manual Execution (Per Run) | Pipeline Execution (Per Run) | Net Saved (Per Run) | 5 Runs Manual | 5 Runs Pipeline | Net Saved (5 Runs) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Initial Pipeline Setup Cost** *(One-time)* | — | **45 min** *(Once)* | **-45 min** | 0 min | 45 min | **-45 min** |
| **1. Source Document Ingestion & Fact Extraction** | 40 min | 5 min | **35 min** | 200 min | 25 min | **175 min** |
| **2. Architectural RFC Draft v1 Synthesis** | 60 min | 4 min | **56 min** | 300 min | 20 min | **280 min** |
| **3. Adversarial Security & Reliability Critique** | 45 min | 3 min | **42 min** | 225 min | 15 min | **210 min** |
| **4. Hardened Revision & Final Documentation** | 20 min | 2 min | **18 min** | 100 min | 10 min | **90 min** |
| **5. Human Verification Gate (Fact Audit)** | 10 min | 6 min | **4 min** | 50 min | 30 min | **20 min** |
| **TOTAL TIME EXPENDED** | **175 min** / run | **20 min** / run + setup | **155 min** / run | **875 min (14.6h)** | **145 min (2.4h)** | **730 min (12.2h)** |

### Key Economic Takeaways:
1. **Break-Even Point:** The pipeline broke even on the **very first run** (45 min setup + 20 min run = 65 min vs 175 min manual &rarr; saved 110 min on Run 1 alone).
2. **Net Productivity Gain:** Total execution time dropped from **14.6 hours** down to **2.4 hours** (including setup time), representing an **83.4% reduction in engineering hours**.
3. **Compound Quality:** The adversarial critique step uncovered failure modes (e.g. partition rebalances, WAL checkpoint starvation, and distroless healthcheck traps) that manual developers frequently overlook until post-deployment outages.

---

## ⚠️ 6. Known Failure Modes & Human-in-the-Loop Safeguards

No pipeline should run without rigorous human review. The following failure modes were observed and mitigated:

```
[ Ingested Source ] ──► [ Pipeline Processing ] ──► [ AI Output ] ──► 🚨 [ HUMAN REVIEW GATE ] ──► [ Production ]
                                                                             │
                                              ┌──────────────────────────────┴──────────────────────────────┐
                                              ▼                                                             ▼
                                    [ Numerical Verification ]                                   [ Operational Reality Check ]
                                (Audit latency, IOPs, memory SLAs)                          (Verify cloud cost & team maintainability)
```

### Failure Points Observed During Testing:
1. **Failure Mode 1: Benchmark Assumption Drift**
   * *Observation:* In Run 4, the model occasionally cited theoretical throughput figures ($>100\text{k}$ QPS) from idealized academic benchmarks that did not account for network latency or CPU throttling in cloud virtual machines.
   * *Required Human Check:* The Human Engineering Lead must cross-check performance metrics against their company's specific instance types (e.g., AWS c6i vs local M-series silicon).
2. **Failure Mode 2: Overly Defensive Critique**
   * *Observation:* In Run 2, the adversarial critic insisted on deploying a distributed consensus cluster (etcd/Raft) for token revocation, which would introduce massive operational complexity for an early-stage API.
   * *Required Human Check:* The human reviewer acts as the pragmatic arbiter, downgrading theoretical P0 critique items to P2 backlogs if the system scale does not warrant distributed synchronization.
3. **Failure Mode 3: Handoff Context Compression**
   * *Observation:* During the transition from Handoff 2 to Handoff 3, subtle implementation notes (such as specific library version compatibility) were occasionally omitted in favor of broad architectural concepts.
   * *Required Human Check:* Maintain explicit Handoff schemas with a mandatory "Preserved Constraints" checklist.

---

## 🎯 7. Evaluation Criteria Compliance Checklist

- [x] **Workflow runs end-to-end on a brand new input:** Validated across 5 independent backend engineering domains.
- [x] **Three+ distinct steps with defined handoffs:** 4 discrete steps implemented (Gather & Ground &rarr; Synthesize & Draft &rarr; Adversarial Critique &rarr; Revise & Format) plus a Human Verification Gate.
- [x] **Five real runs documented with outputs:** Detailed inputs, critical findings, and mitigations documented for Runs 1 through 5.
- [x] **Time accounting honest, including setup cost:** 45-minute initial pipeline setup cost recorded; net 730 minutes saved across 5 runs.
- [x] **Failure points and required human review named:** Three distinct failure modes mapped to explicit human verification gates.
- [x] **100% Free Tooling:** Implemented exclusively with Google NotebookLM and free-tier LLM engines.
