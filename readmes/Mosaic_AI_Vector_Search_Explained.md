# Mosaic AI Vector Search — Concepts Explained (From First Principles)

This README explains **what HNSW, ANN, L2 distance, cosine similarity, and normalization actually mean**, how they fit together, and **why Databricks (Mosaic AI Vector Search) chose HNSW specifically**.

The goal is clarity, not jargon. If you understand this file, you understand how production-grade vector search works.

---

## 1. The Big Picture

Mosaic AI Vector Search is a **semantic retrieval system**.

Instead of searching for keywords, it searches for *meaning* by:
1. Converting data (text, images, code) into vectors called **embeddings**
2. Storing those vectors in a specialized index
3. Quickly finding vectors that are *most similar* to a query vector

This is the backbone of:
- RAG pipelines
- Semantic search
- Recommendation systems
- AI assistants

---

## 2. What Is an Embedding (Plain English)

An embedding is a **numeric fingerprint of meaning**.

Example:
- "I love dogs"
- "I adore puppies"

Even though the words differ, their embeddings are numerically close because the *meaning* is similar.

Embeddings live in high‑dimensional space (often 768–4096 dimensions).  
You cannot reason about them visually, so distance math is used.

---

## 3. Why Exact Search Does Not Work

If you store millions of embeddings:

- Exact nearest‑neighbor search compares every vector
- Time complexity grows linearly with data size
- This becomes unusable in production

**Solution:** Approximate Nearest Neighbor (ANN) search.

ANN trades *perfect accuracy* for *massive speed gains*.

---

## 4. ANN (Approximate Nearest Neighbor)

ANN answers this question:

> “Which vectors are *probably* closest to my query, without checking everything?”

Key idea:
- Avoid brute force
- Navigate the space intelligently
- Accept extremely small approximation error

ANN is standard in all modern vector databases.

---

## 5. What HNSW Actually Is

HNSW stands for **Hierarchical Navigable Small World**.

It is both:
- A **graph structure**
- A **search algorithm**

### Intuition

Imagine a city:
- Highways connect far regions
- Streets connect nearby houses

You do not search every street.  
You jump via highways, then refine locally.

### Structure

HNSW builds:
- Multiple graph layers
- Top layers: few nodes, long‑range links
- Bottom layer: many nodes, short‑range links

### Search Process

1. Start at the top layer
2. Jump toward the approximate region
3. Move down layer by layer
4. Do fine‑grained local search at the bottom

This gives:
- Very fast search
- High recall
- Excellent scaling

---

## 6. Why Databricks Picked HNSW Specifically

Databricks evaluated vector search as **infrastructure**, not a research demo.

HNSW wins because:

### 1. High Recall at Low Latency
- Finds very accurate neighbors
- Consistently fast (single‑digit ms)
- Ideal for real‑time applications

### 2. Incremental Updates
- Vectors can be added dynamically
- No full index rebuild required
- Critical for continuously updated data (logs, documents, chats)

### 3. Production‑Proven
- Used in FAISS, Milvus, Weaviate, OpenSearch
- Battle‑tested at billion‑scale

### 4. Predictable Performance
- Stable latency curves
- Works well across different embedding distributions
- Easier to operate at scale

### 5. Fits Databricks’ Philosophy
Databricks optimizes for:
- Reliability over novelty
- Unified data + AI pipelines
- Enterprise workloads

HNSW aligns perfectly with these constraints.

---

## 7. L2 Distance (What It Really Means)

L2 distance is **straight‑line distance** between two vectors.

Smaller distance → more similar  
Larger distance → less similar

Why use L2?
- Fast to compute
- Works well with graph‑based indexes
- Numerically stable

Mosaic AI Vector Search uses **L2 distance by default**.

---

## 8. Cosine Similarity (Direction, Not Size)

Cosine similarity measures:
> “Are these vectors pointing in the same direction?”

It ignores magnitude.

This matters when:
- You care about meaning direction
- Embedding norms vary

Cosine similarity is very popular in NLP.

---

## 9. Normalization: The Key Connection

Normalization means scaling every vector so its length equals 1.

After normalization:
- All vectors lie on a unit sphere
- Length differences disappear
- Only direction remains

### Critical Insight

When vectors are normalized:

> **Ranking by L2 distance = ranking by cosine similarity**

This is why Mosaic AI says:

> “If you want cosine similarity, normalize your embeddings before indexing.”

They get cosine behavior *without* needing a separate metric.

---

## 10. How Everything Fits Together

Typical Mosaic AI Vector Search flow:

1. Generate embeddings
2. (Optional) Normalize embeddings if cosine similarity is desired
3. Store embeddings in an HNSW index
4. Perform ANN search using L2 distance
5. Retrieve most semantically similar results

One index.  
One distance metric.  
Multiple similarity behaviors.

Elegant and scalable.

---

## 11. Why This Matters for RAG Pipelines

In RAG:
- Retrieval quality determines answer quality
- Latency impacts user experience
- Index updates are frequent

HNSW + ANN + normalized embeddings gives:
- Fast retrieval
- High relevance
- Production‑ready reliability

This is why Mosaic AI Vector Search is suitable for real‑world RAG systems.

---

## 12. One‑Line Summary

Mosaic AI Vector Search uses **HNSW** for fast ANN retrieval, **L2 distance** for efficiency, and **embedding normalization** to achieve cosine‑similarity behavior — a design chosen by Databricks for scalability, reliability, and real‑time performance.

---

End of README.
