FREE_SHIPPING_FROM = 50  # orders of 50 or more ship free
STANDARD_RATE = 4.99


def shipping_cost(order_total):
    """Return the shipping cost for an order total."""
    if order_total > FREE_SHIPPING_FROM:
        return 0
    return STANDARD_RATE
