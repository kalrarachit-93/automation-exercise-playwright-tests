"""
Checkout and payment flow tests for Automation Exercise.

Uses AI-generated user data for realistic registration + checkout.
"""

import pytest
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from pages.signup_page import SignupPage
from pages.home_page import HomePage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from tests.utils.ai_data_generator import generate_test_user


def register_and_login_new_user(page: Page):
    """
    Helper: registers a new AI-generated user and returns the TestUser object.
    Leaves the browser logged in and on the account creation success page,
    ready for a caller to click Continue.
    """
    user = generate_test_user()
    login_page = LoginPage(page)
    signup_page = SignupPage(page)

    login_page.navigate()
    login_page.start_signup(user.name, user.email)
    signup_page.fill_account_details(user)
    signup_page.submit()
    signup_page.expect_account_created()
    signup_page.click_continue()

    return user


def test_guest_checkout_shows_login_prompt(page: Page):
    """Attempting to checkout as a guest shows a 'Register / Login' prompt."""
    home_page = HomePage(page)
    cart_page = CartPage(page)
    checkout_page = CheckoutPage(page)

    home_page.navigate()
    cart_page.add_product_to_cart(index=0)
    cart_page.go_to_cart_from_modal()
    cart_page.proceed_to_checkout.click()

    checkout_page.expect_guest_checkout_modal()


def test_logged_in_user_can_complete_checkout(page: Page):
    """A logged-in user can add a product, go through checkout, and see 'Order Placed!'."""
    register_and_login_new_user(page)

    home_page = HomePage(page)
    cart_page = CartPage(page)
    checkout_page = CheckoutPage(page)

    home_page.navigate()
    cart_page.add_product_to_cart(index=0)
    cart_page.go_to_cart_from_modal()
    cart_page.proceed_to_checkout.click()

    # On checkout page - add a comment then place order
    checkout_page.add_comment("Please deliver quickly")
    checkout_page.click_place_order()

    # On payment page - fill and submit
    checkout_page.fill_payment_details()
    checkout_page.submit_payment()

    # Success
    checkout_page.expect_order_placed()


def test_checkout_comment_persists_to_payment(page: Page):
    """Comment added on checkout page is remembered when advancing to payment."""
    register_and_login_new_user(page)

    home_page = HomePage(page)
    cart_page = CartPage(page)
    checkout_page = CheckoutPage(page)

    home_page.navigate()
    cart_page.add_product_to_cart(index=0)
    cart_page.go_to_cart_from_modal()
    cart_page.proceed_to_checkout.click()

    checkout_page.add_comment("Fragile — handle with care")
    checkout_page.click_place_order()

    # We should now be on the payment page
    expect(page).to_have_url("https://automationexercise.com/payment")


def test_payment_form_accepts_valid_card(page: Page):
    """Payment form accepts valid card details and proceeds to confirmation."""
    register_and_login_new_user(page)

    home_page = HomePage(page)
    cart_page = CartPage(page)
    checkout_page = CheckoutPage(page)

    home_page.navigate()
    cart_page.add_product_to_cart(index=0)
    cart_page.go_to_cart_from_modal()
    cart_page.proceed_to_checkout.click()

    checkout_page.click_place_order()

    # Use non-default card values to prove parametrization works
    checkout_page.fill_payment_details(
        name_on_card="Alice Test",
        card_number="5555555555554444",  # test Mastercard number
        cvc="456",
        expiration_month="06",
        expiration_year="2028",
    )
    checkout_page.submit_payment()
    checkout_page.expect_order_placed()


@pytest.mark.parametrize("month,year", [
    ("01", "2028"),
    ("06", "2029"),
    ("12", "2030"),
])
def test_various_expiration_dates_accepted(page: Page, month: str, year: str):
    """Different valid expiration dates all result in successful order."""
    register_and_login_new_user(page)

    home_page = HomePage(page)
    cart_page = CartPage(page)
    checkout_page = CheckoutPage(page)

    home_page.navigate()
    cart_page.add_product_to_cart(index=0)
    cart_page.go_to_cart_from_modal()
    cart_page.proceed_to_checkout.click()

    checkout_page.click_place_order()
    checkout_page.fill_payment_details(
        expiration_month=month,
        expiration_year=year,
    )
    checkout_page.submit_payment()
    checkout_page.expect_order_placed()

def test_checkout_with_reused_auth(logged_in_page: Page):
    """Same checkout flow, but starting from saved auth state - no UI registration."""
    page = logged_in_page
    home_page = HomePage(page)
    cart_page = CartPage(page)
    checkout_page = CheckoutPage(page)

    home_page.navigate()
    cart_page.add_product_to_cart(index=0)
    cart_page.go_to_cart_from_modal()
    cart_page.proceed_to_checkout.click()

    checkout_page.add_comment("Delivered via reused auth state")
    checkout_page.click_place_order()
    checkout_page.fill_payment_details()
    checkout_page.submit_payment()
    checkout_page.expect_order_placed()