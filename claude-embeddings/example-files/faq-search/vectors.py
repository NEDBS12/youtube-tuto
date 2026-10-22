import math


def length(v):
    """The vector's length (L2 norm): sqrt of the sum of squares."""
    return math.sqrt(sum(x * x for x in v))


def normalize(v):
    """Scale the vector to length 1. Its direction doesn't change."""
    n = length(v)
    return [x / n for x in v]


def dot(a, b):
    """Dot product: multiply number by number, then add it all up."""
    return sum(x * y for x, y in zip(a, b))


def cosine(a, b):
    """Cosine similarity: 1 = same direction, 0 = unrelated."""
    return dot(a, b) / (length(a) * length(b))
