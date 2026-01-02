# 05-extended_rag_taxonomy.md
## Retrieval-Augmented Generation (RAG) — Extended & Complete Taxonomy

This document extends the earlier RAG landscape to include **important modern variants** that are often missed in basic explanations, such as **Adaptive RAG, Corrective RAG, and Self-RAG**.

This is intended as a **complete study reference**.

---

## Baseline: What RAG Is

RAG combines:
1. Retrieval of external knowledge
2. Generation grounded in retrieved context

Baseline flow:
```
Query → Retrieve → Generate
```

Everything below modifies *how retrieval is chosen, evaluated, or corrected*.

---

## Core RAG Families (Mental Grouping)

Think of RAG types as belonging to **five families**:

1. Retrieval Method
2. Control Strategy
3. Feedback / Self-correction
4. Knowledge Structure
5. System Composition

---

## 1️⃣ Semantic RAG (Vector RAG)

**Retrieval method:** Embeddings + similarity search  
**Key trait:** Always retrieves semantically similar chunks  

Used for:
- PDFs
- Docs
- Notes
- FAQs

---

## 2️⃣ Lexical / Keyword RAG

**Retrieval method:** BM25 / keyword matching  
**Key trait:** Exact term matching  

Used for:
- Logs
- Error codes
- Identifiers

---

## 3️⃣ Hybrid RAG

**Retrieval method:** Semantic + lexical  
**Key trait:** Better recall through combination  

Used for:
- Enterprise search
- Mixed structured/unstructured data

---

## 4️⃣ Structured / Deterministic RAG

**Retrieval method:** SQL / Pandas / APIs  
**Key trait:** Exact computation, no embeddings  

Used for:
- Metrics
- Financial data
- Compliance-critical systems

---

## 5️⃣ Agentic RAG

**Control strategy:** LLM agent decides retrieval  

Retrieval becomes a **tool**, not a fixed step.

Used for:
- Multi-domain reasoning
- Ambiguous queries

---

## 6️⃣ Hybrid Agentic RAG

**Control strategy:** Agent + multiple retrievers  

Combines:
- Deterministic tools
- Semantic RAG
- External APIs

This is the **most production-ready** pattern.

---

## 7️⃣ Adaptive RAG (You Were Right!)

**Also called:** Dynamic RAG

### Core idea
The system **adapts its retrieval strategy at runtime** based on:
- Query complexity
- Confidence
- Cost / latency constraints

### Architecture
```
Query
 → Classifier / Router
     ├─ Shallow retrieval
     ├─ Deep retrieval
     └─ No retrieval
 → LLM
```

### Key traits
- Retrieval is conditional
- Not always agent-based
- Often rule- or model-driven

### Used for
- Cost-sensitive systems
- Mixed simple + complex queries

---

## 8️⃣ Corrective RAG

### Core idea
The system **checks retrieved context or answers** and re-retrieves if needed.

### Architecture
```
Retrieve → Generate → Critique
                ↓
           Re-retrieve (if low quality)
```

### Key traits
- Feedback loop
- Improves reliability
- Higher latency

---

## 9️⃣ Self-RAG

### Core idea
The model **reflects on its own answer** and judges whether retrieval was sufficient.

### Architecture
```
Generate → Self-evaluate
        ├─ Good → Answer
        └─ Bad → Retrieve more → Regenerate
```

### Key traits
- Model-driven correction
- Minimal external logic
- Research-oriented

---

## 🔟 Multi-hop RAG

### Core idea
Multiple retrieval steps chained together.

### Used for
- Complex reasoning
- Cross-document questions

---

## 1️⃣1️⃣ Graph RAG

### Core idea
Knowledge stored as **nodes and edges**, not chunks.

### Used for
- Relationships
- Knowledge graphs
- Dependency reasoning

---

## 1️⃣2️⃣ Rerank-based RAG

### Core idea
Retrieve many candidates, then rerank using a stronger model.

### Used for
- Precision-critical retrieval
- Legal / medical search

---

## Comparison Table (Quick Reference)

| RAG Type | Retrieval Control | Feedback Loop | Complexity |
|--------|------------------|---------------|------------|
| Semantic | Fixed | ❌ | Low |
| Hybrid | Fixed | ❌ | Medium |
| Structured | Fixed | ❌ | Low |
| Agentic | Agent | ❌ | High |
| Adaptive | Dynamic | ❌ | Medium |
| Corrective | Fixed | ✅ | Medium |
| Self-RAG | Model | ✅ | High |
| Hybrid Agentic | Agent | Optional | Very High |

---

## How to Remember All This

> **RAG varies along three axes:**  
> *How you retrieve*  
> *Who decides*  
> *Whether you correct*

---

## Final Takeaway

> Adaptive, Corrective, and Self-RAG are not replacements — they are **layers of intelligence added on top of basic RAG**.

---

**File:** `05-extended_rag_taxonomy.md`
