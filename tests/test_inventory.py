"""商品列表页用例：数量、加购、排序。"""
from pages import InventoryPage, LoginPage


def _login_standard(sb):
    LoginPage(sb).open().login("standard_user", "secret_sauce")
    return InventoryPage(sb)


def test_inventory_has_six_products(sb):
    inv = _login_standard(sb)
    assert inv.is_loaded()
    assert inv.item_count() == 6, "演示商城应展示 6 个商品"


def test_add_to_cart_updates_badge(sb):
    inv = _login_standard(sb)
    inv.add_to_cart("backpack")
    assert inv.cart_badge() == "1", "加入背包后购物车角标应为 1"
    inv.add_to_cart("bike-light")
    assert inv.cart_badge() == "2", "加入第二个商品后角标应为 2"


def test_sort_name_a_to_z(sb):
    inv = _login_standard(sb)
    inv.sort_by("az")
    names = [n.lower() for n in inv.product_names()]
    assert names == sorted(names), "名称升序排序结果应符合 A-Z"


def test_sort_price_low_to_high(sb):
    inv = _login_standard(sb)
    inv.sort_by("lohi")
    prices = [float(p.strip("$")) for p in inv.product_prices()]
    assert prices == sorted(prices), "价格低到高排序结果应单调递增"