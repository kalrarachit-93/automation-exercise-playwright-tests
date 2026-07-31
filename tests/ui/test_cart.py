"""
Cart-related tests for Automation Exercise.

Covers adding, viewing, removing, and empty cart flows. The site allows
adding items to cart without being logged in, so these tests don't need
account setup.
"""

import pytest
from playwright.sync_api import Page, expect

from pages.home_page import HomePage
from pages.cart_page import CartPage


def test_can_add_product_to_cart(page: Page):
    """Adding a product from the products page shows the confirmation modal."""
    home_page = HomePage(page)
    cart_page = CartPage(page)

    home_page.navigate()
    cart_page.add_product_to_cart(index=0)

    # Confirmation modal should be visible (the add_product_to_cart already asserts this)


def test_added_product_appears_in_cart(page: Page):
    """After adding a product and clicking 'View Cart', the product is listed in the cart."""
    home_page = HomePage(page)
    cart_page = CartPage(page)

    home_page.navigate()
    cart_page.add_product_to_cart(index=0)
    cart_page.go_to_cart_from_modal()

    cart_page.expect_product_in_cart()
    assert cart_page.get_cart_item_count() == 1


def test_can_add_multiple_products(page: Page):
    """Adding two different products results in a cart with two items."""
    home_page = HomePage(page)
    cart_page = CartPage(page)

    home_page.navigate()
    cart_page.add_product_to_cart(index=0)
    cart_page.click_continue_shopping()
    cart_page.add_product_to_cart(index=3)
    cart_page.go_to_cart_from_modal()

    assert cart_page.get_cart_item_count() == 2


def test_can_remove_product_from_cart(page: Page):
    """After adding then removing a product, the cart shows the empty message."""
    home_page = HomePage(page)
    cart_page = CartPage(page)

    home_page.navigate()
    cart_page.add_product_to_cart(index=3)
    cart_page.go_to_cart_from_modal()

    # Confirm added
    assert cart_page.get_cart_item_count() == 1

    # Remove and confirm empty
    cart_page.remove_product_at(0)
    cart_page.expect_cart_empty()


def test_empty_cart_when_visited_directly(page: Page):
    """Navigating directly to the cart page in a fresh session shows the empty message."""
    cart_page = CartPage(page)

    cart_page.navigate()
    cart_page.expect_cart_empty()


def test_cart_persists_after_navigation(page: Page):
    """Adding a product then navigating away and back — the product remains."""
    home_page = HomePage(page)
    cart_page = CartPage(page)

    home_page.navigate()
    cart_page.add_product_to_cart(index=0)
    cart_page.click_continue_shopping()

    # Navigate away
    home_page.navigate_home()

    # Come back to cart via direct navigation
    cart_page.navigate()

    # Product should still be there
    assert cart_page.get_cart_item_count() == 1