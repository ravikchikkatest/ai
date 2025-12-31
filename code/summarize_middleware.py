from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware
from langchain.chat_models import init_chat_model
from langchain.chat_models.base import BaseChatModel
from dotenv import load_dotenv
import os
from pydantic import PrivateAttr


class DebugChatModel(BaseChatModel):
    _model: BaseChatModel = PrivateAttr()

    def __init__(self, model):
        super().__init__()
        self._model = model

    @property
    def _llm_type(self) -> str:
        return "debug-wrapper"

    def _generate(self, messages, **kwargs):
        print("\n====== FINAL PROMPT SENT TO MODEL ======")
        for i, m in enumerate(messages):
            print(f"\n[{i}] {m.type.upper()}:\n{m.content[:300]}")
        print("======================================\n")

        return self._model._generate(messages, **kwargs)


# --------------------------------------------------
# Inspectable Summarization Middleware
# --------------------------------------------------
class InspectableSummarizationMiddleware(SummarizationMiddleware):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.latest_summary = None

    def _summarize(self, messages):
        summary_message = super()._summarize(messages)
        self.latest_summary = summary_message.content
        return summary_message



# ---------------------
# Initialize model
# ---------------------
# Load environment variables

load_dotenv('C:/Agentic/codellm/.env')


# Configure Google AI API 
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    print("Please set your OPENAI_API_KEY in a .env file")


base_llm = init_chat_model("gpt-4.1-nano")
llm = DebugChatModel(base_llm)

conversation = []

def extract_summary(messages):
    for m in messages:
        if (
            m.type == "human"
            and "Here is a summary of the conversation" in m.content
        ):
            return m.content
    return None

# ---------------------
# Force summarization
# ---------------------
middleware = InspectableSummarizationMiddleware(
    model=llm,
    max_tokens_before_summary=200,   # very low to trigger fast
    messages_to_keep=2               # keep only last 2 verbatim
)
latest_summary = None  # optional global or external store

def send(user_text):
    global latest_summary

    conversation.append({"role": "user", "content": user_text})

    result = agent.invoke({"messages": conversation})

    # 🔍 Extract summary if one was generated
    summary = extract_summary(result["messages"])
    if summary:
        latest_summary = summary
        print("\n=== EXTRACTED SUMMARY ===")
        print(summary)
        print("========================\n")

    # append AI reply back into conversation
    ai_message = result["messages"][-1]
    conversation.append({
        "role": "assistant",
        "content": ai_message.content
    })

    return ai_message.content


# ---------------------
# Create agent
# ---------------------
agent = create_agent(
    model=llm,
    tools=[],
    middleware=[middleware]
)


# ---------------------
# 1. Store a long-term fact
# ---------------------
send("Remember this forever: my favorite programming language is Rust.")

for i in range(6):
    send("Filler text " * 30)

print("SUMMARY:", middleware.latest_summary)

send("What is my favorite programming language?")


# ---------------------
# 3. Inspect saved summary
# ---------------------
print("\n====== STORED SUMMARY (PROGRAMMATIC ACCESS) ======")
print(middleware.latest_summary)
print("=================================================\n")


# ---------------------
# 4. Recall test
# ---------------------
answer = send("What is my favorite programming language?")
print("\nAGENT RESPONSE:")
print(answer)