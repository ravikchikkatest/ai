# Cosine Similarity — Deep Dive for Vector Search, RAG, and Interviews

This README provides a **complete, from-first-principles explanation of Cosine Similarity**,
with intuition, math, examples, and how it is used in **embeddings, vector search, and RAG systems**.
It is written to help you both **understand deeply** and **answer interview questions confidently**.

---

## 1. What Is Cosine Similarity?

**Cosine similarity** measures how similar two vectors are by calculating the **angle between them**.

> It answers the question:
> “Do these two vectors point in the same direction?”

It does **not** care about vector length (magnitude), only direction.

---

## 2. The Formula

For two vectors **A** and **B**:

```
cosine_similarity(A, B) = (A · B) / (||A|| × ||B||)
```

Where:
- `A · B` = dot product
- `||A||` = magnitude of vector A
- Result range: **[-1, 1]**

---

## 3. Interpreting the Score

| Score | Meaning |
|-----|--------|
| 1.0 | Identical meaning |
| ~0.8 | Strongly related |
| ~0.5 | Weakly related |
| 0.0 | Unrelated |
| < 0 | Opposite direction |

---

## 4. Why Cosine Similarity Works for Text Embeddings

Text embeddings encode **semantic meaning as direction**, not magnitude.

Benefits:
- Scale-invariant
- Robust to token count
- Ideal for semantic search

---

## 5. Similarity vs Distance (Critical)

Many vector DBs internally convert:

```
cosine_distance = 1 - cosine_similarity
```

So:
- High similarity → low distance
- Low similarity → high distance

---

## 6. Cosine vs Other Metrics

| Metric | Measures | Best for |
|-----|--------|--------|
| Cosine | Angle | Text embeddings |
| Euclidean | Distance | Spatial data |
| Dot product | Angle + magnitude | Normalized vectors |

---

## 7. Normalization

If vectors are L2-normalized:

```
||A|| = 1
||B|| = 1
```
Then:
```
cosine_similarity = dot_product
```

---

## 8. RAG Pipeline Usage

```
Query → Embedding → Cosine Similarity → Top-K Chunks → LLM
```

---

## 9. Databricks Vector Search Context

Databricks Vector Search:
- Uses cosine similarity by default
- Optimizes via ANN indexes
- Abstracts metric implementation

---

## 10. Common Mistakes

❌ Treating cosine as distance  
❌ Ignoring normalization  
❌ Using Euclidean for text  
❌ Overthinking the math  

---

## 11. Interview One-Liners

- “Cosine similarity measures semantic alignment.”
- “Higher cosine similarity means closer meaning.”
- “Cosine similarity ignores magnitude.”

---

## 12. Mental Model

```
Meaning = direction
Similarity = angle
```

---

## 13. Final Takeaway

> Cosine similarity is foundational for semantic search and RAG systems.

---

**File:** `cosine_similarity_deep_dive.md`
