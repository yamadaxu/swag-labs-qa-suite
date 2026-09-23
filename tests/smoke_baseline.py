"""WPS-era QA smoke baseline: verify the whole toolchain works against the
demo e-commerce store (Swag Labs) in headless mode.

Run:
    pytest tests/smoke_baseline.py --headless -v

This is the "can we even launch a browser and hit the app" gate before the
full POM suite lands.
"""
from seleniumbase import BaseCase


class SmokeBaseline(BaseCase):
    def test_smoke_login_and_land_on_inventory(self):
        self.open("https://www.saucedemo.com")
        self.assert_element("#user-name")
        self.type("#user-name", "standard_user")
        self.type("#password", "secret_sauce")
        self.click('input[type="submit"]')
        self.assert_element("div.inventory_list")
        self.assert_exact_text("Products", "span.title")