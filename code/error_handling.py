from pydantic import BaseModel, Field
from typing import List, Union
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure Google AI API 
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")



class ContactInfo(BaseModel):
    name: str = Field(description="Person's name")
    email: str = Field(description="Email address")

class EventDetails(BaseModel):
    event_name: str = Field(description="Name of the event")
    date: str = Field(description="Event date")

class ExtractionResult(BaseModel):
    items: List[Union[ContactInfo, EventDetails]]


agent = create_agent(
    model="gpt-4.1-nano",     
    tools=[],
    response_format=ToolStrategy(ExtractionResult)
)


respone = agent.invoke({
    "messages": [{"role": "user", "content": "Extract info: John Doe (john@email.com) is organizing Tech Conference on March 15th"}]
})

print(respone["structured_response"])
