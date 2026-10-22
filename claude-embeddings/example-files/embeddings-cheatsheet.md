# Embeddings and normalization: cheat sheet

## The words

- **Embedding:** a vector (a list of numbers) that captures what a text means. Similar meaning → vectors that point in a similar direction.
- **Length (L2 norm):** `sqrt(x1² + x2² + ... + xn²)`. How long the arrow is.
- **Normalize:** divide every number by the length. Same direction, length 1.
- **Dot product:** `x1*y1 + x2*y2 + ...`
- **Cosine similarity:** `dot(a, b) / (length(a) * length(b))`. Compares direction only: 1 = same direction, 0 = unrelated.
- **The payoff:** if both vectors have length 1, `dot(a, b) == cosine(a, b)`. Comparing becomes a plain, fast dot product.

## Two kinds of normalization

- **Normalizing embeddings** (this video): scale each vector to length 1 before comparing vectors. Voyage AI vectors already come normalized.
- **Normalization layers inside LLMs** (LayerNorm, RMSNorm): rescale the numbers between the network's layers to keep training stable. They're part of the model; you don't call them.

## Embeddings for Claude apps

Anthropic doesn't offer an embedding model; its docs point to Voyage AI.

```python
import voyageai

vo = voyageai.Client()  # reads VOYAGE_API_KEY
docs = vo.embed(texts, model="voyage-4-lite", input_type="document").embeddings
q = vo.embed([question], model="voyage-4-lite", input_type="query").embeddings[0]
```

- Voyage embeddings are normalized to length 1, so dot product = cosine similarity.
- Use `input_type="document"` for what you store and `input_type="query"` for what you search with. The docs say not to leave it out.
- Use the same model for documents and queries: vectors from different models can't be compared.
- voyage-4 models return 1,024 numbers by default (256, 512 and 2048 are also available with `output_dimension`).
- **Shortened stored vectors?** Keep the first numbers, then **normalize again**: the shorter vector's length is below 1.

## When to use embeddings

- **Yes:** search by meaning, retrieval for RAG, duplicates, recommendations, grouping similar texts.
- **Keyword search is better for:** exact codes, IDs and rare names. Many systems combine both.

## Links

- Embeddings (Claude docs): https://platform.claude.com/docs/en/build-with-claude/embeddings
- Voyage AI models: https://www.mongodb.com/docs/voyageai/models/
