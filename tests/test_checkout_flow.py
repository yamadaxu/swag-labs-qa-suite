"""结算闭环用例：数据驱动的下单路径 + 金额一致性校验（测试分析点）。"""
import pytest

from pages import CartPage, CheckoutPage, InventoryPage, LoginPage
from tests.conftest import read_csv

CHECKOUT_CASES = read_csv("checkout_data.csv")


def test_full_checkout_happy_path(sb):
    LoginPage(sb).open().login("standard_user", "secret_sauce")
    inv = InventoryPage(sb)
    inv.add_to_cart("backpack").add_to_cart("onesie")
    inv.open_cart()

    cart = CartPage(sb)
    assert cart.has_item_named("Sauce Labs Backpack")
    assert cart.has_item_named("Sauce Labs Onesie")
    cart.checkout()

    checkout = CheckoutPage(sb)
    checkout.fill_shipping("Mei", "Wang", "200000")
    assert checkout.is_on_step_two(), "填写有效收货信息应进入确认页"
    checkout.finish()
    assert check_out_header(checkout) == "Thank you for your order!", "下单成功应展示致谢文案"


def _to_float(s):
    return float(s.strip("$"))


def check_out_header(checkout):
    return checkout.order_header().strip()


@pytest.mark.parametrize("row", CHECKOUT_CASES, ids=lambda r: f"{r['first_name'] or 'E'}-{r['last_name'] or 'E'}-{r['postal_code'] or 'E'}")
def test_checkout_form_validation(sb, row):
    LoginPage(sb).open().login("standard_user", "secret_sauce")
    inv = InventoryPage(sb)
    inv.add_to_cart("backpack").open_cart()
    CartPage(sb).checkout()

    checkout = CheckoutPage(sb)
    checkout.fill_shipping(row["first_name"], row["last_name"], row["postal_code"])

    if row["expect_success"] == "yes":
        assert checkout.is_on_step_two(), "完整收货信息应进入确认页"
    else:
        assert "required" in checkout.error_text().lower(), "缺失必填字段应提示 required"


def test_order_total_math_consistency(sb):
    """测试分析：确认页 Item total 必须等于商品价格之和（防止后台单价改价不同步）。"""
    LoginPage(sb).open().login("standard_user", "secret_sauce")
    inv = InventoryPage(sb)
    inv.add_to_cart("backpack").add_to_cart("bike-light").add_to_cart("fleece-jacket")
    inv.open_cart()

    cart = CartPage(sb)
    cart.checkout()

    checkout = CheckoutPage(sb)
    checkout.fill_shipping("Mei", "Wang", "200000")
    assert checkout.is_on_step_two()

    item_prices = checkout.cart_item_prices()
    expected = round(sum(item_prices), 2)
    assert checkout.item_total() == expected, (
        f"Item total 应与购物车商品金额一致: 期望 {expected}, 实际 {checkout.item_total()}"
    )
    assert abs((checkout.item_total() + checkout.tax()) - checkout.total()) < 0.01, "Subtotal + Tax 应等于 Total"