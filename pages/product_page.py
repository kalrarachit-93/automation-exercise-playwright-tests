"""
Page Object for the product detail page.

URL pattern: /product_details/<id>
Shows a single product's name, price, description, availability, category.
"""

from playwright.sync_api import Page, expect


class ProductPage:
    """A single product's detail page."""

    def __init__(self, page: Page):
        self.page = page

        # Main product information
        self.product_name = page.locator(".product-information > h2")
        self.product_price = page.locator(".product-information > span > span")
        self.availability = page.get_by_text("Availability:")
        self.condition = page.get_by_text("Condition:")
        self.brand = page.get_by_text("Brand:")

        # Actions
        self.quantity_input = page.locator("#quantity")
        self.add_to_cart_button = page.get_by_role("button", name=" Add to cart")

    def expect_loaded(self):
        """Assert the product detail page has loaded with a product name."""
        expect(self.product_name).to_be_visible()

    def expect_shows_availability(self):
        """Assert the availability field is displayed."""
        expect(self.availability).to_be_visible()

    def expect_shows_price(self):
        """Assert a price is displayed."""
        expect(self.product_price).to_be_visible()

    def get_product_name(self) -> str:
        """Return the current product's name as text."""
        return self.product_name.inner_text()