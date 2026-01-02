# LangChain Runnables — Visual Diagrams & Mental Models

This README provides **clear, interview-ready diagrams** to understand how **LangChain Runnables** work.
Use this as a **visual memory aid** for system design, interviews, and real-world architecture.

---

## 1. Runnable Core Mental Model

```
Input
  │
  ▼
┌─────────────┐
│  Runnable   │
└─────────────┘
  │
  ▼
Output
```

If something can be invoked, streamed, batched, retried, or composed — **it is a Runnable**.

---

## 2. RunnableSequence (`|`) — Linear Pipeline

```
User Input
   │
   ▼
┌────────┐
│ Prompt │
└────────┘
   │
   ▼
┌──────┐
│ LLM  │
└──────┘
   │
   ▼
┌──────────────┐
│ OutputParser │
└──────────────┘
   │
   ▼
 Final Answer
```

Python mental mapping:
```python
prompt | llm | parser
```

Think: **Unix pipes for AI**.

---

## 3. RunnableParallel — Fan-out

```
             ┌──────────────┐
Input ─────▶ │ Summarizer   │ ──▶ Summary
             └──────────────┘
             ┌──────────────┐
        ───▶ │ Keyword Ext. │ ──▶ Keywords
             └──────────────┘
             ┌──────────────┐
        ───▶ │ Sentiment    │ ──▶ Sentiment
             └──────────────┘
```

Python mental mapping:
```python
{
  "summary": summarizer,
  "keywords": extractor,
  "sentiment": classifier
}
```

---

## 4. RunnablePassthrough — Input Wiring

```
                ┌─────────────┐
User Question ─▶│ Retriever   │──▶ Context
                └─────────────┘
        │
        └──────────────▶ Question (unchanged)
```

Used heavily in RAG prompt wiring.

---

## 5. RunnableBranch — Conditional Routing (Adaptive RAG)

```
                    ┌──────────────┐
Query ──▶ Condition │  SQL Chain   │──▶ Answer
         (is metric?)└──────────────┘
              │
              │ else
              ▼
         ┌──────────────┐
         │   RAG Chain  │──▶ Answer
         └──────────────┘
```

This enables **Adaptive RAG**.

---

## 6. RunnableMap — Structured Outputs

```
Input
 │
 ▼
┌────────────────────────┐
│  RunnableMap           │
│ ┌─────────┐ ┌────────┐│
│ │ Answer  │ │ Sources││
│ └─────────┘ └────────┘│
└────────────────────────┘
```

Often written as:
```python
{
  "answer": llm,
  "sources": retriever
}
```

---

## 7. Classic RAG (Runnable Composition)

```
User Question
   │
   ▼
┌────────────┐
│ Retriever  │
└────────────┘
   │
   ▼
┌────────┐
│ Prompt │
└────────┘
   │
   ▼
┌──────┐
│ LLM  │
└──────┘
   │
   ▼
 Answer
```

---

## 8. Agentic RAG (Tools as Runnables)

```
User Query
   │
   ▼
┌────────────┐
│   Agent    │
└────────────┘
   │ decides
   ▼
┌────────────┐
│   Tool     │──▶ Result
└────────────┘
   │
   ▼
┌──────┐
│ LLM  │──▶ Final Answer
└──────┘
```

---

## 9. Full Production Diagram (Hybrid Agentic RAG)

```
                    ┌──────────────┐
User Query ───────▶ │   Router     │
                    └──────┬───────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
┌────────────┐      ┌────────────┐     ┌──────────────┐
│ SQL Tool   │      │ Vector RAG │     │ Web / Wiki   │
└────────────┘      └────────────┘     └──────────────┘
        │                  │                  │
        └──────────────┬───┴───────┬──────────┘
                       ▼           ▼
                   ┌──────────────────┐
                   │   Final LLM      │
                   └──────────────────┘
```

---

## 10. One Mental Model to Remember

```
Runnable = Node
Chain    = Line
Branch   = Decision
Parallel = Fan-out
Agent    = Controller
```

If you understand this, you understand LangChain.

---

**File:** `langchain_runnables_diagrams.md`
