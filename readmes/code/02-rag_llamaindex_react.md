# tech_agentic_rag_llamaindex.md
## Agentic RAG with LlamaIndex (ReActAgent + Multiple Indexes) — With Import Object Map

This README explains the **technical object and data flow** of an **Agentic RAG** system built with **LlamaIndex**, where retrieval is exposed as tools and **a ReAct agent chooses which tool to use**.

It includes:
- A flow diagram **annotated with the exact imported objects and their import paths**
- The persistence path (StorageContext)
- Agent runtime loop (Thought → Act → Observe)

---

## Imports (Object Map)

Key imports and where they come from:

- `os` → `import os`
- `load_dotenv` → `from dotenv import load_dotenv`
- `Path` → `from pathlib import Path`

From `llama_index.core`:
- `Settings` → `llama_index.core.Settings`
- `StorageContext` → `llama_index.core.StorageContext`
- `load_index_from_storage` → `llama_index.core.load_index_from_storage`
- `SimpleDirectoryReader` → `llama_index.core.SimpleDirectoryReader`
- `VectorStoreIndex` → `llama_index.core.VectorStoreIndex`

Agent and tools:
- `ReActAgent` → `from llama_index.core.agent import ReActAgent`  (module: `llama_index.core.agent`)
- `QueryEngineTool` → `from llama_index.core.tools import QueryEngineTool` (module: `llama_index.core.tools`)

Models:
- `Groq` → `from llama_index.llms.groq import Groq` (module: `llama_index.llms.groq`)
- `HuggingFaceEmbedding` → `from llama_index.embeddings.huggingface import HuggingFaceEmbedding`
  (module: `llama_index.embeddings.huggingface`)

(You also imported `HuggingFaceInferenceAPIEmbedding`, but the shown code uses `HuggingFaceEmbedding`.)

---

## High-Level Flow (Data + Control) — With Import Paths

```
.env / OS
  │
  ▼
load_dotenv()                              (dotenv.load_dotenv)
os.getenv()                                (os.getenv)
  │
  ▼
Settings.llm = Groq(...)                   (llama_index.core.Settings + llama_index.llms.groq.Groq)
Settings.embed_model = HuggingFaceEmbedding(...)
                                           (llama_index.embeddings.huggingface.HuggingFaceEmbedding)
  │
  ▼
PDF Paths                                  (pathlib.Path)
  │
  ▼
SimpleDirectoryReader.load_data()           (llama_index.core.SimpleDirectoryReader)
  │
  ▼
Document[]                                 (llama_index.core.Document; produced internally)
  │
  ▼
VectorStoreIndex.from_documents(...)        (llama_index.core.VectorStoreIndex)
  │
  ├─────────────── persist / reload ──────────────────────────────┐
  │                                                               │
  │  storage_context.persist(persist_dir=...)                      │
  │       (llama_index.core.StorageContext via index.storage_context)
  │                                                               │
  │  StorageContext.from_defaults(persist_dir=...)                 │
  │       (llama_index.core.StorageContext)                        │
  │  load_index_from_storage(storage_context)                      │
  │       (llama_index.core.load_index_from_storage)               │
  │                                                               │
  └───────────────────────────────────────────────────────────────┘
  │
  ▼
index.as_query_engine(top_k=3)              (QueryEngine produced by llama_index)
  │
  ▼
QueryEngineTool.from_defaults(...)          (llama_index.core.tools.QueryEngineTool)
  │
  ▼
ReActAgent.from_tools(tools, llm=...)       (llama_index.core.agent.ReActAgent)
  │
  ▼
agent.chat(user_query)                     (ReActAgent.chat)
  │
  ▼
Answer (LLM-generated)                     (Groq via Settings.llm)
```

---

## Object-Level Pipeline (Uber + Lyft)

You build *two separate memories* and expose them as tools:

1) **Lyft memory**
- `SimpleDirectoryReader(input_files=[lyft_pdf])`
- `VectorStoreIndex.from_documents(lyft_docs)`
- `lyft_index.as_query_engine(top_k=3)`
- `QueryEngineTool(name="lyft_10k", query_engine=lyft_engine, ...)`

2) **Uber memory**
- `SimpleDirectoryReader(input_files=[uber_pdf])`
- `VectorStoreIndex.from_documents(uber_docs)`
- `uber_index.as_query_engine(top_k=3)`
- `QueryEngineTool(name="uber_10k", query_engine=uber_engine, ...)`

Then:
- `ReActAgent.from_tools([lyft_tool, uber_tool], llm=Settings.llm)`

---

## Runtime Execution (ReAct loop)

When you call:

```python
response = agent.chat(user_query)
```

the agent typically follows:

```
Thought (LLM decides a plan)
 → Act (choose a tool: uber_10k or lyft_10k)
 → Observe (tool returns retrieved context + draft answer)
 → Thought (LLM synthesizes / verifies)
 → Final Answer
```

The difference from Simple RAG is that retrieval is **not hardwired**. The agent chooses **which** retriever to invoke.

---

## One-Line Takeaway

> Agentic RAG = **multiple retrievers as tools + an agent that decides which tool to use before answering**.

