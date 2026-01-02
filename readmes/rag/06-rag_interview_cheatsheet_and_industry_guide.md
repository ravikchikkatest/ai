# 06-rag_interview_cheatsheet_and_industry_guide.md
## RAG Complete Guide — Cheat-Sheet + Industry Model Choices

This document extends the RAG taxonomy with:
- An **interview-ready cheat-sheet diagram**
- **Which models work well for which RAG types in industry**
- Practical guidance beyond theory

This is designed for **interviews, system design rounds, and real-world architecture decisions**.

---

## 🔹 One-Page RAG Cheat-Sheet (Interview Gold)

```
                          ┌──────────────────────┐
                          │        USER QUERY     │
                          └──────────┬───────────┘
                                     │
                          ┌──────────▼───────────┐
                          │   ROUTING / DECISION  │
                          │ (Rules / Agent / LLM) │
                          └──────────┬───────────┘
        ┌────────────────────────────┼────────────────────────────┐
        │                            │                            │
┌───────▼────────┐         ┌─────────▼────────┐        ┌─────────▼────────┐
│ STRUCTURED RAG  │         │  SEMANTIC RAG     │        │ KEYWORD RAG      │
│ (SQL / Pandas)  │         │ (Vector Search)  │        │ (BM25 / Logs)    │
└───────┬────────┘         └─────────┬────────┘        └─────────┬────────┘
        │                              │                            │
        └──────────────┬───────────────┴───────────────┬──────────┘
                       │                               │
              ┌────────▼─────────┐           ┌─────────▼────────┐
              │  HYBRID RAG       │           │  MULTI-HOP RAG   │
              │ (Merge + Rerank)  │           │ (Chain Retrieve) │
              └────────┬─────────┘           └─────────┬────────┘
                       │                               │
                ┌──────▼──────────┐          ┌─────────▼────────┐
                │  AGENTIC RAG     │◀────────▶│  ADAPTIVE RAG    │
                │ (Tools + ReAct)  │          │ (Dynamic Depth)  │
                └──────┬──────────┘          └─────────┬────────┘
                       │                               │
              ┌────────▼──────────┐           ┌─────────▼────────┐
              │ HYBRID AGENTIC RAG │           │ CORRECTIVE /     │
              │ (Prod-grade)      │           │ SELF-RAG         │
              └────────┬──────────┘           └─────────┬────────┘
                       │                               │
                       └──────────────┬────────────────┘
                                      │
                              ┌───────▼────────┐
                              │   FINAL ANSWER │
                              └────────────────┘
```

---

## 🔹 Interview One-Liners (Memorise These)

- **Semantic RAG**: “Retrieve by meaning, always retrieve.”
- **Hybrid RAG**: “Recall first, precision later.”
- **Structured RAG**: “Truth comes from databases, not LLMs.”
- **Agentic RAG**: “The LLM decides how to retrieve.”
- **Adaptive RAG**: “Retrieval depth adapts to query complexity.”
- **Corrective / Self-RAG**: “If the answer looks wrong, retrieve again.”
- **Hybrid Agentic RAG**: “Production systems mix truth + meaning + control.”

---

## 🔹 Industry-Grade Model Choices (2025)

### Embedding Models (Semantic RAG backbone)

| Use Case | Recommended Models |
|-------|--------------------|
| General-purpose | `BAAI/bge-small-en-v1.5` |
| High accuracy | `bge-large-en`, `E5-large` |
| Multilingual | `bge-m3`, `LaBSE` |
| Cost-sensitive | `MiniLM-L6-v2` |

**Industry note:**  
> Embeddings matter more than LLM choice for retrieval quality.

---

### LLMs for Generation & Reasoning

| RAG Type | Models That Work Well |
|-------|-----------------------|
| Simple / Semantic RAG | Gemini 1.5 Flash, GPT-4o-mini |
| Hybrid / Multi-hop RAG | GPT-4.1, Claude 3 Sonnet |
| Agentic RAG | GPT-4.1, Claude 3 Opus |
| Cost-optimized Agentic | Groq (LLaMA 3.1), Gemini Flash |
| Deterministic-heavy systems | Smaller LLM + tools |

**Industry rule:**  
> Use the **cheapest model that reasons well enough**, not the smartest one.

---

## 🔹 Vector Databases in Practice

| Scale | Common Choices |
|-----|---------------|
| Local / POC | FAISS |
| Mid-scale | Chroma |
| Enterprise | Pinecone, Weaviate |
| SQL-heavy orgs | pgvector |

---

## 🔹 RAG Type → When Companies Use It

| Scenario | RAG Type |
|-------|---------|
| Internal docs Q&A | Semantic RAG |
| Customer support bots | Hybrid RAG |
| Finance dashboards | Structured + Agentic |
| Legal / Compliance | Rerank + Corrective RAG |
| AI copilots | Hybrid Agentic RAG |

---

## 🔹 Common Interview Traps (Avoid These)

❌ “RAG is just vector search”  
❌ “Agents replace retrieval”  
❌ “LLMs should calculate numbers”  

✅ Retrieval, computation, and reasoning are **separate responsibilities**.

---

## 🔹 Final Mental Model (Pin This)

> **RAG varies along three axes:**  
> 1. *How you retrieve*  
> 2. *Who decides*  
> 3. *How you correct*

---

## Final Takeaway

> Modern RAG systems are **layered architectures**, not single patterns.  
> The best systems combine **truth (data)**, **meaning (vectors)**, and **control (agents)**.

---

**File:** `06-rag_interview_cheatsheet_and_industry_guide.md`
