# LangChain Structured Output Guide

Structured output allows LangChain agents to return predictable, validated data structures instead of free-form text. This enables downstream systems to consume agent outputs directly as Python objects or JSON, without brittle parsing logic.

---

## Why Structured Output?

Traditional LLM responses require post-processing and parsing. Structured output removes that friction by enforcing schemas at generation time.

**Benefits**
- Strong guarantees on output shape
- Automatic validation and retries
- Native Python objects (Pydantic, dataclasses, TypedDict)
- Production-safe agent behavior

---

## How It Works

LangChain’s `create_agent` supports structured output through the `response_format` parameter.

The agent’s final state includes:

```python
result["structured_response"]
```

This is validated, schema-conformant data.

---

## Response Format Options

### 1. Schema Type (Recommended)

Pass a schema type directly and let LangChain choose the best strategy.

```python
response_format=ContactInfo
```

LangChain automatically selects:
- ProviderStrategy if the model supports native structured output
- ToolStrategy otherwise

---

### 2. ProviderStrategy (Native Structured Output)

Uses provider-native schema enforcement (most reliable).

```python
from pydantic import BaseModel
from langchain.agents import create_agent

class ContactInfo(BaseModel):
    name: str
    email: str
    phone: str

agent = create_agent(
    model="gpt-5",
    response_format=ContactInfo
)
```

Strict mode (LangChain >= 1.2):

```python
from langchain.agents.structured_output import ProviderStrategy

response_format = ProviderStrategy(
    schema=ContactInfo,
    strict=True
)
```

---

### 3. ToolStrategy (Tool Calling Fallback)

Used when native structured output is not available.

```python
from langchain.agents.structured_output import ToolStrategy

agent = create_agent(
    model="gpt-5",
    response_format=ToolStrategy(ContactInfo)
)
```

Supports:
- Pydantic models
- Dataclasses
- TypedDict
- JSON Schema
- Union types

---

## Supported Schema Types

| Type | Return Value |
|----|----|
| Pydantic | Model instance |
| Dataclass | Dataclass instance |
| TypedDict | Python dict |
| JSON Schema | Python dict |
| Union | Chosen schema instance |

---

## Union Schemas

```python
from typing import Union

response_format = ToolStrategy(Union[ProductReview, CustomerComplaint])
```

Useful for mixed-intent extraction and classification.

---

## Error Handling (ToolStrategy)

By default, LangChain retries automatically on:
- Schema validation errors
- Multiple structured outputs
- Type mismatches

### Custom Error Handling

```python
ToolStrategy(
    schema=ProductRating,
    handle_errors="Please provide a valid rating between 1–5."
)
```

Disable retries:

```python
ToolStrategy(
    schema=ProductRating,
    handle_errors=False
)
```

---

## Custom Tool Messages

```python
ToolStrategy(
    schema=MeetingAction,
    tool_message_content="Action item captured and added to notes."
)
```

---

## Model Compatibility

- Structured output support is detected dynamically from model profiles
- You may override profiles manually if needed

```python
custom_profile = {
    "structured_output": True
}
```

---

## Best Practices

- Prefer schema types directly
- Use Pydantic for validation-heavy pipelines
- Use ProviderStrategy when available
- Avoid free-form parsing in production

---

## When to Use Structured Output

Ideal for:
- Data extraction
- Classification
- RAG metadata
- Automation workflows
- Agent-to-agent communication

Not ideal for:
- Creative writing
- Open-ended chat

---

## References

- LangChain Structured Output Docs  
  https://docs.langchain.com/oss/langchain/structured-output
