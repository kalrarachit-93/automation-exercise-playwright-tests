"""
Page Object for the 'Enter Account Information' page.

This is the second step of signup. After submitting name + email on 
LoginPage, the user lands here to fill out the full profile.
"""

from playwright.sync_api import Page, expect


class SignupPage:
    """The account information page (second step of signup)."""

    def __init__(self, page: Page):
        self.page = page

        # Account information section
        self.title_mr = page.get_by_role("radio", name="Mr.")
        self.title_mrs = page.get_by_role("radio", name="Mrs.")
        self.password_input = page.get_by_role("textbox", name="Password")
        self.days_select = page.locator("#days")
        self.months_select = page.locator("#months")
        self.years_select = page.locator("#years")
        self.newsletter_checkbox = page.get_by_role("checkbox", name="Sign up for our newsletter!")
        self.offers_checkbox = page.get_by_role("checkbox", name="Receive special offers from our partners!")

        # Address information section
        self.first_name = page.get_by_role("textbox", name="First name")
        self.last_name = page.get_by_role("textbox", name="Last name")
        self.company = page.get_by_role("textbox", name="Company").first
        self.address = page.get_by_role("textbox", name="Address").first
        self.country_select = page.locator("#country")
        self.state = page.get_by_role("textbox", name="State")
        self.city = page.get_by_role("textbox", name="City")
        self.zipcode = page.locator("#zipcode")
        self.mobile = page.get_by_role("textbox", name="Mobile Number")

        # Create Account button + success message
        self.create_account_button = page.get_by_role("button", name="Create Account")
        self.account_created_message = page.get_by_text("Account Created!")
        self.continue_button = page.get_by_role("link", name="Continue")

    def fill_account_details(self, user):
        """
        Fill all the required account fields using a TestUser object.
        Selects Mr. by default; picks a fixed birthdate for simplicity.
        """
        self.title_mr.check()
        self.password_input.fill(user.password)

        # Birthdate — pick any valid date
        self.days_select.select_option("15")
        self.months_select.select_option("6")   # June
        self.years_select.select_option("1990")

        # Skip newsletter/offers (not required)

        # Address fields
        self.first_name.fill(user.first_name)
        self.last_name.fill(user.last_name)
        self.company.fill(user.company)
        self.address.fill(user.address)
        self.country_select.select_option("United States")
        self.state.fill(user.state)
        self.city.fill(user.city)
        self.zipcode.fill(user.zipcode)
        self.mobile.fill(user.mobile)

    def submit(self):
        """Click Create Account."""
        self.create_account_button.click()

    def expect_account_created(self):
        """Assert the 'Account Created!' success message appears."""
        expect(self.account_created_message).to_be_visible()

    def click_continue(self):
        """Click the Continue button on the 'Account Created!' page."""
        self.continue_button.click()