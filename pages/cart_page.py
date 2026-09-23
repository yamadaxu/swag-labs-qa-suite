"""购物车页 Page Object。覆盖购物车条目校验与结算入口。"""


class CartPage:
    def __init__(self, sb):
        self.sb = sb

    def is_loaded(self):
        return self.sb.is_element_present("#cart_contents_container")

    def cart_items(self):
        return self.sb.find_elements("div.cart_item")

    def has_item_named(self, item_name):
        return self.sb.is_element_present(f'div.cart_item:contains("{item_name}")')

    def remove_item(self, item_id):
        self.sb.click(f'button[name*="{item_id}"]')
        return self

    def checkout(self):
        self.sb.click("button#checkout")
        return self