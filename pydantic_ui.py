# from agent.simple_agent import agent
# from agent.search_agent import agent
# app is important to import without that get ERROR: Error loading ASGI app. Attribute "app" not found in module "main"
from agent.wikipedia_agent import agent, app

def main():
    question = "Who is the Kishor Kumar? provide its wikipedia link"
    print(f"User: {question}")
    result = agent.run_sync(question)
    print("Agent: ", result.output)


if __name__ == "__main__":
    main()

# to run will use pydantic ui
# import agent.to_web()
# uvicorn pydantic_ui:app --host 127.0.0.1 --port 7932