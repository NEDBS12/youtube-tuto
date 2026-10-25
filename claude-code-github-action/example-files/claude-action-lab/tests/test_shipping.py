from shipping import shipping_cost


def test_small_order_pays_shipping():
    assert shipping_cost(20) == 4.99


def test_big_order_ships_free():
    assert shipping_cost(80) == 0


def test_exactly_50_ships_free():
    assert shipping_cost(50) == 0
