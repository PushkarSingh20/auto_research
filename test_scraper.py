from agents.scraper_agent import scraper_node

state = {
    "research": {
        "sources": [
            {
                "title": "Artificial Intelligence",
                "url": "https://en.wikipedia.org/wiki/Artificial_intelligence",
                "snippet": "Artificial Intelligence",
            }
        ]
    }
}

state = scraper_node(state)

print()

print("=" * 80)

print("DOCUMENTS")

print("=" * 80)

for doc in state["documents"]:

    print("\nTITLE:")
    print(doc["title"])

    print("\nURL:")
    print(doc["url"])

    print("\nCONTENT PREVIEW:\n")

    print(doc["content"][:1000])

    print("\n" + "-" * 80)