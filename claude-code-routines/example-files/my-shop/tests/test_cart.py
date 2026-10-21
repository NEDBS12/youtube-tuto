import pytest

from cart import discount, shipping, subtotal


def item(price, qty=1):
    return {"price": price, "qty": qty}


def test_subtotal():
    assert subtotal([item(10, 3), item(2.5, 2)]) == pytest.approx(35)


@pytest.mark.parametrize("total, expected", [(99.99, 99.99), (100, 90), (200, 180)])
def test_discount(total, expected):
    assert discount(total) == pytest.approx(expected)


@pytest.mark.parametrize("total, expected", [(0, 4.99), (49.99, 4.99), (50, 0), (75, 0)])
def test_shipping(total, expected):
    assert shipping(total) == pytest.approx(expected)
