# LangChain Community Utilities — Deep Dive Reference Guide

This document is a **comprehensive study guide** for `langchain_community.utilities`.
It explains **what utilities are**, **why they exist**, and gives **clear examples** for the most important ones
such as `WikipediaAPIWrapper`, search utilities, and API wrappers.

---

## 1. What Are LangChain Utilities?

Utilities are **low-level helper wrappers** around external services.

> Utilities are NOT agents, NOT tools by default, and NOT retrievers.

They simply:
- Talk to external APIs
- Normalize responses
- Return clean Python data

Utilities are usually **wrapped by Tools**.

---

## 2. Utilities vs Tools vs Retrievers

| Concept | Purpose | LLM Decides? |
|------|------|------|
| Utility | Raw API wrapper | ❌ |
| Tool | Action surface | ✅ |
| Retriever | Fetch context | ❌ |
| Agent | Decision-maker | ✅ |

Pipeline:
```
Utility → Tool → Agent
```

---

## 3. WikipediaAPIWrapper

### Example
```python
from langchain_community.utilities import WikipediaAPIWrapper

wiki = WikipediaAPIWrapper(top_k_results=3)
wiki.run("Databricks Mosaic AI")
```

Keyword-based factual retrieval.

---

## 4. TavilySearchAPIWrapper

```python
from langchain_community.utilities import TavilySearchAPIWrapper

tavily = TavilySearchAPIWrapper()
tavily.run("LangChain Runnables")
```

---

## 5. DuckDuckGoSearchRun

```python
from langchain_community.utilities import DuckDuckGoSearchRun

ddg = DuckDuckGoSearchRun()
ddg.run("latest LLM benchmarks")
```

---

## 6. ArxivAPIWrapper

```python
from langchain_community.utilities import ArxivAPIWrapper

arxiv = ArxivAPIWrapper()
arxiv.run("retrieval augmented generation")
```

---

## 7. PythonREPL

```python
from langchain_community.utilities import PythonREPL

repl = PythonREPL()
repl.run("10 * 5")
```

---

## 8. SQLDatabase

```python
from langchain_community.utilities import SQLDatabase

db = SQLDatabase.from_uri("sqlite:///example.db")
```

---

## 9. RequestsWrapper

```python
from langchain_community.utilities import RequestsWrapper

requests = RequestsWrapper()
requests.get("https://api.example.com")
```

---

## 10. Architecture View

```
External API → Utility → Tool → Agent
```

---

## 11. Interview Mental Model

```
Utilities = Hands
Tools     = Buttons
Agents    = Brain
```

---

**File:** `langchain_community_utilities_deep_dive.md`
