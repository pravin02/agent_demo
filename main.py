from teacher_agent import agent


def main():
    print("Hello from agent-demo!")
    result = agent.run_sync("What is current Time?")
    print("Agent: ", result.output)



if __name__ == "__main__":
    main()
