from pydantic_ai import Agent

from pydantic_ai.models.ollama import OllamaModel

from pydantic_ai.providers.ollama import OllamaProvider

from pydantic_ai.capabilities import WebSearch, WebFetch, Thinking

import os
from dotenv import load_dotenv

from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from pydantic_ai.ext.langchain import tool_from_langchain
import wikipedia

load_dotenv()

model_name = os.getenv("MODEL_NAME") or ""
base_url = os.getenv("OLLAMA_BASE_URL")

model = OllamaModel(model_name, provider=OllamaProvider(base_url))

wikipedia_api_wrapper = WikipediaAPIWrapper(
    wiki_client=wikipedia, top_k_results=1, doc_content_chars_max=1000, lang="en"
)
wikipedia = WikipediaQueryRun(api_wrapper=wikipedia_api_wrapper)
wikipedia_tool = tool_from_langchain(wikipedia)

"""This agent has capabality to search over wikipedia and collect the results based on
    question and will be feeded to LLM for final response
 """
agent = Agent(
    model,
    capabilities=[Thinking(), WebSearch(), WebFetch()],
    tools=[wikipedia_tool],
)

app = agent.to_web()
