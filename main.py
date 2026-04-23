# from agent.simple_agent import agent
# from agent.search_agent import agent
from agent.wikipedia_agent import agent


def main():
    question = "Who is the Kishor Kumar?"
    print(f"User: {question}")
    result = agent.run_sync(question)
    print("Agent: ", result.output)


if __name__ == "__main__":
    main()
