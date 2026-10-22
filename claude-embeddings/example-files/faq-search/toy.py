from vectors import length, normalize, dot, cosine

query = [1, 1]
docs = {"A": [2, 2], "B": [5, 1]}  # A points the same way as the query

print("doc  length   dot  cosine")
for name, v in docs.items():
    ln, d, c = length(v), dot(query, v), cosine(query, v)
    print(f"{name}     {ln:.2f}  {d:.2f}  {c:.3f}")

print("\nAfter normalizing to length 1:")
q = normalize(query)
for name, v in docs.items():
    u = normalize(v)
    print(f"{name}     length {length(u):.2f}  dot {dot(q, u):.3f}")
