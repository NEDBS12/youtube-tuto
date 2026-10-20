import pytest

from cart import discount, shipping, subtotal


def item(price, qty=1):
    return {"price": price, "qty": qty}


@pytest.mark.parametrize("items, expected", [
    ([], 0),
    ([item(10)], 10),
    ([item(10, 3)], 30),
    ([item(2.5, 4)], 10),
    ([item(10), item(5)], 15),
    ([item(19.99, 2)], 39.98),
    ([item(100)], 100),
    ([item(1, 100)], 100),
    ([item(0, 5)], 0),
    ([item(7.5, 2), item(5, 1)], 20),
])
def test_subtotal(items, expected):
    assert subtotal(items) == pytest.approx(expected)


@pytest.mark.parametrize("total, expected", [
    (0, 0),
    (20, 20),
    (50, 50),
    (99.99, 99.99),
    (100, 90),
    (100.01, 90.009),
    (150, 135),
    (200, 180),
    (500, 450),
    (1000, 900),
])
def test_discount(total, expected):
    assert discount(total) == pytest.approx(expected)


@pytest.mark.parametrize("total, expected", [
    (0, 4.99),
    (10, 4.99),
    (25, 4.99),
    (49.99, 4.99),
    (50, 0),
    (50.01, 0),
    (75, 0),
    (100, 0),
    (250, 0),
    (999, 0),
])
def test_shipping(total, expected):
    assert shipping(total) == pytest.approx(expected)
