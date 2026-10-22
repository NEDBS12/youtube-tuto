"""Tests without an API key: the math is real, Voyage AI is simulated.

Run: python -m pytest -q
"""
import math
import runpy
import sys
import types

import pytest

from vectors import cosine, dot, length, normalize

# ---------- the math ----------

def test_length_and_normalize():
    assert length([3, 4]) == 5
    assert normalize([3, 4]) == [0.6, 0.8]
    assert math.isclose(length(normalize([5, 1, 7, -2])), 1.0)


def test_normalized_dot_equals_cosine():
    a, b = [1, 1], [5, 1]
    assert math.isclose(dot(normalize(a), normalize(b)), cosine(a, b))


def test_raw_dot_prefers_the_longer_vector():
    q = [1, 1]
    assert dot(q, [5, 1]) > dot(q, [2, 2])          # dot product is fooled by length
    assert cosine(q, [2, 2]) > cosine(q, [5, 1])    # cosine is not


def test_toy_output(capsys):
    runpy.run_path("toy.py")
    out = capsys.readouterr().out
    assert "A     2.83  4.00  1.000" in out
    assert "B     length 1.00  dot 0.832" in out


# ---------- search.py with a simulated Voyage AI ----------
# Each text becomes a vector of 5 "meanings", normalized like real Voyage vectors.
TOPICS = [{"order", "package", "arrive", "arrived", "showed", "where", "tracking"},
          {"return", "refund", "send", "back"},
          {"shipping", "free", "cost", "delivery"},
          {"dishwasher", "wash", "clean", "safe"},
          {"address", "change", "move", "moved"}]


class FakeClient:
    def __init__(self, *a, **k):
        self.calls = []

    def embed(self, texts, model, input_type):
        assert input_type in ("document", "query")
        self.calls.append((model, input_type))
        vecs = []
        for t in texts:
            words = set(t.lower().replace("?", "").split())
            v = [len(words & topic) + 0.1 for topic in TOPICS]
            vecs.append(normalize(v))
        return types.SimpleNamespace(embeddings=vecs)


@pytest.fixture
def fake_voyage(monkeypatch):
    monkeypatch.setitem(sys.modules, "voyageai", types.SimpleNamespace(Client=FakeClient))


def test_search_finds_meaning_not_words(fake_voyage, monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["search.py", "The package never showed up"])
    runpy.run_path("search.py")
    lines = capsys.readouterr().out.splitlines()
    assert lines[0].startswith("5 vectors, 5 numbers each, length 1.000")
    assert lines[1].endswith("Where is my order?")   # no shared words with the question
