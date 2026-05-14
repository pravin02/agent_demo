import os
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv

load_dotenv()
model_name = os.getenv("MODEL_NAME") or ""
base_url = os.getenv("MODEL_BASE_URL")


class BaseAgent:
    """Base Agent"""

    def __init__(self):
        self.llm = ChatOllama(base_url=base_url, model=model_name, temperature=0.7)

    def invoke(self, system_prompt: str, user_prompt: str):
        """Invoke  the LLM with user and system prompt"""
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]

        response = self.llm.invoke(messages)
        return response.content


