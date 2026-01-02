# LangChain Chains Deep Dive (Python) — RetrievalQA, QA Chains, and More

This README is an **in-depth guide** to `langchain.chains` — especially the object you mentioned:
`RetrievalQA` (often misspelled as *ReturevakQA*).

It explains what chains are, why they exist, the most common chain types, and how they connect
to retrievers, vector stores, tools, and agents.

---

## 0. Quick Fix: What you meant

You wrote:
> `ReturevakQA`

The real class is typically:

```python
from langchain.chains import RetrievalQA
```

There are also related modern patterns:
- `create_retrieval_chain(...)`
- `create_stuff_documents_chain(...)`
- `ConversationalRetrievalChain` (older but still seen)

---

## 1. What is a “Chain” in LangChain?

A **Chain** is an object that:
1) Takes an input (like a question)
2) Runs a sequence of steps
3) Returns a final output

Chains exist so that you can reuse “pipelines” without rewriting glue code.

A chain is like a **function with a memory of how to call the LLM + its supporting steps**.

---

## 2. RetrievalQA — The classic RAG chain

### 2.1 What it does
`RetrievalQA` is a chain that combines:
- A **Retriever** (to fetch context docs)
- An **LLM** (to answer using that context)
- A **Prompt** (instructions)

Pipeline:

```
Question
  ↓
Retriever.invoke(question)
  ↓
Top-K Documents
  ↓
LLM(prompt + docs + question)
  ↓
Answer
```

### 2.2 Minimal example

```python
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI

qa = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(),
    retriever=retriever,          # any LangChain retriever
    return_source_documents=True  # super useful for debugging
)

result = qa.invoke({"query": "What is Apache Spark?"})
print(result["result"])
print(result["source_documents"])
```

### 2.3 Why it’s useful
- Quick RAG setup
- Standard API (`invoke`)
- Can return sources

### 2.4 Downsides (modern view)
`RetrievalQA` is convenient but somewhat “opaque.” Newer LangChain patterns are more modular
and explicit.

---

## 3. Newer “Composable” Chains (Recommended)

Modern LangChain favors building chains from smaller pieces.

### 3.1 `create_retrieval_chain`

```python
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template(
    "Answer the question using only the context.\n\nContext:\n{context}\n\nQ: {input}"
)

llm = ChatOpenAI()
combine_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, combine_chain)

out = rag_chain.invoke({"input": "What is Apache Spark?"})
print(out["answer"])
```

This is conceptually the same as RetrievalQA, but more explicit and composable.

---

## 4. ConversationalRetrievalChain

This chain adds chat history:

```
User question + history
  ↓
Question condensing (optional)
  ↓
Retriever
  ↓
LLM answer with history-aware context
```

Example:

```python
from langchain.chains import ConversationalRetrievalChain
from langchain_openai import ChatOpenAI

chat_rag = ConversationalRetrievalChain.from_llm(
    llm=ChatOpenAI(),
    retriever=retriever
)

chat_history = []
resp = chat_rag.invoke({"question": "What is Spark?", "chat_history": chat_history})
```

When to use:
- Chatbots
- Multi-turn Q&A

---

## 5. Document Combination Chains (How docs are fed into the model)

When retrieval returns multiple documents, you need a way to combine them. LangChain commonly uses:

### 5.1 Stuffing (stuff)
- Concatenate all docs into one context
- Cheapest and simplest
- Risk: context overflow

### 5.2 Map-Reduce
- Run LLM per doc, then combine summaries
- More expensive but scales

### 5.3 Refine
- Start with one doc, then incrementally refine answer using next docs

These are often exposed as “chain types” in RetrievalQA.

---

## 6. Important `langchain.chains` objects you’ll see

> Exact availability depends on LangChain version, but these are common in interviews and codebases.

### Core retrieval + QA
- `RetrievalQA`
- `ConversationalRetrievalChain`
- `create_retrieval_chain` (modern, LCEL-style)
- multi-retriever patterns (varies by version)

### Summarization
- `load_summarize_chain`
- map-reduce summarization
- refine summarization

### Router / Multi-prompt
- `MultiPromptChain`
- `LLMRouterChain`
- `RouterChain`

### Sequential / composed pipelines
- `SimpleSequentialChain`
- `SequentialChain`

### LLM-only utility chains
- `LLMChain` (older but still common)

---

## 7. How Chains Connect to the Objects You Already Know

You already understand:

- Vector DB (Databricks Vector Search, Chroma, Pinecone)
- VectorStore wrapper (`DatabricksVectorSearch(...)`)
- Retriever (`as_retriever(k=...)`)
- LLM (ChatGroq, ChatDatabricks, ChatOpenAI)

Chains are the **glue object**:

```
Vector Store → Retriever → Chain → Answer
```

---

## 8. Debugging & Best Practices

### Always enable sources in RAG chains
If supported:

```python
return_source_documents=True
```

### Add a reranker (flashrank / Cohere rerank)
Pattern:

```
Retriever (top 20) → Reranker → top 5 → LLM
```

---

## 9. Interview Cheat Sheet (One-liners)

- “A Chain is a reusable pipeline for LLM calls and supporting steps.”
- “RetrievalQA is a classic RAG chain: retrieve docs then answer.”
- “Modern LangChain uses composable chains like create_retrieval_chain.”
- “ConversationalRetrievalChain adds chat history awareness.”

---

## 10. Minimal Visual Mental Map

```
VectorStore
   ↓ as_retriever()
Retriever
   ↓
RetrievalQA / create_retrieval_chain
   ↓
LLM Answer (+ sources)
```

---

**File:** `langchain_chains_deep_dive.md`
