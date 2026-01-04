# Large Language Model Architectures — Quick Guide

This document provides a clear, exam-ready overview of common LLM architectures such as
Dense models, Mixture-of-Experts (MoE), and related variants.

---

## Why Architecture Matters

Model architecture determines:
- Quality vs efficiency trade-offs
- Inference speed and cost
- Scalability
- Suitability for RAG, coding, or reasoning tasks

---

## 1. Dense Models

Description:
All parameters are active for every token.

Examples:
- LLaMA2-70B
- GPT-3 style models
- Early MPT models

Strengths:
- Simple and stable
- Predictable behavior
- Easier fine-tuning

Weaknesses:
- Expensive inference
- Poor scaling efficiency

---

## 2. Mixture-of-Experts (MoE)

Description:
Model contains multiple expert subnetworks.
Only a small subset is activated per token via a routing mechanism.

Examples:
- DBRX
- Mixtral
- Grok-1

Strengths:
- High quality per FLOP
- Faster inference than dense models
- Scales efficiently

Weaknesses:
- Complex training
- Harder to fine-tune

---

## 3. Sparse Models

Description:
General class of models where not all parameters are active.
MoE is the most common example.

---

## 4. Decoder-Only Transformers

Description:
Autoregressive models that generate text token by token.

Examples:
- GPT family
- LLaMA
- DBRX

---

## 5. Encoder-Decoder Models

Description:
Separate encoder and decoder components.

Examples:
- T5
- BART

Best for:
Translation and summarization tasks.

---

## 6. Retrieval-Augmented Systems (RAG)

Note:
RAG is a system architecture, not a model architecture.
It combines retrieval with an LLM.

---

## Architecture Comparison

Dense:
- Simple
- Expensive

MoE:
- Efficient
- Complex

Encoder-Decoder:
- Structured tasks

Decoder-only:
- Chat and generation

---

## Exam Memory Anchors

- Dense = simple, expensive
- MoE = efficient, scalable
- DBRX = MoE
- LLaMA2 = Dense
- RAG is not a model architecture

---

End of document.
