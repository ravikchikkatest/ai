# Foundation LLM Cheat Sheet (Exam & Interview Ready)

This document is a **quick-reference cheat sheet** for common exam-style questions about
**foundation large language models (LLMs)**, especially those focused on:

- Open-source vs proprietary models
- Context window size
- Code vs general-purpose models
- When to choose which model

Designed for **Generative AI Engineer exams, interviews, and design discussions**.

---

## 1. Core Decision Axes (Memorize These)

Most questions reduce to one or more of the following:

1. Open-source vs closed-source
2. Context window size (small vs large)
3. Quality vs cost vs latency
4. Code-specialized vs general-purpose
5. Data governance (can data leave org or not)

---

## 2. Key Models You Must Recognize

### MPT-30B
- Type: Open-source LLM
- Context window: **Very large** (8k+ tokens)
- Strengths:
  - Long-context processing
  - Document-heavy workloads
  - RAG applications with large inputs
- Weaknesses:
  - Not state-of-the-art reasoning
- Typical exam use:
  - “Open-source LLM with large context window”

✅ **Correct answer when long context + open source are required**

---

### DBRX / DBRX Instruct
- Type: Databricks foundation model
- Architecture: Mixture-of-Experts (MoE)
- Strengths:
  - High-quality reasoning
  - Code + instruction following
- Weaknesses (exam perspective):
  - **Not framed as open-source long-context model**
- Typical exam use:
  - Premium quality Databricks-hosted model
  - Not the answer for “open-source + large context” questions

❌ Often a tempting but incorrect choice

---

### Llama2-70B
- Type: Open-weight open-source model
- Context window: Moderate (4k tokens typical)
- Strengths:
  - High quality
  - Can be self-hosted
- Weaknesses:
  - Context window not the largest
- Typical exam use:
  - Confidential data + quality + self-hosting

---

### CodeLlama-34B
- Type: Code-specialized open model
- Context window: Moderate
- Strengths:
  - Code generation across languages
- Weaknesses:
  - Not for long documents
- Typical exam use:
  - Developer assistants

---

### Dolly (e.g., 1.5B)
- Type: Small open-source model
- Strengths:
  - Lightweight
- Weaknesses:
  - Low quality
- Typical exam use:
  - Almost always incorrect unless explicitly asking for “lightweight”

---

### BGE-large
- Type: **Embedding model**
- NOT a generative LLM
- Typical exam use:
  - Trick option

❌ Never correct for generation tasks

---

### OpenAI GPT-4
- Type: Proprietary closed-source
- Strengths:
  - Very high quality
- Weaknesses:
  - Data sent to third party
- Typical exam use:
  - Disallowed when governance/privacy is strict

---

## 3. Common Exam Question Patterns

### Pattern 1: “Open-source LLM with large context window”
✅ **MPT-30B**

---

### Pattern 2: “Highest quality Databricks-hosted model”
✅ **DBRX Instruct**

---

### Pattern 3: “Sensitive data, no third-party sharing”
✅ **Llama2-70B** (self-hosted)

---

### Pattern 4: “Code generation across languages”
✅ **CodeLlama-34B**

---

### Pattern 5: “Semantic search / retrieval”
✅ **Embedding models (BGE-large)**

---

## 4. Fast Elimination Rules (Very Important)

- If the task is generation → eliminate embedding models
- If privacy is strict → eliminate OpenAI models
- If context window is the key → eliminate small/medium models
- If code-specific → eliminate general-purpose LLMs

These rules usually leave **one obvious answer**.

---

## 5. One-Line Memory Anchors

- **Long context + open source → MPT**
- **Quality-first Databricks → DBRX**
- **Private + high quality → Llama2-70B**
- **Code assistant → CodeLlama**
- **Search ≠ generation → Embeddings**

---

## 6. Why DBRX Was Incorrect in the Example

The question explicitly required:
- Open-source LLM
- Large context window

DBRX:
- Is not positioned as an open-source long-context model in exams
- Is framed as a Databricks-hosted premium model

Therefore:
❌ Incorrect for that question

---

End of cheat sheet.
