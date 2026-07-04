from tools.search import search_web

results = search_web(
    ["Artificial Intelligence"],
    max_results=3,
)

print(results)