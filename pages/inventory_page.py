"""商品列表页 Page Object。覆盖列表、加购、排序、商品详情。"""


class InventoryPage:
    def __init__(self, sb):
        self.sb = sb

    def is_loaded(self):
        return self.sb.is_element_present("div.inventory_list")

    def item_count(self):
        return len(self.sb.find_elements("div.inventory_item"))

    def add_to_cart(self, item_id):
        self.sb.click(f'button[name*="{item_id}"]')
        return self

    def cart_badge(self):
        return self.sb.get_text("#shopping_cart_container .shopping_cart_badge")

    def has_cart_badge(self):
        return self.sb.is_element_present("#shopping_cart_container .shopping_cart_badge")

    def open_cart(self):
        self.sb.click("#shopping_cart_container a")
        return self

    def go_home(self):
        self.sb.click("#inventory_sidebar_link")
        self.sb.click("#react-burger-menu-btn")
        return self

    def sort_by(self, value):
        self.sb.select_option_by_value("select.product_sort_container", value)
        return self

    def product_names(self):
        names = []
        for el in self.sb.find_elements("div.inventory_item_name"):
            names.append(el.text)
        return names

    def product_prices(self):
        prices = []
        for el in self.sb.find_elements("div.inventory_item_price"):
            prices.append(el.text)
        return prices

    def product_image_srcs(self):
        srcs = []
        for el in self.sb.find_elements("div.inventory_item_img img"):
            srcs.append(el.get_attribute("src"))
        return srcs