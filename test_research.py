from agents.research_agent import research_node

state = {
    "query": "Applications of AI in Healthcare",
    "planner": {
        "keywords": [
            "Applications of AI in Healthcare",
            "Medical AI",
            "Clinical Decision Support"
        ],
        "max_sources": 5,
    }
}

state = research_node(state)

print("\nCollected Sources:\n")

for source in state["research"]["sources"]:
    print(source)