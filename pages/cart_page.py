"""
Page Object for the cart interactions.

Covers:
- Adding products to cart from the products listing
- The 'added to cart' modal
- Viewing the cart contents
- Removing products
- Cart empty state
"""

from playwright.sync_api import Page, expect


class CartPage:
    """The cart and cart-related interactions on Automation Exercise."""

    CART_URL = "https://automationexercise.com/view_cart"

    def __init__(self, page: Page):
        self.page = page

        # 'Add to cart' buttons on the products page - many of them
        # We use nth() to pick a specific product
        self.add_to_cart_buttons = page.get_by_text("Add to cart")

        # Modal that appears after clicking 'Add to cart'
        self.modal_continue_shopping = page.get_by_role("button", name="Continue Shopping")
        self.modal_view_cart = page.get_by_role("link", name="View Cart")
        self.modal_added_message = page.get_by_text("Your product has been added to cart.")

        # Cart page
        self.cart_rows = page.locator("tr[id^='product-']")  # each product is a table row
        self.delete_buttons = page.locator(".cart_quantity_delete")
        self.empty_cart_message = page.get_by_text("Cart is empty! Click here to")
        self.proceed_to_checkout = page.get_by_role("link", name="Proceed To Checkout")

    def navigate(self):
        """Navigate directly to the cart page."""
        self.page.goto(self.CART_URL)

    def add_product_to_cart(self, index: int = 0):
        """Click 'Add to cart' on the product at the given index (0-based).
           Uses dispatch_event because Automation Exercise has a sticky 
           'All Products' heading that intercepts mouse clicks on buttons
           scrolled into the top area of the viewport."""
        button = self.add_to_cart_buttons.nth(index)
        button.scroll_into_view_if_needed()
        button.dispatch_event("click")
        expect(self.modal_added_message).to_be_visible()

    def click_continue_shopping(self):
        """Close the 'added to cart' modal and stay on the products page."""
        self.modal_continue_shopping.click()

    def go_to_cart_from_modal(self):
        """Click 'View Cart' from the confirmation modal."""
        self.modal_view_cart.click()

    def remove_product_at(self, index: int = 0):
        """Remove the product at the given cart row index."""
        self.delete_buttons.nth(index).click()

    def get_cart_item_count(self) -> int:
        """Return the number of products currently in the cart."""
        return self.cart_rows.count()

    def expect_cart_empty(self):
        """Assert the empty cart message is visible."""
        expect(self.empty_cart_message).to_be_visible()

    def expect_product_in_cart(self):
        """Assert at least one product is in the cart."""
        expect(self.cart_rows.first).to_be_visible()