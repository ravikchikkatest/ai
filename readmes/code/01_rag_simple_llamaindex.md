# tech_simple_rag_llamaindex_csv.md
## Simple RAG with LlamaIndex (CSV → Vector Index → Query) — With Import Object Map

This README explains the **technical object and data flow** of a **Simple (non-agentic) RAG** system built with **LlamaIndex**, using a CSV file as the data source.

It includes:
- A flow diagram **annotated with the exact imported objects and their import paths**
- Object-by-object responsibilities
- Runtime execution flow

---

## Imports (Object Map)

These are the main objects/classes used and where they come from:

- `os` → `import os`
- `pandas` → `import pandas as pd`
  - `pd.DataFrame` (runtime type produced by `pd.read_csv`)
- `load_dotenv` → `from dotenv import load_dotenv`
- `Settings` → `from llama_index.core import Settings`
- `Document` → `from llama_index.core import Document`
- `VectorStoreIndex` → `from llama_index.core import VectorStoreIndex`
- `Gemini` → `from llama_index.llms.gemini import Gemini`
- `HuggingFaceEmbeddings` → `from llama_index.embeddings.huggingface import HuggingFaceEmbeddings`

---

## High-Level Flow (Data + Control) — With Import Paths

```
.env / OS
  │
  ▼
load_dotenv()                           (dotenv.load_dotenv)
os.getenv()                              (os.getenv)
  │
  ▼
Settings.llm = Gemini(...)               (llama_index.core.Settings + llama_index.llms.gemini.Gemini)
Settings.embed_model = HuggingFaceEmbeddings(...)
                                         (llama_index.embeddings.huggingface.HuggingFaceEmbeddings)
  │
  ▼
CSV file (sample_data.csv)               (filesystem)
  │
  ▼
pd.read_csv(...)                         (pandas.read_csv)
  │
  ▼
pd.DataFrame                             (pandas.DataFrame)
  │
  ▼
Document[]                               (llama_index.core.Document)
  │
  ▼
VectorStoreIndex.from_documents(...)      (llama_index.core.VectorStoreIndex)
  │
  ▼
index.as_query_engine(top_k=5)            (QueryEngine produced by llama_index)
  │
  ▼
query_engine.query(user_input)            (QueryEngine.query)
  │
  ▼
Answer (LLM-generated)                   (Gemini via Settings.llm)
```

---

## 1) Environment & Global Configuration

**Imports involved**
- `dotenv.load_dotenv`
- `os.getenv`
- `llama_index.core.Settings`
- `llama_index.llms.gemini.Gemini`
- `llama_index.embeddings.huggingface.HuggingFaceEmbeddings`

**What happens**
- `.env` is loaded so your API key becomes available via `os.getenv`.
- `Settings.llm` is set to a `Gemini` LLM instance (generation).
- `Settings.embed_model` is set to `HuggingFaceEmbeddings` (semantic vectors).

**Why it matters**
`Settings` acts like *global dependency injection*: downstream LlamaIndex objects use these models automatically.

---

## 2) Data Ingestion (CSV → DataFrame)

**Imports involved**
- `pandas as pd`

**Flow**
`pd.read_csv(csv_path)` returns a `pd.DataFrame` with rows/columns.

At this stage, the data is structured but not yet “semantic memory”.

---

## 3) Knowledge Unit Creation (DataFrame rows → Document[])

**Imports involved**
- `llama_index.core.Document`

**Flow**
Each DataFrame row is formatted into a readable text blob:

- Row → `"col: val, col2: val2, ..."`
- That text becomes `Document(text=...)`

This step strongly affects retrieval quality because it defines the “units” the retriever can return.

---

## 4) Semantic Memory Construction (Document[] → VectorStoreIndex)

**Imports involved**
- `llama_index.core.VectorStoreIndex`

**Flow**
`VectorStoreIndex.from_documents(documents)` embeds each `Document.text` using:

- embedder: `Settings.embed_model` (HuggingFaceEmbeddings)
- storage: an in-memory vector index

You now have semantic search over the CSV.

---

## 5) Retrieval + Generation (QueryEngine)

**Objects involved**
- `QueryEngine` (created by `index.as_query_engine(...)`)

**Runtime flow**
```
User query text
 → embed query (Settings.embed_model)
 → vector similarity search (top_k=5)
 → retrieved Document contexts
 → prompt assembly
 → LLM synthesis (Settings.llm / Gemini)
 → Answer
```

This is **classic RAG**: retrieval happens every time before generation, in a fixed pattern.

---

## One-Line Takeaway

> Simple RAG = **one index + one retriever + one LLM**, always “retrieve then answer”.

