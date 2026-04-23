#from agent.simple_agent import agent
from agent.search_agent import agent


def main():
    result = agent.run_sync("List top 10 news about US-iran war")
    print("Agent: ", result.output)



if __name__ == "__main__":
    main()
