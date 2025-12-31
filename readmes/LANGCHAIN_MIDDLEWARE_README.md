
# LangChain Middleware – Complete README

This document consolidates LangChain middleware documentation:
- Overview
- Built-in middleware
- Custom middleware

Source docs:
https://docs.langchain.com/oss/python/langchain/middleware/overview
https://docs.langchain.com/oss/python/langchain/middleware/built-in
https://docs.langchain.com/oss/python/langchain/middleware/custom

---

## What is Middleware?

Middleware in LangChain lets you intercept and modify agent execution at runtime.
It runs before/after model calls, tool calls, and agent execution.

Use cases:
- Guardrails
- Summarization
- Retries & fallbacks
- Human-in-the-loop
- Logging and observability
- Dynamic prompt or model selection

---

## How Middleware Fits

Agent → Middleware → Model / Tools → Middleware → Agent

Middleware is injected when creating the agent and runs automatically.

---

## Built-in Middleware

| Middleware | Purpose |
|-----------|--------|
| SummarizationMiddleware | Summarize long conversations |
| HumanInTheLoopMiddleware | Pause execution for approval |
| ModelCallLimitMiddleware | Limit model calls |
| ToolCallLimitMiddleware | Limit tool executions |
| ModelFallbackMiddleware | Fallback to backup model |
| ModelRetryMiddleware | Retry model calls |
| ToolRetryMiddleware | Retry tool calls |
| PIIMiddleware | Detect/redact PII |
| TodoListMiddleware | Planning & task tracking |

---

## Using Built-in Middleware

```python
from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware
from langchain.chat_models import init_chat_model

llm = init_chat_model("gpt-4o")

middleware = SummarizationMiddleware(
    model=llm,
    max_tokens_before_summary=3000,
    messages_to_keep=20
)

agent = create_agent(
    model=llm,
    tools=[],
    middleware=[middleware]
)

agent.invoke({"messages": [{"role": "user", "content": "Hello"}]})
```

---

## Custom Middleware

There are two styles:
1. Lifecycle hooks
2. Wrap-style interceptors

---

## Lifecycle Hook Example

```python
from langchain.agents.middleware import AgentMiddleware

class LoggingMiddleware(AgentMiddleware):
    def before_model(self, state, runtime):
        print("Before model call")

    def after_model(self, state, runtime):
        print("After model call")
```

---

## Wrap Model Call Example

```python
from langchain.agents.middleware import wrap_model_call

@wrap_model_call
def dynamic_model(request, handler):
    if len(request.messages) > 10:
        return handler(request.override(model="gpt-4o"))
    return handler(request)
```

---

## Wrap Tool Call Example

```python
from langchain.agents.middleware import wrap_tool_call

@wrap_tool_call
def log_tool(request, handler):
    print("Tool:", request.tool_call["name"])
    return handler(request)
```

---

## Custom State Middleware

```python
from langchain.agents.middleware import AgentMiddleware
from typing_extensions import NotRequired

class CounterState(dict):
    model_calls: NotRequired[int]

class CallCounter(AgentMiddleware[CounterState]):
    state_schema = CounterState

    def after_model(self, state, runtime):
        state["model_calls"] = state.get("model_calls", 0) + 1
        return state
```

---

## Key Rules

- Middleware order matters
- One middleware should do one thing
- Avoid side effects
- Use built-ins before custom

---

## Summary

Middleware gives LangChain agents production-grade control:
- Safe
- Observable
- Extensible
- Deterministic

