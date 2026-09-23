"""结算页 Page Object。覆盖信息填写、校验、汇总金额一致性。"""

PRICE_REGEX = r"^\$\d+\.\d{2}$"


class CheckoutPage:
    def __init__(self, sb):
        self.sb = sb

    def is_on_step_one(self):
        return self.sb.is_element_present("div.checkout_info")

    def fill_shipping(self, first_name, last_name, postal_code):
        self.sb.type("#first-name", first_name)
        self.sb.type("#last-name", last_name)
        self.sb.type("#postal-code", postal_code)
        self.sb.click("input#continue")
        return self

    def is_on_step_two(self):
        return self.sb.is_element_present("#checkout_summary_container")

    def error_text(self):
        if self.sb.is_element_present("div.error-message-container.error"):
            return self.sb.get_text("div.error-message-container.error")
        return ""

    def item_total(self):
        text = self.sb.get_text("div.summary_subtotal_label")
        return self._to_float(text)

    def tax(self):
        text = self.sb.get_text("div.summary_tax_label")
        return self._to_float(text)

    def total(self):
        text = self.sb.get_text("div.summary_total_label")
        return self._to_float(text)

    def cart_item_prices(self):
        prices = []
        for el in self.sb.find_elements("div.inventory_item_price"):
            prices.append(self._to_float(el.text))
        return prices

    def finish(self):
        self.sb.click("button#finish")
        return self

    def order_header(self):
        if self.sb.is_element_present("h2"):
            return self.sb.get_text("h2")
        return ""

    @staticmethod
    def _to_float(text):
        cleaned = text.replace("Item total:", "").replace("Tax:", "").replace("Total:", "").strip().replace("$", "")
        try:
            return round(float(cleaned), 2)
        except ValueError:
            return 0.0