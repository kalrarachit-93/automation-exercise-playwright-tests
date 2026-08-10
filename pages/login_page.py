"""
Page Object for Automation Exercise login page.

The login page has TWO forms:
- Login form (left) - for existing users
- Signup form (right) - starts the account creation flow

Both forms contain an "Email Address" placeholder, so we scope our 
locators to their respective forms to avoid strict-mode violations.
"""

from playwright.sync_api import Page, expect


class LoginPage:
    """The Login / Signup entry page."""

    URL = "https://automationexercise.com/login"

    def __init__(self, page: Page):
        self.page = page

        # The two forms on the page
        login_form = page.locator("form").filter(has_text="Login")
        signup_form = page.locator("form").filter(has_text="Signup")

        # Login form locators
        self.login_email = login_form.get_by_placeholder("Email Address")
        self.login_password = login_form.get_by_placeholder("Password")
        self.login_button = login_form.get_by_role("button", name="Login")

        # Signup form locators
        self.signup_name = signup_form.get_by_placeholder("Name")
        self.signup_email = signup_form.get_by_placeholder("Email Address")
        self.signup_button = signup_form.get_by_role("button", name="Signup")

        # Feedback messages
        self.login_error = page.get_by_text(
            "Your email or password is incorrect!"
        )
        self.signup_error = page.get_by_text(
            "Email Address already exist!"
        )

    def navigate(self):
        """Navigate to the login page."""
        self.page.goto(self.URL)

    def login_as(self, email: str, password: str):
        """Fill the login form and submit."""
        self.login_email.fill(email)
        self.login_password.fill(password)
        self.login_button.click()

    def start_signup(self, name: str, email: str):
        """
        Fill the initial signup form (name + email) and submit.
        This takes the user to the 'Enter Account Information' page.
        """
        self.signup_name.fill(name)
        self.signup_email.fill(email)
        self.signup_button.click()

    def expect_login_error(self):
        """Assert the 'incorrect credentials' error message is visible."""
        expect(self.login_error).to_be_visible()

    def expect_signup_error(self):
        """Assert the 'email already exists' error message is visible."""
        expect(self.signup_error).to_be_visible()

    def expect_client_side_block(self):
        """Assert the login form was stopped by browser-side HTML5 validation
        (type=email / required) - i.e. the form is invalid and was never
        submitted to the server.
        """
        form_is_invalid = self.login_button.evaluate(
            "btn => !btn.closest('form').checkValidity()"
        )
        assert form_is_invalid, "Expected HTML5 validation to block submission"