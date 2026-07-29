"""
Product listing and product detail tests for Automation Exercise.

Covers navigation, search, and viewing individual products.
Ad-blocking fixture (from conftest.py) is applied automatically.
"""

import pytest
import re
from playwright.sync_api import Page, expect

from pages.home_page import HomePage
from pages.product_page import ProductPage


def test_products_page_loads_with_products(page: Page):
    """The products page loads and shows a grid of products."""
    home_page = HomePage(page)
    home_page.navigate()

    home_page.expect_products_visible()
    assert home_page.get_product_count() > 0


def test_home_page_shows_products(page: Page):
    """The site's home page also shows a product grid (Features Items)."""
    home_page = HomePage(page)
    home_page.navigate_home()

    assert home_page.get_product_count() > 0


def test_can_view_product_details(page: Page):
    """Clicking 'View Product' navigates to a product detail page."""
    home_page = HomePage(page)
    product_page = ProductPage(page)

    home_page.navigate()
    home_page.view_product_at(0)

    product_page.expect_loaded()
    product_page.expect_shows_price()
    product_page.expect_shows_availability()

    # URL should now be /product_details/<n>
    expect(page).to_have_url(re.compile(r"/product_details/\d+"))


def test_search_returns_results(page: Page):
    """Searching for a common term returns product results."""
    home_page = HomePage(page)
    home_page.navigate()
    home_page.search("dress")

    home_page.expect_search_results_visible()
    assert home_page.get_product_count() > 0


def test_search_with_no_matches_shows_no_products(page: Page):
    """Searching for a nonsense term returns no products."""
    home_page = HomePage(page)
    home_page.navigate()
    home_page.search("xyznothingmatchesthis12345")

    # We accept two valid outcomes for a no-results search:
    # either the count is 0 OR the searched-products heading is still shown
    # but with no product cards. Both are legitimate site behaviors.
    home_page.expect_search_results_visible()
    assert home_page.get_product_count() == 0


@pytest.mark.parametrize("search_term", [
    "dress",
    "top",
    "shirt",
])
def test_search_terms_return_results(page: Page, search_term: str):
    """Multiple common search terms each return at least one result."""
    home_page = HomePage(page)
    home_page.navigate()
    home_page.search(search_term)

    home_page.expect_search_results_visible()
    assert home_page.get_product_count() > 0, f"No results for '{search_term}'"