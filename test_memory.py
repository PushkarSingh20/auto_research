from memory.chroma import memory

documents = [
    {
        "title": "Artificial Intelligence",
        "url": "https://example.com",
        "content": "Artificial Intelligence is transforming healthcare.",
        "source_type": "web",
    }
]

memory.store_documents(
    query="AI Healthcare",
    documents=documents,
)

results = memory.retrieve_documents(
    "Healthcare AI",
)

print(results)

print()

print("Total Documents:", memory.count())