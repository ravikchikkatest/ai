# Legal Document RAG System (FAISS + OpenAI + Gemini)

This project demonstrates a **production-style Retrieval-Augmented Generation (RAG) pipeline** for analyzing legal documents such as NDAs, service agreements, and licensing contracts.

---

## What This System Does

- Accepts legal documents (PDF, DOCX, TXT)
- Splits them into semantic chunks
- Converts chunks into embeddings
- Stores them in a FAISS vector index
- Retrieves the most relevant clauses based on a user query
- Uses an LLM to answer questions grounded only in retrieved text

This avoids hallucinations and reduces LLM cost.

---

## Core Technologies

### FAISS (Facebook AI Similarity Search)
Used for fast vector similarity search.

### OpenAI Embeddings
Convert text into numeric vectors for semantic comparison.

### Google Gemini
Used as the reasoning LLM for answering questions over retrieved content.

### Streamlit
Lightweight UI for document upload and querying.

---

## Why RAG Is Needed for Legal Docs

Legal documents:
- Are long
- Contain precise language
- Require grounded answers

RAG ensures answers come **from the document itself**, not model memory.

---

## High-Level Architecture

1. Document Upload
2. Text Extraction
3. Chunking
4. Embedding Generation
5. FAISS Index Storage
6. Query Embedding
7. Similarity Search
8. Context Injection into LLM
9. Final Answer

---

## Example Queries

- "What are the termination conditions?"
- "How long does the confidentiality obligation last?"
- "Summarize payment obligations."

---

## Why FAISS Instead of a Traditional Database

| Feature | Traditional DB | FAISS |
|------|---------------|-------|
| Stores vectors | ❌ | ✅ |
| Semantic search | ❌ | ✅ |
| Scales to millions | ❌ | ✅ |
| ML-native | ❌ | ✅ |

---

## Clearing or Resetting the Vector Store

Simply delete:
- `faiss.index`
- `faiss_meta.pkl`

FAISS is stateless beyond these files.

---

## Production Considerations

- Use object storage (S3/GCS) for FAISS files
- Wrap retrieval in a FastAPI service
- Run Streamlit or frontend separately
- Add auth & audit logs for legal compliance

---

## Future Enhancements

- Clause classification
- Multi-document comparison
- Citation highlighting
- Role-based access
- Kubernetes deployment

---

## Summary

FAISS acts as long-term memory.
LLMs act as reasoning engines.
RAG connects the two safely and efficiently.

This architecture is widely used in real-world AI systems.

