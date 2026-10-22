# Embeddings and vector normalization: search by meaning

Files from the Zero Cost AI video **"Embeddings and Vector Normalization Explained Simply (Python)"**.

"The package never showed up" and "Where is my order?" share zero words, but they mean the same thing. This folder does the vector math in plain Python (length, normalize, dot product, cosine similarity), shows why a raw dot product can be fooled by a vector's length, and builds a small FAQ search with Voyage AI embeddings, the provider Anthropic's Claude docs point to.

## Use it in your project

| File | What it does |
|---|---|
| [`faq-search/vectors.py`](example-files/faq-search/vectors.py) | `length`, `normalize`, `dot` and `cosine` in plain Python, no libraries |
| [`faq-search/toy.py`](example-files/faq-search/toy.py) | Two-number vectors: the raw dot product picks the wrong one, cosine (or normalized vectors) picks the right one |
| [`faq-search/search.py`](example-files/faq-search/search.py) | Embeds 5 FAQ questions with `voyage-4-lite` and ranks them for a customer's question with a dot product |
| [`faq-search/test_offline.py`](example-files/faq-search/test_offline.py) | Tests the math for real and simulates Voyage AI: no API key, no cost |
| [`embeddings-cheatsheet.md`](example-files/embeddings-cheatsheet.md) | The words, the formulas, the two kinds of normalization, Voyage AI tips |

1. Try the math, no key needed: in `faq-search/`, run `python toy.py`.
2. Run the tests, no key needed: `pip install pytest`, then `python -m pytest -q` (5 passed).
3. With a Voyage AI key: `pip install -U voyageai`, set `VOYAGE_API_KEY`, then run `python search.py "The package never showed up"`.

- Your scores from `search.py` will differ from the video (the run on screen is a recreation); the top match should be "Where is my order?".
- On Mac or Linux, use `python3` if `python` isn't found.
- Voyage vectors already have length 1, so `search.py` uses a plain dot product. If you shorten stored vectors, normalize them again with `vectors.normalize`.
- To use your own FAQ, edit the `FAQ` list. Embed documents with `input_type="document"` and questions with `input_type="query"`, using the same model for both.

## Files in this folder

- `claude-embeddings.mp4`: the video
- `claude-embeddings.srt`: subtitles
- `script.json`, `make_script.py`: the video script (made with the claude-expert-video skill)
- `example-files/`: the FAQ search and the cheat sheet (no secrets: the test simulates Voyage AI)

## Learn more

- [Embeddings (Claude docs)](https://platform.claude.com/docs/en/build-with-claude/embeddings)
- [Voyage AI models](https://www.mongodb.com/docs/voyageai/models/)
