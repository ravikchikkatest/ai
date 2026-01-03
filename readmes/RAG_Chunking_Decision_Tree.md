# Chunking Decision Tree for RAG Applications

This document provides a **clear, exam-ready decision tree** for choosing the correct chunking strategy
when preparing data for Retrieval-Augmented Generation (RAG) systems.

It applies across domains such as **legal documents, customer support tickets, research papers,
technical manuals, and conversational data**.

---

## Why Chunking Matters

Chunking determines:
- Retrieval precision
- Context completeness
- Token efficiency
- Downstream answer quality

Poor chunking cannot be fixed later by reranking or prompting.

---

## Chunking Decision Tree

Follow these steps **in order**.

---

## STEP 1 — Is the document structured?

**Structured documents include:**
- Legal contracts
- Policies and regulations
- Technical specifications
- Standards and manuals

**Unstructured documents include:**
- Chat logs
- Narratives
- Emails
- Free-form text

### If YES → go to STEP 2  
### If NO → go to STEP 4

---

## STEP 2 — Does the document contain explicit sections or headings?

Examples:
- Articles, clauses, numbered sections
- Markdown headings
- Table of contents

### If YES → **Use Logical / Structural Chunking** ✅

**How:**
- Split by headings and subheadings
- Keep each section intact
- Preserve numbering and titles
- Ensure chunks remain under token limits

This is the **correct strategy for legal and policy documents**.

Then go to STEP 3.

---

## STEP 3 — Do any sections exceed token limits?

### If YES:
- Split *within the same section*
- Label parts clearly (e.g., “Section 4.1 – Part 1”)
- Never merge different sections

### If NO:
- Index sections as-is

Optional:
- Use minimal overlap (5–10%) **only within the same section**

---

## STEP 4 — Is the document unstructured but long?

Examples:
- Support tickets
- Research articles without clear sectioning
- Knowledge base articles

### Use **Semantic Chunking**

**How:**
- Chunk by topic or idea boundaries
- Use NLP signals or sentence similarity
- Keep chunks coherent

Optional:
- Add small overlap (10–20%) to preserve context

---

## STEP 5 — Is the text conversational or chronological?

Examples:
- Chat logs
- Email threads
- Transcripts

### Use **Sliding Window Chunking**

**How:**
- Fixed-size chunks (e.g., 300–500 tokens)
- Overlap adjacent chunks (10–30%)
- Preserve temporal order

---

## STEP 6 — Final Validation Checklist

Before indexing, verify:

- No chunk exceeds model token limits
- Each chunk is semantically complete
- Chunks do not mix unrelated sections
- Metadata (section titles, IDs) is preserved

---

## Common Exam Traps

❌ Equal-sized chunking without structure awareness  
❌ One-document-per-chunk for long texts  
❌ Excessive overlap as a primary strategy  
❌ Mixing multiple legal sections in one chunk  

---

## One-Line Rule (Memorize This)

> **Chunk by structure when structure exists; use overlap only when structure does not.**

---

## Summary Table

| Document Type | Recommended Chunking |
|-------------|----------------------|
| Legal / Policy | Logical / Structural |
| Technical Docs | Structural |
| Research Papers | Section-based |
| Support Tickets | Semantic |
| Chat Logs | Sliding Window |
| Narratives | Sliding Window + Overlap |

---

End of document.
