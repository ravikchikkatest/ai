# LangChain Text Splitters — Deep Dive Guide

This README is a **comprehensive, in-depth guide** to **LangChain text splitters**,
covering **why they exist**, **how they work**, and **when to use each type**.

Text splitters are one of the **most critical but misunderstood** parts of RAG systems.

---

## 1. Why Text Splitters Exist (First Principles)

LLMs have **context limits**.
Vector databases work best with **semantically coherent chunks**.

Text splitters exist to:
- Break large documents into chunks
- Preserve semantic meaning
- Optimize retrieval quality
- Reduce embedding cost

> Bad chunking = bad RAG, no matter how good the model is.

---

## 2. Where Text Splitters Sit in the RAG Pipeline

```
Raw Document
   ↓
Text Splitter
   ↓
Chunks
   ↓
Embeddings
   ↓
Vector Store
```

---

## 3. Base Classes in LangChain

All splitters inherit from:

```python
langchain.text_splitter.TextSplitter
```

---

## 4. CharacterTextSplitter

### Description
Splits text purely by character count.

```python
from langchain.text_splitter import CharacterTextSplitter

splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_text(text)
```

---

## 5. RecursiveCharacterTextSplitter

### Description
Recursively splits using paragraph, line, word boundaries.

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter
```

---

## 6. SentenceSplitter

### Description
Splits by sentence boundaries for semantic coherence.

```python
from llama_index.core.node_parser import SentenceSplitter
```

---

## 7. TokenTextSplitter

### Description
Splits text based on token count.

```python
from langchain.text_splitter import TokenTextSplitter
```

---

## 8. SemanticChunker

### Description
Uses embeddings to split text by meaning.

```python
from langchain.text_splitter import SemanticChunker
```

---

## 9. Markdown & HTML Splitters

- MarkdownHeaderTextSplitter
- HTMLHeaderTextSplitter

---

## 10. Interview Cheat Sheet

| Scenario | Splitter |
|--------|----------|
| Default RAG | RecursiveCharacterTextSplitter |
| High-quality QA | SentenceSplitter |
| Token limits | TokenTextSplitter |
| Semantic QA | SemanticChunker |

---

## 11. Final Takeaway

> Text splitting quality directly impacts retrieval quality.

---

**File:** `langchain_text_splitters_deep_dive.md`
