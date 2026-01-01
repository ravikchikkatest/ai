# Agentic RAG with LlamaIndex (ReAct + Multiple Indexes)

This README explains the **mental model** behind an **Agentic RAG system** built with **LlamaIndex**, using:

- Multiple document indexes (Uber + Lyft 10-K PDFs)
- Query engines wrapped as tools
- A ReAct-style agent that decides *which tool to use*

The goal is not just to run the code, but to **understand the flow well enough to rebuild it from memory**.

---

## High-Level Mental Map

Think of the system as:

```
Environment
   ↓
Indexes (Memory)
   ↓
Query Engines (Capabilities)
   ↓
Tools (Named Skills)
   ↓
Agent (Planner + Reasoner)
   ↓
Answer
```

This is **Agentic RAG**: retrieval is no longer fixed — the agent chooses *when and where* to retrieve.

---

## 1️⃣ Environment Setup (Global Brain)

```python
Settings.llm = Groq(...)
Settings.embed_model = HuggingFaceEmbedding(...)
```

This step wires the **global intelligence** of the system.

- The LLM (Groq + LLaMA) handles reasoning, planning, and final answers
- The embedding model converts text into vectors for semantic search

`Settings` acts as **global dependency injection**. Once configured, every index and query engine automatically uses these models.

If this step is wrong, everything still runs — but retrieval quality and reasoning suffer.

---

## 2️⃣ Raw Data → Documents (PDF Ingestion)

```python
SimpleDirectoryReader(input_files=[...]).load_data()
```

This step converts **raw files (PDFs)** into `Document` objects.

Mental model:
- PDFs are *unstructured data*
- `Document` is the atomic knowledge unit
- Each document chunk represents retrievable context

At this stage, the data is readable by the LLM but not yet searchable by meaning.

---

## 3️⃣ Documents → Index (Semantic Memory)

```python
VectorStoreIndex.from_documents(docs)
```

This step builds **semantic memory**.

Internally:

```
Document text
 → Embeddings
 → Vectors
 → Vector index
```

Each company (Uber, Lyft) gets its **own index**, which is important:
- Memory is separated
- Retrieval can be targeted
- Tools can represent distinct knowledge domains

---

## 4️⃣ Persistence (Long-Term Memory)

```python
index.storage_context.persist(...)
load_index_from_storage(...)
```

This step makes memory **durable**.

Mental model:
- First run: build memory
- Later runs: reload memory instantly

This avoids recomputing embeddings and enables production-style workflows.

---

## 5️⃣ Index → Query Engine (Capabilities)

```python
index.as_query_engine(similarity_top_k=3)
```

A `QueryEngine` is a **capability**, not just a function.

It encapsulates:
- Retrieval logic
- Prompt construction
- LLM calls

Think:
> "This object knows how to answer questions about Uber (or Lyft)."

---

## 6️⃣ Query Engines → Tools (Named Skills)

```python
QueryEngineTool.from_defaults(...)
```

This step wraps each query engine as a **tool the agent can choose**.

Mental model:
- Tool = named skill + description
- The description teaches the agent *when to use it*

Example:
- `uber_10k` → "Questions about Uber financials"
- `lyft_10k` → "Questions about Lyft financials"

This is the key transition from **RAG** to **Agentic RAG**.

---

## 7️⃣ Agent Creation (Planner + Executor)

```python
ReActAgent.from_tools(tools, llm=Settings.llm)
```

The agent now:
- Reads the user question
- Plans what to do
- Chooses the correct tool
- Retrieves context
- Synthesizes an answer

ReAct = **Reason + Act**

The agent decides:
- *Which* index to query
- *Whether* to query more than once

You no longer hardcode retrieval flow.

---

## 8️⃣ Runtime Loop (Interactive Reasoning)

```python
response = agent.chat(user_query)
```

At runtime, the flow is:

```
User question
 → Agent reasoning
 → Tool selection
 → Retrieval
 → LLM synthesis
 → Answer
```

The user interacts with **one agent**, not multiple indexes.

---

## RAG vs Agentic RAG (This Example)

| Aspect | Classic RAG | This Code |
|-----|------------|----------|
| Retrieval | Fixed | Agent-chosen |
| Indexes | One | Multiple |
| Control flow | Linear | Planned |
| Tool choice | No | Yes |
| Adaptability | Low | High |

---

## Memorisation Shortcut (Very Important)

Say this out loud:

> **Indexes are memory**  
> **Query engines are capabilities**  
> **Tools are named skills**  
> **Agent decides what to use**

If you remember that, you understand this system.

---

## One-Line Takeaway

> **This is Agentic RAG: the LLM decides how to retrieve before it decides how to answer.**

---

**File:** `readme_02_agentic_rag_llamaindex.md`
