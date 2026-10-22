import sys
import voyageai
from vectors import length, dot

vo = voyageai.Client()  # reads your VOYAGE_API_KEY
FAQ = [
    "Where is my order?",
    "How do I return a mug?",
    "Is shipping free?",
    "Are your mugs dishwasher safe?",
    "Can I change my delivery address?",
]

# 1. Embed the FAQ once: one vector per question
docs = vo.embed(FAQ, model="voyage-4-lite",
                input_type="document").embeddings
print(f"{len(docs)} vectors, {len(docs[0])} numbers each, "
      f"length {length(docs[0]):.3f}")

# 2. Embed the customer's question
question = sys.argv[1]
q = vo.embed([question], model="voyage-4-lite",
             input_type="query").embeddings[0]

# 3. Length 1 already, so the dot product IS the cosine
ranked = sorted(zip((dot(q, d) for d in docs), FAQ), reverse=True)
for score, text in ranked[:3]:
    print(f"{score:.3f}  {text}")
