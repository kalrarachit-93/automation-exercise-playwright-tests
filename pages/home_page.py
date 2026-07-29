"""
Page Object for the Automation Exercise products / home page.

Covers the product listing page (/products) with search, product cards,
and category navigation. The site's home page (/) also shows a "Featured
Items" grid of the same products, so we support both entry points.
"""

from playwright.sync_api import Page, expect


class HomePage:
    """The products listing page."""

    PRODUCTS_URL = "https://automationexercise.com/products"
    HOME_URL = "https://automationexercise.com/"

    def __init__(self, page: Page):
        self.page = page

        # Search
        self.search_input = page.get_by_role("textbox", name="Search Product")
        self.search_button = page.locator("#submit_search")

        # Product cards — there are many on the page, so we get the first
        # "View Product" link when we need "any product"
        # Note: the visible text includes a leading space (from an icon)
        self.view_product_links = page.get_by_role("link", name=" View Product")

        # Section headings
        self.all_products_heading = page.get_by_role("heading", name="All Products")
        self.searched_products_heading = page.get_by_role("heading", name="Searched Products")

    def navigate(self):
        """Navigate to the products listing page."""
        self.page.goto(self.PRODUCTS_URL)

    def navigate_home(self):
        """Navigate to the site home page."""
        self.page.goto(self.HOME_URL)

    def search(self, query: str):
        """Type a search query and submit."""
        self.search_input.fill(query)
        self.search_button.click()

    def view_product_at(self, index: int = 0):
        """
        Click 'View Product' on the product at the given index.
        Default is 0 (the first product on the page).
        """
        self.view_product_links.nth(index).click()

    def expect_products_visible(self):
        """Assert the 'All Products' section is visible."""
        expect(self.all_products_heading).to_be_visible()

    def expect_search_results_visible(self):
        """Assert the 'Searched Products' section is visible after searching."""
        expect(self.searched_products_heading).to_be_visible()

    def get_product_count(self) -> int:
        """Return the number of product cards currently visible."""
        return self.view_product_links.count()