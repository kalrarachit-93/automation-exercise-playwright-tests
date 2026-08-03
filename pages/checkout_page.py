"""
Page Object for the checkout flow.

Covers three related pages:
- The checkout review page (/checkout) - address confirmation + order review
- The payment page (/payment) - card details form
- The order confirmation page - 'Order Placed!' success

Also handles the 'Register / Login' modal that appears when a guest
user attempts to checkout.
"""

from playwright.sync_api import Page, expect


class CheckoutPage:
    """The checkout, payment, and order confirmation pages."""

    CHECKOUT_URL = "https://automationexercise.com/checkout"
    PAYMENT_URL = "https://automationexercise.com/payment"

    def __init__(self, page: Page):
        self.page = page

        # Guest checkout modal (appears when guest clicks 'Proceed To Checkout')
        self.register_login_link = page.get_by_role("link", name="Register / Login")

        # Checkout review page (/checkout)
        self.comment_textarea = page.locator('textarea[name="message"]')
        self.place_order_link = page.get_by_role("link", name="Place Order")

        # Payment page (/payment)
        self.name_on_card = page.locator('input[name="name_on_card"]')
        self.card_number = page.locator('input[name="card_number"]')
        self.cvc = page.get_by_role("textbox", name="ex.")
        self.expiration_month = page.get_by_role("textbox", name="MM")
        self.expiration_year = page.get_by_role("textbox", name="YYYY")
        self.pay_and_confirm_button = page.get_by_role("button", name="Pay and Confirm Order")

        # Success confirmation
        self.order_placed_message = page.get_by_text("Order Placed!")

    def add_comment(self, message: str):
        """Fill the delivery comment box on the checkout review page."""
        self.comment_textarea.fill(message)

    def click_place_order(self):
        """Click 'Place Order' to advance from checkout review to payment."""
        self.place_order_link.click()

    def fill_payment_details(
        self,
        name_on_card: str = "Test User",
        card_number: str = "4111111111111111",
        cvc: str = "123",
        expiration_month: str = "12",
        expiration_year: str = "2030",
    ):
        """
        Fill all payment form fields. Defaults are safe test values.
        4111111111111111 is a standard test card number that many payment
        systems recognize as 'test data'.
        """
        self.name_on_card.fill(name_on_card)
        self.card_number.fill(card_number)
        self.cvc.fill(cvc)
        self.expiration_month.fill(expiration_month)
        self.expiration_year.fill(expiration_year)

    def submit_payment(self):
        """Click 'Pay and Confirm Order' to complete the order."""
        self.pay_and_confirm_button.click()

    def expect_guest_checkout_modal(self):
        """Assert the 'Register / Login' link is visible (appears in the guest modal)."""
        expect(self.register_login_link).to_be_visible()

    def expect_order_placed(self):
        """Assert the 'Order Placed!' success message is visible."""
        expect(self.order_placed_message).to_be_visible()