# LangChain Runnables — Complete Study & Reference Guide

This README is a **deep, structured explanation of LangChain Runnables** (`langchain_core.runnables`).
It is written as a **learning + interview + system-design reference**, not just API notes.

This document explains:
- What Runnables are
- Why they exist
- All major Runnable types
- How they compose
- How they relate to Chains, Agents, Tools, and LangGraph

---

## 1. What Are Runnables?

A **Runnable** is LangChain’s **fundamental execution abstraction**.

> A Runnable is *anything that can be invoked with input and produces output*.

Formally:
```
input → Runnable → output
```

LLMs, prompts, retrievers, tools, chains, and even Python functions are all Runnables.

---

## 2. Why Runnables Exist (Key Insight)

Before Runnables:
- Chains were rigid
- Composition was difficult
- Async, streaming, batching were inconsistent

Runnables solve this by providing:
- A **unified execution interface**
- First-class support for:
  - streaming
  - batching
  - async
  - retries
  - fallbacks

---

## 3. Core Runnable Interface

All Runnables support:

- `invoke(input)` → single call
- `ainvoke(input)` → async
- `batch(inputs)` → batch processing
- `stream(input)` → token streaming
- `with_config()` → runtime configuration

This makes every component interoperable.

---

## 4. RunnableLambda

### What it is
Wraps a Python function as a Runnable.

### Example
```python
from langchain_core.runnables import RunnableLambda

r = RunnableLambda(lambda x: x.upper())
r.invoke("hello")  # "HELLO"
```

### Use cases
- Data transformation
- Glue logic
- Post-processing

---

## 5. RunnableSequence (`|` operator)

### What it is
Sequential composition of Runnables.

### Example
```python
chain = prompt | llm | output_parser
```

This replaces classic `LLMChain`.

### Mental model
```
A → B → C
```

---

## 6. RunnableParallel

### What it is
Runs multiple Runnables **in parallel** on the same input.

### Example
```python
from langchain_core.runnables import RunnableParallel

parallel = RunnableParallel({
    "summary": summarizer,
    "keywords": keyword_extractor
})
```

### Mental model
```
        ┌─ Runnable A
Input ──┼─ Runnable B
        └─ Runnable C
```

---

## 7. RunnablePassthrough

### What it is
Passes input through unchanged.

### Example
```python
from langchain_core.runnables import RunnablePassthrough

chain = {
  "context": retriever,
  "question": RunnablePassthrough()
}
```

### Why it matters
Critical for **prompt wiring**.

---

## 8. RunnableBranch

### What it is
Conditional routing based on input.

### Example
```python
from langchain_core.runnables import RunnableBranch

branch = RunnableBranch(
    (lambda x: "sql" in x, sql_chain),
    (lambda x: "doc" in x, rag_chain),
    fallback_chain
)
```

### This enables
- Adaptive RAG
- Tool routing
- Early decision-making

---

## 9. RunnableMap

### What it is
Maps inputs to structured outputs.

Often used implicitly via dict syntax.

### Example
```python
{
  "answer": llm,
  "sources": retriever
}
```

---

## 10. Config, Retries, and Fallbacks

Runnables support:
- `.with_retry()`
- `.with_fallbacks()`
- `.with_config()`

### Example
```python
llm.with_retry(stop_after_attempt=3)
```

This is **production-critical**.

---

## 11. Streaming & Async

Every Runnable supports streaming and async.

### Example
```python
async for chunk in llm.astream(prompt):
    print(chunk)
```

This is why Runnables replaced older abstractions.

---

## 12. Runnables vs Chains vs Agents

| Concept | Purpose |
|------|--------|
| Runnable | Execution primitive |
| Chain | Fixed pipeline (built from Runnables) |
| Agent | Dynamic controller that chooses Runnables |
| Tool | Runnable with side effects |
| Retriever | Runnable that fetches context |

Everything is a Runnable.

---

## 13. Runnables & LangGraph

LangGraph builds **graphs of Runnables**:
- Nodes = Runnables
- Edges = control flow

This is how:
- Agentic RAG
- Adaptive systems
- Stateful workflows

are built.

---

## 14. Interview One-Liners

- “Runnables unify execution across LangChain.”
- “Chains and agents are composed of Runnables.”
- “Runnables enable streaming, batching, retries, and composition.”
- “LangGraph is built on top of Runnables.”

---

## 15. Final Mental Model

> **Runnable = function + execution semantics**

If you understand Runnables, you understand LangChain.

---

**File:** `langchain_runnables_complete_guide.md`
