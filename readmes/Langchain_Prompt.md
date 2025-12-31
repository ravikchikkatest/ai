A LangChain prompt template is a reusable way to build prompts for language models. It gives you a clear structure to follow, while making it easy to customize prompts and save time.

LangChain’s templates help keep your prompts consistent, and make the model’s answers more predictable and reliable. Over time, **they also improve results by reducing randomness in how prompts are written**.

A prompt template usually consists of two things:

1. A text prompt, which is just a chunk of natural language. It can be plain text, or it can have placeholders like `{variable}` that get filled in with real values when you use it.  
2. Optional formatting rules, so you can control how the final prompt looks, like whether text should be bold, in all caps, or styled a certain way.

Once you fill in the variables, the template turns into a finished prompt that gets sent to the LLM to generate a response.

In our experience, LangChain’s prompt templates work well for getting started and handling most tasks, but when your app scales up and starts making 100+ LLM calls, **its built-in system starts to feel clunky and hard to scale**: managing all the different components (using LangChain and LangSmith), like chains and iterations, becomes messy fast.

That’s why we designed Mirascope and Lilypad to make LLM app development easier.

[Mirascope](https://github.com/mirascope/mirascope) is a user-friendly LLM toolkit that offers just the right abstractions to build smarter apps, without the clutter, confusion, or guesswork ([jump down](#how-mirascope-makes-prompt-templates-easier-to-build) to read more). [Lilypad](https://github.com/mirascope/lilypad) is a prompt management and observability tool that makes use cases for tracing and versioning prompts easier, to test what’s working ([skip to here](#how-lilypad-makes-structuring-calls-and-prompts-easier) to read more about Lilypad).

We dive into how LangChain prompt templates work and show you ways of iterating and versioning prompts using Mirascope and Lilypad.

## 3 Types of LangChain Prompt Templates

LangChain offers different template classes:

* String `PromptTemplate` for creating basic prompts.  
* `ChatPromptTemplate` for chat-based prompts with multiple messages.  
* `MessagesPlaceholder` for injecting a dynamic list of messages (such as a conversation history).

### `PromptTemplate`: Simple String-Based Prompts

This generates prompts by filling in blanks in a string, and is perfect for completion-style models that expect a single text input (`text-davinci-003` or similar).

You define a prompt with placeholders using standard Python format syntax. At runtime, these get resolved to generate the final prompt string:

```python
from langchain_core.prompts import PromptTemplate

example_prompt = PromptTemplate.from_template("Share an interesting fact about {animal}.")  # infers 'animal' as input variable

# Format the template with a specific animal
filled_prompt = prompt.format(animal="octopus")
print(filled_prompt)

#> Share an interesting fact about octopus.
```

You can have multiple placeholders like `{animal}` and `{topic}` as needed, or none at all if the prompt is always the same.

### `ChatPromptTemplate`: Chat-Style Prompt with Roles

Chat-based models (like GPT\-4, Claude, or Gemini) don’t just take in a plain string. They expect a sequence of messages where each message has a role (like "system", "user", or "assistant") and some content.

LangChain's `ChatPromptTemplate` helps you build these kinds of prompts cleanly and dynamically. Think of it as a way to define a chat scenario with placeholders, then fill in the values when needed.

```python
from langchain_core.prompts import ChatPromptTemplate

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a patient tutor who explains things clearly."),
    ("human", "Can you explain {concept} like I'm five?")
])

# Fill in the template with a specific concept
formatted_messages = chat_prompt.format_messages(concept="gravity")

print(formatted_messages)
```

After formatting, this will give you something like:

```
[
    SystemMessage(content="You are a patient tutor who explains things clearly.", role="system"),
    HumanMessage(content="Can you explain gravity like I'm five?", role="user")
]
```

Each item in that list is a structured message that includes both the role and the content, exactly how chat-based LLMs expect it. This is handy because you don’t need to manually construct message objects — the template handles it for you.

### `MessagesPlaceholder`: Inserting Dynamic Chat History into a Prompt

When you’re working with chat-based models, you often want to include conversation history (or some sequence of messages). `MessagesPlaceholder` acts as a stand-in for a dynamic list of messages you’ll provide at runtime.

Imagine we’re building a career coach bot that remembers previous questions and answers:

```python
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful career coach."),
    MessagesPlaceholder("conversation"),  # Dynamic history insertion
    ("human", "{current_question}")
])

# Define history using proper message objects
conversation_history = [
    HumanMessage(content="How do I prepare for a job interview?"),
    AIMessage(content="Start by researching the company and practicing common questions.")
]

formatted_messages = chat_prompt.format_messages(
    conversation=conversation_history,
    current_question="Should I send a thank-you email afterward?"
)

print(formatted_messages)
```

The output will be a list of message objects like:

```
[
    SystemMessage(content="You are a helpful career coach.", role="system"),
    HumanMessage(content="How do I prepare for a job interview?", role="user"),
    AIMessage(content="Start by researching the company and practicing common questions.", role="assistant"),
    HumanMessage(content="Should I send a thank-you email afterward?", role="user")
]
```

This setup allows you to manage dynamic dialogue context without manual overhead. When we used `MessagesPlaceholder("conversation")`, it was replaced with the full history of back-and-forth messages between the user and assistant.

The messages were injected exactly in order, so you didn’t have to manually merge or format them, since LangChain took care of that behind the scenes.
