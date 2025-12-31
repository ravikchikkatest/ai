from langchain.chat_models import init_chat_model
from langchain_core.messages import ToolMessage
from langchain.tools import tool
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os
from pydantic import BaseModel, Field
from langchain.agents import create_agent


# Load environment variables
load_dotenv()

# Configure Google AI API 
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class ContactInfo(BaseModel):
    """Contact information for a person."""
    name: str = Field(description="The name of the person")
    email: str = Field(description="The email address of the person")
    phone: str = Field(description="The phone number of the person")


agent = create_agent(
    model="gpt-4.1-nano",     
    response_format=ContactInfo,
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "Extract contact info from: John Doe, john@example.com, (555) 123-4567"}]
})

print(result["structured_response"])
