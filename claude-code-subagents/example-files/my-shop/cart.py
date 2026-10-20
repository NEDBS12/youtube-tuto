def subtotal(items):
    """Sum of price x quantity for every item."""
    return sum(item["price"] * item["qty"] for item in items)


def discount(total):
    """10% off orders of 100 or more."""
    if total > 100:
        return total * 0.9
    return total


def shipping(total):
    """Free shipping from 50, otherwise 4.99."""
    return 0 if total >= 50 else 4.99
