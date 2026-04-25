from fastapi import FastAPI
from agent.wikipedia_agent import agent


app = FastAPI()


@app.get("/")
def home() -> str:
    return "home"


@app.get("/agent")
def agent_run_sync(query: str = "what is PI") -> str:
    return agent.run_sync(query).output
