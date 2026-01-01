# Simple RAG with LlamaIndex — Mental Model & Notes

This README explains a **simple Retrieval-Augmented Generation (RAG)** pipeline using **LlamaIndex**, with a focus on *how to think about the objects and flow*, not just how to run the code.

The goal is that you can **rebuild this from memory**.

---

## The 5-Step RAG Skeleton

```python
# 1. GLOBAL BRAIN (set once)
Settings.llm = Gemini(...)
Settings.embed_model = HuggingFaceEmbeddings(...)

# 2. LOAD RAW DATA
df = pd.read_csv(csv_path)

# 3. CREATE KNOWLEDGE UNITS
documents = [
    Document(text=", ".join(f"{c}: {v}" for c, v in row.items()))
    for _, row in df.iterrows()
]

# 4. BUILD SEMANTIC MEMORY
index = VectorStoreIndex.from_documents(documents)

# 5. ASK QUESTIONS
query_engine = index.as_query_engine(similarity_top_k=5)
response = query_engine.query(user_input)
```

Think of it as:

```
Brain → Data → Knowledge → Memory → Questions
```

---

## 1️⃣ GLOBAL BRAIN (LLM + Embeddings)

```python
Settings.llm = Gemini(...)
Settings.embed_model = HuggingFaceEmbeddings(...)
```

This step wires the **intelligence layer** of the system.

- `Settings.llm` defines *how answers are generated* (reasoning, language, tone).
- `Settings.embed_model` defines *how meaning is represented* (text → vectors).

`Settings` works like **global dependency injection**. Once set, every index, retriever, and query engine automatically uses these models without you passing them around manually.

---

## 2️⃣ LOAD RAW DATA (Structured Data)

```python
df = pd.read_csv(csv_path)
```

This is a **data ingestion step**, not an AI step.

- Pandas loads structured data (rows + columns) into memory.
- At this stage, the data is *machine-readable* but **not LLM-friendly**.
- LLMs do not reason over tables — they reason over **text**.

---

## 3️⃣ CREATE KNOWLEDGE UNITS (Rows → Documents)

```python
documents = [
    Document(text=", ".join(f"{c}: {v}" for c, v in row.items()))
    for _, row in df.iterrows()
]
```

This is the **most important conceptual step** in RAG.

- A `Document` is the smallest retrievable unit in LlamaIndex.
- Each document should be **self-contained and meaningful**.
- Converting rows into readable `"column: value"` text preserves context.

Good documents = good retrieval.  
Bad documents = bad answers.

---

## 4️⃣ BUILD SEMANTIC MEMORY (Documents → Index)

```python
index = VectorStoreIndex.from_documents(documents)
```

This step builds **semantic memory**.

Internally:

```
Document text
 → Embedding model
 → Vectors
 → Vector index
```

From this point on, you search **by meaning**, not keywords.

---

## 5️⃣ ASK QUESTIONS (Retrieval + Reasoning)

```python
query_engine = index.as_query_engine(similarity_top_k=5)
response = query_engine.query(user_input)
```

This is where **RAG actually happens**.

The QueryEngine:
1. Embeds the user query  
2. Retrieves top-K relevant documents  
3. Injects them into a prompt  
4. Calls the LLM  
5. Returns a grounded answer  

---

## Mental Model (Memorise This)

> **Settings give the system a brain**  
> **Data becomes Documents**  
> **Documents become Memory**  
> **Memory answers Questions**

---

**File:** `readme_01_rag_simple_llamaindex.md`
