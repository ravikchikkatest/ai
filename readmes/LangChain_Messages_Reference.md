# LangChain Messages Reference

This document is a cleaned, navigation-free reference for the **LangChain `messages` module**.
It focuses only on the core content used by developers when building chat-based applications and agents.

Source conceptually based on:
https://reference.langchain.com/python/langchain/messages/

---

## Overview

LangChain represents conversations using **message objects**.  
Each message has:
- A **role** (who sent it)
- **Content** (text, tool calls, or structured data)
- Optional **metadata** (IDs, names, additional kwargs)

Messages are the fundamental unit exchanged between:
- Users
- AI models
- Tools
- Systems / agents

---

## Base Message

All message types inherit from `BaseMessage`.

### Common Fields

- `content`: The main message content (string or structured)
- `additional_kwargs`: Extra provider-specific data
- `response_metadata`: Metadata returned by the model
- `name`: Optional name (used for tools or function calls)
- `id`: Optional unique identifier

---

## HumanMessage

Represents user input.

```python
from langchain.messages import HumanMessage

msg = HumanMessage(content="Hello, how are you?")
```

Used when sending user prompts to a model.

---

## AIMessage

Represents a model-generated response.

```python
from langchain.messages import AIMessage

msg = AIMessage(content="I'm doing great!")
```

May also include:
- Tool calls
- Function calls
- Structured output metadata

---

## SystemMessage

Provides instructions or context to guide model behavior.

```python
from langchain.messages import SystemMessage

msg = SystemMessage(content="You are a helpful assistant.")
```

Typically injected at the start of a conversation.

---

## ToolMessage

Represents the output of a tool call.

```python
from langchain.messages import ToolMessage

msg = ToolMessage(
    content="Weather is sunny",
    tool_call_id="call_123"
)
```

Used internally by agents when tools are invoked.

---

## FunctionMessage (Legacy)

Represents function-call responses (older pattern).

```python
from langchain.messages import FunctionMessage

msg = FunctionMessage(
    name="get_weather",
    content="{"temp": 21}"
)
```

Modern implementations typically use `ToolMessage` instead.

---

## ChatMessage

A flexible message with an arbitrary role.

```python
from langchain.messages import ChatMessage

msg = ChatMessage(role="assistant", content="Hello")
```

Useful for custom or experimental roles.

---

## Message Conversion Utilities

LangChain provides helpers to convert messages to/from dictionaries.

### To Dict

```python
msg.to_dict()
```

### From Dict

```python
from langchain.messages import messages_from_dict

messages = messages_from_dict(list_of_dicts)
```

Useful for persistence and replaying conversations.

---

## Message Lists

Most LangChain APIs expect messages as a list:

```python
messages = [
    SystemMessage(content="You are helpful"),
    HumanMessage(content="Explain RAG"),
    AIMessage(content="RAG combines retrieval and generation...")
]
```

---

## When to Use Each Message Type

| Message Type | Use Case |
|-------------|---------|
| HumanMessage | User input |
| AIMessage | Model output |
| SystemMessage | Instructions / persona |
| ToolMessage | Tool execution results |
| ChatMessage | Custom roles |
| FunctionMessage | Legacy function calls |

---

## Best Practices

- Always use `SystemMessage` for behavioral instructions
- Preserve message order
- Prefer `ToolMessage` over legacy function messages
- Store messages as dicts for persistence
- Avoid mixing free-form text with structured tool outputs

---

## Related Concepts

- Agents
- Tool calling
- Structured output
- Conversation memory
- LangGraph state management

---

## References

Official documentation:  
https://reference.langchain.com/python/langchain/messages/
