from datetime import datetime

from pydantic_ai import Agent
from pydantic_ai.models.ollama import OllamaModel
from pydantic_ai.providers.ollama import OllamaProvider
from pydantic_ai.capabilities import WebSearch, Thinking


import os
from dotenv import load_dotenv

load_dotenv()
model = os.getenv("MODEL_NAME")
base_url = os.getenv("OLLAMA_BASE_URL")

print(f"model {model} and base url : {base_url}")


model = OllamaModel(
    model_name="gemma4", provider=OllamaProvider(base_url="http://localhost:11434/v1")
)

agent = Agent(
    model,
    description="You are subject matter expert in all the areas and working as professional teacher in the universities.",
    capabilities=[Thinking(), WebSearch()],
)


# custom tool to work with date time
@agent.tool_plain
def current_datetime() -> datetime:
    """This tool return user current date time"""
    return datetime.now()
