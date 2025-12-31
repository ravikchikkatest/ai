from langchain.chat_models import init_chat_model
from langchain_core.messages import ToolMessage
from langchain.tools import tool
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os
import streamlit as st

# -------------------------
# 1. Tool schemas
# -------------------------

class GetWeather(BaseModel):
    """Get the current weather in a given location"""
    location: str = Field(..., description="City and state, e.g. Los Angeles, CA")


class GetPopulation(BaseModel):
    """Get the population of a given location"""
    location: str = Field(..., description="City and state, e.g. New York, NY")


# -------------------------
# 2. Tool implementations
# -------------------------

@tool(args_schema=GetWeather)
def get_weather(location: str) -> str:
    """Returns the current temperature for a city."""
    mock_weather = {
        "Los Angeles, CA": "28°C",
        "New York, NY": "22°C",
    }
    return mock_weather.get(location, "Weather data unavailable")


@tool(args_schema=GetPopulation)
def get_population(location: str) -> str:
    """Returns the population for a city."""
    mock_population = {
        "Los Angeles, CA": "3.9 million",
        "New York, NY": "8.4 million",
    }
    return mock_population.get(location, "Population data unavailable")


# -------------------------
# 3. Create configurable model
# -------------------------

# Load environment variables
load_dotenv()

# Configure Google AI API 
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    st.error("Please set your OPENAI_API_KEY in a .env file")
    st.stop()

model = init_chat_model(
    model="gpt-4.1-nano",
    model_provider="openai",
    openai_api_key=OPENAI_API_KEY,
    temperature=0,
)

# Bind tools
model_with_tools = model.bind_tools(
    [get_weather, get_population]
)

# -------------------------
# 4. Invoke with default model (GPT-4o)
# -------------------------

response = model_with_tools.invoke(
    "Which city is hotter today and which is bigger: LA or NY?"
)

print("gpt-4.1-nano response:")
print(response.content)

ai_msg = response  # your first response

tool_messages = []

for call in ai_msg.tool_calls:
    tool_name = call["name"]
    args = call["args"]

    if tool_name == "get_weather":
        result = get_weather.invoke(args)
    elif tool_name == "get_population":
        result = get_population.invoke(args)
    else:
        continue

    tool_messages.append(
        ToolMessage(
            content=result,
            tool_call_id=call["id"]
        )
    )

final_response = model_with_tools.invoke(
    [
        ai_msg,
        *tool_messages
    ]
)

print("\n✅ Final answer:")
print(final_response.content)

# python -m pip install -r requirements.txt
# python -m binding_tools


# | Call                      | Who runs it | Purpose       |
# | ------------------------- | ----------- | ------------- |
# | `model.invoke()` #1       | LLM         | Tool planning |
# | `get_weather.invoke()`    | Python      | Fetch data    |
# | `get_population.invoke()` | Python      | Fetch data    |
# | `model.invoke()` #2       | LLM         | Final answer  |
