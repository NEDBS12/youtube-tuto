import os

API_KEY = os.environ["API_KEY"]


def greet(name):
    return f"Hello, {name}!"


print(greet("world"))
