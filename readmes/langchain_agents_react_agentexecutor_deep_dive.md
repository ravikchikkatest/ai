# LangChain Agents Deep Dive (ReAct + AgentExecutor + “create_*_agent” helpers)

> Scope: **Python LangChain** agent creation helpers (especially `langchain.agents.react.agent`) plus **AgentExecutor**.  
> Notes: LangChain has been evolving quickly. Some “v0.3 reference” pages are labeled outdated, while newer “v1.x reference” surfaces **`create_agent`** (graph-based). I’ll point out what is **legacy vs current** and show how they connect. citeturn1view0turn3view0turn4view0

---

## 0) The 2 worlds: “classic AgentExecutor” vs “graph-based create_agent”

### A) Classic (v0.x style): `create_*_agent(...)` → wrap with `AgentExecutor(...)`
This is the pattern you’ve seen in notebooks:

1. Pick an agent “brain style” (`create_react_agent`, `create_tool_calling_agent`, etc.)
2. Give it **tools** and a **prompt** (depending on the helper)
3. Wrap it in `AgentExecutor` to run the loop (iterations, tool calls, parsing errors, etc.) citeturn3view0turn4view0

### B) Newer (v1.x style): `langchain.agents.create_agent(...)` returns a **CompiledStateGraph**
The newer reference docs expose **`create_agent(...)`** as a “create an agent graph that calls tools in a loop until a stopping condition is met.” It supports model strings, middleware, state schemas, checkpointing, stores, interrupts, etc. citeturn1view0

**Mental model:**
- Classic: `AgentExecutor` is the “runtime loop manager”.
- New: `create_agent` gives you a “LangGraph-style” agent graph (compiled).

---

## 1) What lives under `langchain.agents.react.agent`?

### `create_react_agent(...)`
Signature (from reference):

- `llm`: `BaseLanguageModel`
- `tools`: `Sequence[BaseTool]`
- `prompt`: `BasePromptTemplate`
- optional `output_parser`
- `tools_renderer`
- `stop_sequence` (often stops on `"Observation:"` to reduce hallucinated tool outputs)

It returns a **Runnable** that outputs either `AgentAction` or `AgentFinish`. citeturn3view0

#### Important warning (from docs)
The docs explicitly say this ReAct implementation is older and not ideal for production; they recommend a more robust ReAct implementation from LangGraph (and newer agent approaches). citeturn3view0

#### Required prompt keys for ReAct prompting
Your prompt must include:
- `{tools}` (tool descriptions)
- `{tool_names}` (names list)
- `{agent_scratchpad}` (history of Thought/Action/Observation…)

Also typically includes `{input}`. citeturn3view0

---

## 2) The “agent creation helpers” catalog (create_*_agent)

From the v0.3 agents reference navigation, these helpers are commonly used: citeturn2view0

### Core “brain styles”
- `create_react_agent`
- `create_tool_calling_agent`
- `create_structured_chat_agent`
- `create_json_chat_agent`
- `create_openai_tools_agent`
- `create_openai_functions_agent`
- `create_xml_agent`
- `create_self_ask_with_search_agent`

### Convenience builders & routing
- `initialize_agent`
- `create_conversational_retrieval_agent`
- `create_vectorstore_agent`
- `create_vectorstore_router_agent`
- `load_agent`, `load_agent_from_config`

> In practice: you usually pick **one** “brain style” + wrap it in `AgentExecutor`.

---

## 3) AgentExecutor deep dive (the runtime loop manager)

`AgentExecutor` is a **Chain** that runs an agent step-by-step, calling tools as needed. It also implements the **Runnable interface** (so you get `invoke`, `with_retry`, `assign`, `get_graph`, etc.). citeturn4view0

### Key init args you’ll care about
- `agent`: the agent runnable / agent object that decides actions
- `tools`: allowed tools (what the agent can call)
- `max_iterations`: cap on tool-use loops (default 15) citeturn4view0
- `max_execution_time`: wall-clock limit citeturn4view0
- `early_stopping_method`:  
  - `"force"`: stop with a message if limits hit  
  - `"generate"`: do one final LLM pass to produce a final answer citeturn4view0
- `handle_parsing_errors`:  
  - `False` = raise errors  
  - `True` = send parsing error back to LLM as Observation  
  - string/callable = custom observation message citeturn4view0
- `return_intermediate_steps`: include Thought/Action/Observation trace in output citeturn4view0

### How AgentExecutor runs (high level)
1. Start with user inputs
2. Ask agent “what next?”
3. If agent returns `AgentAction(tool, tool_input)` → call tool → feed tool output back
4. Repeat until `AgentFinish(final_answer)` or stop limits reached

---

## 4) Concrete examples (copy/paste friendly)

> Examples show the “classic” pattern because that’s what `create_react_agent` etc. expect.

### 4.1 ReAct agent (classic) + AgentExecutor

```python
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain_openai import ChatOpenAI   # or any LLM wrapper
from langchain_community.tools import DuckDuckGoSearchRun

# 1) Prompt: must match ReAct requirements (tools, tool_names, agent_scratchpad, input)
prompt = hub.pull("hwchase17/react")

# 2) Tools
tools = [DuckDuckGoSearchRun()]

# 3) LLM
llm = ChatOpenAI(model="gpt-4o-mini")

# 4) Create agent runnable
agent = create_react_agent(llm, tools, prompt)

# 5) Wrap in executor (loop manager)
executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

print(executor.invoke({"input": "Find 2 bullet points on the UK GDP definition"}))
```

Why this works:
- ReAct prompt forces the agent to write: Thought → Action → Observation (repeat) → Final Answer.
- The executor is what actually **calls the tools** and feeds observations back into the agent. citeturn3view0turn4view0

### 4.2 `create_tool_calling_agent` (tool-call capable chat models)
This style is usually nicer with modern chat models that support structured tool calling.

```python
from langchain.agents import AgentExecutor
from langchain.agents.tool_calling_agent.base import create_tool_calling_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.tools import DuckDuckGoSearchRun

llm = ChatOpenAI(model="gpt-4o-mini")
tools = [DuckDuckGoSearchRun()]

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Use tools when needed."),
    ("human", "{input}")
])

agent = create_tool_calling_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

executor.invoke({"input": "Search the web for LangChain and summarize in 3 bullets."})
```

(Exact prompt requirements differ vs ReAct; this family leans on tool-call schemas.) citeturn3view1turn4view0

### 4.3 VectorStore agent convenience
If you already have a vector store and want an agent that can query it via tools, you can use the vectorstore agent helper. citeturn3view6

```python
from langchain.agents.agent_toolkits.vectorstore.base import create_vectorstore_agent
from langchain_openai import ChatOpenAI

# vectorstore = ... (FAISS / Chroma / Pinecone / etc.)
llm = ChatOpenAI(model="gpt-4o-mini")

agent_executor = create_vectorstore_agent(
    llm=llm,
    vectorstore=vectorstore,
    verbose=True,
)

agent_executor.invoke({"input": "What does the policy say about refunds?"})
```

---

## 5) When to choose which “create_*_agent” helper (quick interview logic)

### ReAct (`create_react_agent`)
Use when:
- You want the most “classic” agent explanation (Thought/Action/Observation loop).
- You’re demoing reasoning traces clearly.

Avoid when:
- You need robust production behavior with tool calling, structured outputs, etc. (the docs warn it’s older). citeturn3view0

### Tool-calling agents (`create_tool_calling_agent`, `create_openai_tools_agent`)
Use when:
- Your model supports tool calling (function calling / tool schema).
- You want fewer brittle parsing issues and more structured tool invocations. citeturn3view1turn3view2

### Structured/JSON/XML agents
Use when:
- Downstream systems need machine-readable outputs or constrained formats. citeturn3view3turn2view0

### Vectorstore / conversational retrieval helpers
Use when:
- You’re building RAG-ish agent experiences and want “batteries included” scaffolding. citeturn3view4turn3view6

---

## 6) “Where did `create_react_agent` go?” (common confusion)
You may see deprecation messages or docs showing that some helper functions moved or recommended alternatives exist (graph-based agents). Newer reference docs emphasize **`langchain.agents.create_agent`** as the entrypoint for a graph-based agent loop. citeturn1view0turn0search0

If you’re learning for interviews:
- Know the classic ReAct + AgentExecutor story (easy to explain)
- Also mention that newer stacks often move to graph-based orchestration (LangGraph) for reliability, memory, interrupts, and multi-agent flows. citeturn1view0turn0search0

---

## 7) Quick glossary (objects you’ll see in code)
- **Tool (`BaseTool`)**: callable capability (search, DB query, Python REPL, etc.)
- **Agent**: policy that selects the next tool call or returns a final answer
- **AgentExecutor**: runtime loop that executes agent steps and tools
- **Runnable**: composable unit with `invoke/ainvoke/stream` etc.
- **Prompt**: instructions + slots (input variables)
- **Scratchpad**: the agent’s running log of intermediate steps (ReAct style) citeturn3view0turn4view0

---

## 8) Suggested learning path (fast)
1. Build a ReAct agent with 1–2 tools and watch the Thought/Action/Observation loop.
2. Turn on `return_intermediate_steps=True` and learn what the executor returns.
3. Swap to `create_tool_calling_agent` to see how structured tool calling differs.
4. Explore the graph-based `create_agent` and compare how “state + middleware + interrupts” feel vs classic executors. citeturn1view0turn4view0
