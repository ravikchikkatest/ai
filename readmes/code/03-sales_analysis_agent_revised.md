# 03-sales_analysis_agent_revised.md
## Sales Analysis Agent (Hybrid Agentic RAG + Deterministic Analytics)

This document explains the **technical object-level flow** of a **hybrid sales analysis agent** built with **LlamaIndex**.

This system combines:
- **Deterministic analytics** (exact sums / averages via pandas)
- **Semantic RAG** (vector search over sales records)
- **Agentic control** (ReActAgent decides which tool to use)

The intent is to clearly show **how data flows** and **which imported objects participate** at each stage.

---

## Imports (Object Map)

### Python / System
- `os` → filesystem & env vars
- `sys` → process control
- `logging` → runtime diagnostics
- `Path` → `pathlib.Path`
- `pandas as pd` → tabular data processing
- `dotenv.load_dotenv` → environment loading

### LlamaIndex Core
- `Settings` → `llama_index.core.Settings`
- `Document` → `llama_index.core.Document`
- `VectorStoreIndex` → `llama_index.core.VectorStoreIndex`
- `StorageContext` → `llama_index.core.StorageContext`
- `load_index_from_storage` → `llama_index.core.load_index_from_storage`
- `SentenceSplitter` → `llama_index.core.node_parser.SentenceSplitter`

### Agent & Tools
- `ReActAgent` → `llama_index.core.agent.ReActAgent`
- `QueryEngineTool` → `llama_index.core.tools.QueryEngineTool`
- `FunctionTool` → `llama_index.core.tools.FunctionTool`

### Models
- `Groq` → `llama_index.llms.groq.Groq`
- `Gemini` → `llama_index.llms.gemini.Gemini` (imported, optional)
- `HuggingFaceEmbedding` → `llama_index.embeddings.huggingface.HuggingFaceEmbedding`

---

## High-Level Flow (Data + Control)

```
.env / OS
  ↓
load_dotenv + os.getenv
  ↓
Settings.llm = Groq
Settings.embed_model = HuggingFaceEmbedding
  ↓
CSV (sales_data.csv)
  ↓
pandas.DataFrame (_SALES_DF)
  ↓
Document[]
  ↓
SentenceSplitter
  ↓
VectorStoreIndex (persisted)
  ↓
QueryEngine
  ↓
QueryEngineTool (semantic)
      +
FunctionTool (analytics)
        ↓
     ReActAgent
        ↓
      Answer
```

---

## 1. Environment & Global Brain

**Objects**
- `load_dotenv`
- `os.getenv`
- `Settings`
- `Groq`
- `HuggingFaceEmbedding`

**Role**
- Loads secrets
- Configures global LLM (Groq + LLaMA 3)
- Configures global embedding model

All downstream LlamaIndex components automatically inherit these settings.

---

## 2. Deterministic Data Layer (Analytics Memory)

**Objects**
- `pandas.DataFrame`
- `_SALES_DF` (global cache)

**Flow**
```
CSV → DataFrame → numeric cleanup → filtering → aggregation
```

This layer provides **exact answers** (sum, average) and is not probabilistic.

---

## 3. Analytics Tool (FunctionTool)

**Object**
- `FunctionTool.from_defaults`

**Wrapped function**
- `compute_analytics(metric, column, filter_condition)`

**Purpose**
- Exact numeric computation
- Used for questions like:
  - "Total sales in South region"
  - "Average unit price for Laptops"

This bypasses embeddings and LLM hallucination risk.

---

## 4. Knowledge Units (Documents)

**Objects**
- `Document`

**Flow**
```
DataFrame row
 → structured text (OrderID, Date, Region, ...)
 → Document(text)
```

Each document represents one sales record.

---

## 5. Chunking (SentenceSplitter)

**Object**
- `SentenceSplitter`

**Configuration**
- `chunk_size=512`
- `chunk_overlap=50`

**Purpose**
- Preserve semantic coherence
- Improve retrieval quality

---

## 6. Semantic Memory (VectorStoreIndex)

**Object**
- `VectorStoreIndex`

**Flow**
```
Document.text
 → HuggingFaceEmbedding
 → vectors
 → vector index
```

**Persistence**
- Stored on disk via `StorageContext`
- Reloaded on subsequent runs

---

## 7. Retrieval Interface (QueryEngine)

**Object**
- `QueryEngine` (created via `index.as_query_engine()`)

**Role**
- Semantic retrieval
- Context assembly
- LLM prompting

---

## 8. RAG Tool (QueryEngineTool)

**Object**
- `QueryEngineTool`

**Purpose**
- Expose semantic search as an agent-selectable tool
- Used for:
  - Trend analysis
  - Contextual lookup
  - Exploratory questions

---

## 9. Agent (ReActAgent)

**Object**
- `ReActAgent`

**Internal Loop**
```
Thought → Act → Observe → Thought → Answer
```

**Capabilities**
- Chooses between:
  - `analytics_tool` (exact math)
  - `sales_context_tool` (semantic RAG)

This makes the system **hybrid and adaptive**.

---

## 10. Runtime Execution

```
User Query
 → Agent reasoning (LLM)
 → Tool selection
 → FunctionTool OR QueryEngineTool
 → Observation
 → Final synthesis
 → Answer
```

---

## Hybrid Design Summary

| Aspect | Analytics Tool | RAG Tool |
|------|---------------|---------|
| Accuracy | Exact | Probabilistic |
| Data Source | DataFrame | Vector index |
| Best For | Metrics | Trends / context |
| Used By | Agent | Agent |

---

## Memorisation Shortcut

> **Tables for truth, vectors for meaning, agent for control**

---

## One-Line Takeaway

> This system is not just RAG — it is an **agent that decides when to compute and when to retrieve**.
