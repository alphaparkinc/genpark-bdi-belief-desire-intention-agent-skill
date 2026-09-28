from client import BDIAgent

def main():
    agent = BDIAgent()
    agent.update_beliefs({"battery_level": 12})
    plan = agent.filter_intentions()
    print("BDI Agent Deliberation Verification:")
    print(f"Generated Desires: {agent.desires}")
    print(f"Committed Intentions: {plan}")
    print(f"Next Action Step: {agent.step()}")

if __name__ == "__main__":
    main()
